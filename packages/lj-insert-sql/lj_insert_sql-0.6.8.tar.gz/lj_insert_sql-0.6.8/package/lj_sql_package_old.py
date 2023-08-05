from sqltool.mysql_client import MySqlClient
import logging.handlers

logging.getLogger().addHandler(logging.StreamHandler())
logging.getLogger("sql_client").addHandler(logging.StreamHandler())

'''
hex_package_info
'''


class Base:
    TABLE_NAME = None
    FIELDS = ()
    UNIQUE_FIELDS = ()

    def to_dict(self, *, with_unique, with_not_unique=True, with_null_value=False):
        ret = dict()
        for key in self.FIELDS:
            value = getattr(self, key)
            is_unique = key in self.UNIQUE_FIELDS
            if (with_unique == is_unique or with_not_unique == (not is_unique)) \
                    and (with_null_value or (value is not None)):
                ret[key] = value
        return ret

    def update(self, client):
        data = self.to_dict(with_unique=False)
        if not data:
            return
        return client.update(
            update_columns=self.to_dict(with_unique=False),
            table_name=self.TABLE_NAME,
            wheres=list(self.to_dict(with_unique=True, with_not_unique=False).items())
        )

    def insert(self, client):
        data = self.to_dict(with_unique=True)
        sql = client.gen_insert_sql([data], table_name=self.TABLE_NAME, field_list=list(data.keys()))
        client.execute(sql)

    def pre_save(self, client):
        pass

    def save(self, client):
        self.pre_save(client)
        found = client.select(
            table_name=self.TABLE_NAME,
            wheres=list(self.to_dict(with_unique=True, with_not_unique=False).items()),
            limit=1
        )
        if found:
            self.update(client)
        else:
            self.insert(client)


class OldSqlTool(object):
    def __init__(self, host, port, user, pwd, db, charset):
        self.conn_local = MySqlClient(
                                    host=host,
                                    port=port,
                                    user=user,
                                    passwd=pwd,
                                    db=db,
                                    charset=charset)

    def _get_insert_sql(self, insert_data, table_name):
        datas = insert_data.items()
        insert_data_key = ','.join([x[0] for x in datas])
        data_value = [x[1] for x in datas]
        num_s = ('%s,' * len(insert_data))[:-1]
        update_data_key = ','.join([x[0] + '=%s' for x in datas])
        sql_insert = f'INSERT INTO `{table_name}`({insert_data_key}) ' \
                     f'VALUES({num_s}) ON DUPLICATE KEY UPDATE {update_data_key};'
        return sql_insert, data_value

    def _get_sql_select_id(self, data, table_name):
        query_fields = ["package_name", "lj_package_id", "version", "package_version", "dependency_package_name",
                        "dependency_package_version", "dependency_environment"]
        sql_list = []
        for each in query_fields:
            if each in data.keys():
                if data[each] is None:
                    sql_list.append(f'{each} is null')
                else:
                    sql_list.append(f'{each} = "{data[each]}"')
        sql_query = ' and '.join(sql_list)
        sql_select_id = f"select id from {table_name} where {sql_query}"
        return sql_select_id

    def _get_increment_sql(self, increment_data, table_name, increment_id, is_insert):
        datas = increment_data.items()
        insert_data_key = ','.join([x[0] for x in datas])
        data_value = [x[1] for x in datas]
        num_s = ('%s,' * len(increment_data))[:-1]
        sql_increment = f"insert into {table_name} (id,is_insert,time,{insert_data_key}) " \
                        f"VALUES({increment_id},{is_insert},curdate(),{num_s})"
        return sql_increment, data_value

    def data_to_db(self, insert_data, table_name, increment_fields):
        """
        :param table_name: 表的连接、数据库、表名信息
        :param insert_data: 插入的数据，字典形式-->{'字段名':值}
        :param : 增量表的连接、数据库、表名信息
        :param increment_fields:["lj_package_id","package_name","home_page","first_release_time","latest_release_time",
                      "latest_release", "description", "language", "keywords", "license", "verified_license"]
                      ["package_name","lj_package_id","version","published_time","license","verified_license"]
                      ["lj_package_id","package_version","dependency_package_name","dependency_package_version"]
        :return:
        """
        increment_table_name = table_name + '_increment'
        increment_data = {}
        for each in increment_fields:
            increment_data[each] = insert_data[each]
        sql_insert, data_value = self._get_insert_sql(insert_data, table_name)
        # 返回值为1，该记录不存在，插入了数据；返回值为2，该记录存在，并且更新了数据
        is_insert = self.conn_local.execute(sql_insert, data_value * 2)
        if is_insert != 0:
            sql_select_id = self._get_sql_select_id(insert_data, table_name)
            increment_id = self.conn_local.get_one(sql_select_id)['id']
            sql_increment, data_value = self._get_increment_sql(
                increment_data, increment_table_name, increment_id, is_insert
            )
            self.conn_local.execute(sql_increment, data_value)
        return is_insert

    def restructure(self, dependency_package_name, dependency_version_expression, dependency_type, dependency_version):
        requirement = []
        requirement.append({
                'dependency_package_name': dependency_package_name,
                'dependency_version_expression': dependency_version_expression,
                'dependency_type': dependency_type,
                'dependency_version': dependency_version})
        return requirement
