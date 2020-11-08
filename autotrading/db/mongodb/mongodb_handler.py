from pymongo import MongoClient

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

        if mode == "remote":
            self._client = MongoClient("mongodb://{user}:{password}@{remote_host}:{port}".format(**self.db_config))
        elif mode == "local":
            self._client = MongoClient("mongodb://{user}:{password}@{local_ip}:{port}".format(**self.db_config))

        self._db = self._client[db_name]
        self._collection = self._db[collection_name]
