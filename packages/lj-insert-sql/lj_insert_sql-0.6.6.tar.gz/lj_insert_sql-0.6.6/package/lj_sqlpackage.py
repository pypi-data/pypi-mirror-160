import requests
from sqltool.mysql_client import MySqlClient
import datetime
import logging
import logging.handlers
from package.utils import LICENSE_URL
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


class PackageType(Base):
    TABLE_NAME = 'package_type'
    FIELDS = ('package_type', 'name', 'language')
    UNIQUE_FIELDS = ('package_type',)

    """
    :param package_type   唯一标识
    :param name         名称
    :param language     语言
    """

    def __init__(self, package_type, name, language):
        self.package_type = package_type
        self.name = name
        self.language = language


class PackageFile(Base):
    TABLE_NAME = 'package_file'
    FIELDS = ('file_name', 'version', 'file_type', 'file_md5', 'package_type', 'package_id')
    UNIQUE_FIELDS = ('file_name', 'package_id')

    def __init__(self, file_name, version, package_type, file_type, file_md5):
        self.version = version
        self.file_name = file_name
        self.file_type = file_type
        self.file_md5 = file_md5
        self.package_type = package_type
        self.package_id = None

    def pre_save(self, client):
        info = PackageInfo(self.file_name, self.file_type)
        self.package_id = info.select_id(client)


class PackageInfo(Base):
    TABLE_NAME = 'package_info'
    FIELDS = ('package_name', 'package_type', 'description', 'home_page', 'repository_url', 'license_key', 'license',
              'last_version')
    UNIQUE_FIELDS = ('package_name', 'package_type')

    def __init__(self, package_name, package_type, license=None, description=None, home_page=None, repository_url=None,
                 last_version=None):
        self.package_name = package_name
        self.description = description
        self.home_page = home_page
        self.repository_url = repository_url
        self.package_type = package_type
        self.license = license
        self.license_key = None
        self.last_version = last_version

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

    def pre_save(self, client):
        if self.license:
            self.license_key = Public.license(self.license)
        return self.license_key


class PackageVersion(Base):
    TABLE_NAME = 'package_version'
    # 字段必须和__init__一致
    FIELDS = ('version', 'publish_time', 'package_name', 'license', 'package_type', 'package_id', 'license_key')
    UNIQUE_FIELDS = ('package_id', 'version')

    def __init__(self, package_name, package_type, version, publish_time=None, license=None):
        self.version = version
        self.publish_time = publish_time
        self.package_name = package_name
        self.license = license
        self.package_type = package_type
        self.package_id = None
        self.license_key = None

    def pre_save(self, client):
        info = PackageInfo(self.package_name, self.package_type)
        self.package_id = info.select_id(client)
        if self.license:
            self.license_key = Public.license(self.license)


class PackageDependencies(Base):
    TABLE_NAME = 'package_dependencies'
    FIELDS = ('package_name', 'package_type', 'package_version', 'dependency_package_name',
              'dependency_version_expression', 'dependency_type', 'dependency_version', 'dependency_package_id',
              'lj_dependency_version_expression', 'package_id')
    UNIQUE_FIELDS = ('dependency_package_id', 'package_type', 'package_id', 'dependency_version_expression')

    def __init__(self, package_name, package_type, package_version):
        self.package_name = package_name
        self.package_type = package_type
        self.package_version = package_version

        self.dependency_package_name = None
        self.dependency_version_expression = None
        self.dependency_type = None
        self.dependency_version = None
        self.dependency_package_id = None

        self.lj_dependency_version_expression = None
        self.package_id = None

        self.requirement = []

    def restructure(self, dependency_package_name, dependency_version_expression, dependency_type, dependency_version):
        return self.requirement.append({'dependency_package_name': dependency_package_name,
                                        'dependency_version_expression': dependency_version_expression,
                                        'dependency_type': dependency_type,
                                        'dependency_version': dependency_version})

    def pre_save(self, client):
        info = PackageInfo(self.package_name, self.package_type)
        self.package_id = info.select_id(client)


class Public:
    def __init__(self, origin_license):
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



class SqlTool(object):
    def __init__(self, host, port, user, pwd, db, charset):
        self.conn_local = MySqlClient(
            host=host,
            port=port,
            user=user,
            passwd=pwd,
            db=db,
            charset=charset
        )
        self.create_time = datetime.datetime.strftime(datetime.datetime.now(), '%Y-%m-%d %H:%M:%S')

    def package_file(self, file: PackageFile):
        file.save(self.conn_local)

    def package_info(self, package: PackageInfo):
        try:
            package.save(self.conn_local)
            return True
        except Exception as e:
            print(e)
            return False

    def package_version(self, version: PackageVersion):
        try:
            version.save(self.conn_local)
            return True
        except Exception as e:
            print(e)
            return False

    def dependencies(self, deps: PackageDependencies):
        try:
            for result in deps.requirement:
                deps.dependency_package_name = result['dependency_package_name']
                deps.dependency_version_expression = result['dependency_version_expression']
                deps.dependency_type = result['dependency_type']
                deps.dependency_version = result['dependency_version']
                deps_info = PackageInfo(result['dependency_package_name'], deps.package_type)
                deps.dependency_package_id = deps_info.select_id(self.conn_local)
                deps.lj_dependency_version_expression = change_to_lj_expression(deps.package_type,
                                                                                deps.dependency_version_expression)
                deps.save(self.conn_local)
            return True
        except Exception as e:
            print(e)
            return False

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

