import uuid

from postgresql import DbManager, DbManagerProtocol


class EphemeralPostgreSqlDbContext:

    __db_manager: DbManagerProtocol
    __scripts: [str]
    __db_name: str

    def __init__(self,
                 connection_string,
                 scripts: [str],
                 db_manager: DbManagerProtocol = None):

        supported_data_sources = ['localhost', '127.0.0.1']

        connection_params = self.__get_connection_string_params(connection_string)
        if connection_params.get('SERVER', None) not in supported_data_sources:
            raise Exception('Ephemeral database server must be local, use localhost or 127.0.0.1 as server address.')

        if 'DATABASE' in connection_params:
            raise Exception('Ephemeral database name should not be included on the connection string, please remove DATABASE parameter.')

        self.__db_manager = db_manager or DbManager(connection_params)
        self.__scripts = scripts

    def __enter__(self):
        self.__db_name = f'edb_{uuid.uuid4().hex}'
        self.__db_manager.create_database(self.__db_name)
        scripts_errors = []
        for script in self.__scripts:
            try:
                self.__db_manager.execute_non_query(script, self.__db_name)
            except Exception as e:
                scripts_errors.append(e)
        return self, self.__db_name, scripts_errors

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.__db_manager.drop_database(self.__db_name)

    def get_all_database_names(self):
        query_result = self.__db_manager.execute_query(
            'SELECT datname as name FROM pg_database;',
            ''
        )
        return [item.get('name') for item in query_result]

    def get_all_table_names(self):
        query_result = self.__db_manager.execute_query(
            f'SELECT tablename as name FROM pg_catalog.pg_tables;',
            self.__db_name
        )
        return [item.get('name') for item in query_result]

    def get_row_count(self, table_name) -> int:
        query_result = self.__db_manager.execute_query(
            f'SELECT count(*) as row_count FROM {table_name};',
            self.__db_name
        )
        if len(query_result) == 0:
            return 0
        return query_result[0].get('row_count')

    @staticmethod
    def __get_connection_string_params(connection_string) -> dict:
        connection_string_params = {}
        for part in connection_string.split(';'):
            key_value_pair_array = part.split('=')
            if len(key_value_pair_array) != 2:
                continue
            if key_value_pair_array[0].upper() == 'SERVER':
                host_and_port = key_value_pair_array[1].split(',')
                connection_string_params['SERVER'] = host_and_port[0]
                if len(host_and_port) == 2:
                    connection_string_params['PORT'] = int(host_and_port[1])
            elif key_value_pair_array[0].upper() == 'PORT':
                connection_string_params[key_value_pair_array[0].upper()] = int(key_value_pair_array[1])
            else:
                connection_string_params[key_value_pair_array[0].upper()] = key_value_pair_array[1]
        return connection_string_params
