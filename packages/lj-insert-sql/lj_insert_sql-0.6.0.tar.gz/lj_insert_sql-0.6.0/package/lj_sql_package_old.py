import requests
from package.utils import LICENSE_URL
from sqltool.mysql_client import MySqlClient
import datetime
import logging
import logging.handlers
from lj_spider_core.version import change_to_lj_expression

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


class Public():
    def __init(self, origin_license):
        self.origin_license = origin_license

    def license(self):
        verified_license = self.__license_key(document=self.origin_license) if self.origin_license else ''
        if not verified_license:
            if not self.origin_license or self.origin_license is None:
                verified_license = ""
            else:
                verified_license = self.origin_license
            if len(verified_license) >= 50 or verified_license.endswith('...'):
                verified_license = ''
            logging.info(f'字段:{["handle_from_field"]} 清洗失败')
            return verified_license
        else:
            return verified_license

    def __license_key(self, document):
        try:
            url = LICENSE_URL
            headers = {
                'Content-Type': 'text/plain'
            }
            res = requests.post(url, data=document, headers=headers)
            return res.text
        except Exception as e:
            print(e)
            return False



class OldSqlTool(object):

    def _get_insert_sql(self, insert_data, table_name):
        datas = insert_data.items()
        insert_data_key = ','.join([x[0] for x in datas])
        data_value = [x[1] for x in datas]
        num_s = ('%s,' * len(insert_data))[:-1]
        update_data_key = ','.join([x[0] + '=%s' for x in datas])
        sql_insert = f'INSERT INTO `{table_name}`({insert_data_key}) VALUES({num_s}) ON DUPLICATE KEY UPDATE {update_data_key};'
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
        sql_increment = f"insert into {table_name} (id,is_insert,time,{insert_data_key}) VALUES({increment_id},{is_insert},curdate(),{num_s})"
        return sql_increment, data_value

    def data_to_db(self, insert_data, conn, table_name, increment_fields):
        '''
        :param table_info: 表的连接、数据库、表名信息
        :param insert_data: 插入的数据，字典形式-->{'字段名':值}
        :param incre_table_info: 增量表的连接、数据库、表名信息
        :param increment_fields:["lj_package_id","package_name","home_page","first_release_time","latest_release_time",
                        "latest_release", "description", "language", "keywords", "license", "verified_license"]
                        ["package_name","lj_package_id","version","published_time","license","verified_license"]
                        ["lj_package_id","package_version","dependency_package_name","dependency_package_version"]
        :return:
        '''
        increment_table_name = table_name + '_increment'
        increment_data = {}
        for each in increment_fields:
            increment_data[each] = insert_data[each]
        sql_insert, data_value = self._get_insert_sql(insert_data, table_name)
        with conn.cursor() as cursor:
            is_insert = cursor.execute(sql_insert, data_value * 2)  # 返回值为1，该记录不存在，插入了数据；返回值为2，该记录存在，并且更新了数据
            if is_insert != 0:
                sql_select_id = self._get_sql_select_id(insert_data, table_name)
                cursor.execute(sql_select_id)
                increment_id = cursor.fetchone()[0]
                sql_increment, data_value = self._get_increment_sql(increment_data, increment_table_name, increment_id,
                                                              is_insert)
                cursor.execute(sql_increment, data_value)
        conn.commit()
        return is_insert

    def restructure(self, dependency_package_name, dependency_version_expression, dependency_type, dependency_version):
        requirement_list = []
        requirement_list.append({'dependency_package_name': dependency_package_name,
                                        'dependency_version_expression': dependency_version_expression,
                                        'dependency_type': dependency_type,
                                        'dependency_version': dependency_version})
        return requirement_list


    # def package_deps(self, deps: PackageDeps):
    #     try:
    #         for result in deps.requirement:
    #             deps.dependency_package_name = result['dependency_package_name']
    #             deps.dependency_version_expression = result['dependency_version_expression']
    #             deps.dependency_type = result['dependency_type']
    #             deps.dependency_version = result['dependency_version']
    #
    #             deps_info = PackageInfo(result['dependency_package_name'], deps.package_type)
    #             deps.dependency_package_id = deps_info.select_id(self.conn_local)
    #             deps.lj_dependency_version_expression = change_to_lj_expression(deps.package_type,
    #                                                                             deps.dependency_version_expression)
    #             deps.save(self.conn_local)
    #         return True
    #     except Exception as e:
    #         print(e)
    #         return False


class LjId(Base):
    TABLE_NAME = 'lj_id_map_package'
    FIELDS = ('package_name', 'type')
    UNIQUE_FIELDS = ('package_name','type')

    def __init__(self, package_name, type):
        self.package_name = package_name
        self.type = type

    def select_id(self, client):
        found = client.select(
            table_name=self.TABLE_NAME,
            wheres=self.to_dict(with_unique=True, with_not_unique=False),
            limit=1
        )
        if not found:
            self.insert(client)
            found = client.select(
                table_name=self.TABLE_NAME,
                wheres=self.to_dict(with_unique=True, with_not_unique=False),
                limit=1
            )
        return found[0]['id']


class LjIdSqlTool(Base):
    """
        生成lj_id
    """
    def __init__(self, host, port, user, pwd, db, charset):
        self.conn_lj_id = MySqlClient(
            host=host,
            port=port,
            user=user,
            passwd=pwd,
            db=db,
            charset=charset
        )

    def insert_lj_package_id(self, lj: LjId):
        return lj.select_id(self.conn_lj_id)


