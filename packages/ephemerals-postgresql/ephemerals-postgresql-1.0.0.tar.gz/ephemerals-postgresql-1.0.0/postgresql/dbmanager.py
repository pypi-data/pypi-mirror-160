import abc
from abc import ABC

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT


class DbManagerProtocol(ABC):
    @abc.abstractmethod
    def create_database(self, name: str):
        pass

    @abc.abstractmethod
    def execute_non_query(self, sentence: str, at: str):
        pass

    @abc.abstractmethod
    def execute_query(self, sentence: str, at: str) -> [dict]:
        pass

    @abc.abstractmethod
    def drop_database(self, name: str):
        pass


class DbManager(DbManagerProtocol):

    __connection_params: dict

    def __init__(self, connection_params):
        self.__connection_params = connection_params

    def create_database(self, name: str):
        cnn = self.connect()
        cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = cnn.cursor()
        cursor.execute(f'create database {name};')
        cursor.close()
        cnn.close()

    def execute_non_query(self, sentence: str, at: str):
        cnn = self.connect(at)
        cursor = cnn.cursor()
        cursor.execute(sentence)
        cnn.commit()
        cursor.close()
        cnn.close()

    def execute_query(self, sentence: str, at: str) -> [dict]:
        cnn = self.connect(at)
        cursor = cnn.cursor()
        cursor.execute(sentence)
        columns = [column[0] for column in cursor.description]
        results = []
        for row in cursor.fetchall():
            results.append(dict(zip(columns, row)))
        cursor.close()
        cnn.close()
        return results

    def drop_database(self, name: str):
        cnn = self.connect()
        cnn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = cnn.cursor()
        cursor.execute(f'drop database {name} WITH (FORCE);')
        cursor.close()
        cnn.close()

    def connect(self, db_name=None, schema=None):
        params = {
            'user': self.__connection_params.get('USER ID'),
            'password':  self.__connection_params.get('PASSWORD'),
            'host':  self.__connection_params.get('SERVER'),
            'port': self.__connection_params.get('PORT')
        }
        if db_name is not None:
            params['database'] = db_name
        if schema is not None:
            params['options'] = f'-c search_path={schema}'

        return psycopg2.connect(**params)
