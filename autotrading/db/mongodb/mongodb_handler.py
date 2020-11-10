import configparser

from pymongo import MongoClient, CursorType

from autotrading.db.base_handler import DBHandler


class MongoDBHandler(DBHandler):
    """
    PyMongo 를 래핑해서 사용하는 클래스. DBHandler 추상 클래스를 상속.
    리모트 DB와 로컬 DB를 모두 사용할 수 있도록 __init__에서 mode로 구분
    """
    
    def __init__(self, mode="local", db_name=None, collection_name=None):
        """
        MongoDBHandler __init__ 구현부
        :param mode: 로컬 or 리모트 DB인지 구분 -> "local", "remote"
        :param db_name: 데이터베이스 명
        :param collection_name: 콜렉션 명

        :raise
            db_name 과 collection_name 이 없으면 Exception 발생
        """

        if db_name is None or collection_name is None:
            raise Exception("Need to db name and collection name")

        config = configparser.ConfigParser()
        config.read('conf/config.ini')

        self.db_config = {}
        self.db_config["local_ip"] = config["MONGODB"]["local_ip"]
        self.db_config["port"] = config["MONGODB"]["port"]
        # self.db_config["remote_host"] = config["MONGODB"]["remote_host"]
        # self.db_config["remote_port"] = config["MONGODB"]["remote_port"]
        # self.db_config["user"] = config["MONGODB"]["user"]
        # self.db_config["password"] = config["MONGODB"]["password"]

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))
        elif mode == "local":
            self._client = MongoClient("mongodb://{local_ip}:{port}".format(**self.db_config))

        self._db = self._client[db_name]
        self._collection = self._db[collection_name]

    def set_db_collection(self, db_name=None, collection_name=None):
        """
        MongoDB 에서 작업하려는 database 와 collection 을 변경할때 사용
        :param db_name: database 에 해당하는 이름
        :param collection_name: database 에 속하는 collection 이름
        :return: None
        """
        if db_name is None:
            raise Exception("Need to dbname name")

        self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]

    def get_current_db_name(self):
        """
        현재 MongoDB 에서 작업 중인 database 의 이름을 반환합니다.

        :raises:
            self._db.name : 현재 사용중인 database 이름을 반환
        """
        return self._db.name

    def get_current_collection_name(self):
        """
        현재 MongoDB 에서 작업 중인 collection 의 이름을 반환합니다.

        :raises:
            self._collection.name : 현재 사용중인 collection 이름을 반환
        """
        return self._collection.name

    def insert_item(self, data, db_name=None, collection_name=None):
        """
        MongoDB 에 하나의 document 를 입력하기 위한 메소드
        :param data:
        :param db_name:
        :param collection_name:
        :return: inserted_id : 입력 완료된 문서의 ObjectId 반환
        """
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.insert_one(data).inserted_id

    def insert_items(self, datas, db_name=None, collection_name=None):
        """
        MongoDB에 다수의 document 를 입력하기 위한 메소드
        :param datas:
        :param db_name:
        :param collection_name:
        :return: inserted_ids : 입력 완료된 문서의 objectId list 를 반환
        """
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.insert_many(datas).inserted_ids

    def find_items(self, condition=None, db_name=None, collection_name=None):
        """
        MongoDB 에서 다수의 document 를 검색하기 위한 메소드
        :param condition: 검색조건을 dictionary 형태로 입력 받음
        :param db_name:
        :param collection_name:
        :return: Cursor 를 반환
        """
        if condition is None:
            condition = {}  # dictionary
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find(condition, no_cursor_timeout=True, cursor_type=CursorType.EXHAUST)

    def find_item(self, condition, db_name=None, collection_name=None):
        """
        MongoDB 에서 하나의 document 를 검색하기 위한 메소드
        :param condition: 검색조건을 dictionary 형태로 입력 받음
        :param db_name:
        :param collection_name:
        :return: 검색된 문서가 있으면 문서의 내용을 반환
        """
        if condition is None:
            condition = {}  # dictionary
        if db_name is not None:
            self._db = self._client[db_name]
        if collection_name is not None:
            self._collection = self._db[collection_name]
        return self._collection.find_one(condition)



