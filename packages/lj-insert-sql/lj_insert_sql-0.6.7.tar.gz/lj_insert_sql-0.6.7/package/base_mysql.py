'''
Author: jiaochanghao jch_2154195820@163.com
Date: 2022-07-21 10:07:46
LastEditors: jiaochanghao jch_2154195820@163.com
LastEditTime: 2022-07-21 14:55:28
FilePath: /insertpackage/package/base_mysql.py
Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
'''
from lj_spider_core.spider.base.rabbit_mq import RabbitMQ
from package.lj_sql_package_old import OldSqlTool
from package.lj_sqlpackage import *

class ToMysql:
    def __init__(self, package_type, connection_parameters, mysql_configure: dict, old_mysql_configure: dict):
        """
        :param package_type: 包类型 : hex_info  hex_version hex_dependencies
        :param connection_parameters: rabbitmq连接
        :param mysql_configure: 新表连接
        :param old_mysql_configure: 旧表连接
        """
        self.package_type = package_type
        self.connection_parameters = connection_parameters
        # 新表连接
        self.mysql_client = SqlTool(host=old_mysql_configure['host'],port=int(old_mysql_configure['port']),
                                    user=old_mysql_configure['user'],pwd=old_mysql_configure['pwd'],
                                    charset=old_mysql_configure['charset'], db=old_mysql_configure['db'])
        # 旧表连接
        self.old_mysql_client = OldSqlTool(host=mysql_configure['host'],port=int(mysql_configure['port']),
                                    user=mysql_configure['user'],pwd=mysql_configure['pwd'],
                                    charset=mysql_configure['charset'], db=mysql_configure['db'])
        # 过滤包语言
        self.package_classes = ['pip', 'maven', 'npm', 'nuget', 'cargo', 'go',
                                'coco', 'c', 'ruby', 'composer', 'hex', 'nvd', 'snyk']

    def set_mysql(self, insert_data, increment_fields):
        """
        :param insert_data: 插入的数据，字典形式-->{'字段名':值}
        :param increment_fields: ["lj_package_id","package_name","home_page","first_release_time","latest_release_time",
                      "latest_release", "description", "language", "keywords", "license", "verified_license"]
                      ["package_name","lj_package_id","version","published_time","license","verified_license"]
                      ["lj_package_id","package_version","dependency_package_name","dependency_package_version"]
        :return:
        """
        package_type = self.package_type.split('_')
        if isinstance(package_type[0], str):
            assert package_type[0] in self.package_classes
            table_name = f"package_{package_type[1]}"
            old_table_name = f"{package_type[0]}_package_{package_type[1]}"
            if table_name:
                # 入库fosseye数据库旧表
                return self.old_mysql_client.data_to_db(insert_data, table_name, increment_fields)
            elif old_table_name:
                # 入库fosseye数据库新表
                if package_type[1] == 'info':
                    inser = PackageInfo()
                if package_type[1] == 'version':
                    inser = PackageVersion()
                if package_type[1] == 'dependencies':
                    inser = PackageDependencies()
                f"{self.mysql_client}.{table_name}"(inser)
            else:
                return

# mysql_configure = {"host":"localhost", "port":3306, "user":"root", "pwd":"123", "charset":"utf8", "":"", "":"",}
# sql_conf_list = []
# for conf, par in mysql_configure.items():
#     mysql_configure = str(conf) + '=' + str(par)
#     sql_conf_list.append(mysql_configure)
# configure = ','.join(sql_conf_list)
# mysql_client = SqlTool(configure)

# mysql_client.

a = {"host":"localhost", "port":3306, "user":"root", "pwd":"123", "charset":"utf8", "db":"data_center"}
b = {"host":"localhost", "port":3306, "user":"root", "pwd":"123", "charset":"utf8", "db":"fosseye"}
tomysql = ToMysql('hex_info',1, a, b)
tomysql.set_mysql({'1':2},{'1':'2'})

