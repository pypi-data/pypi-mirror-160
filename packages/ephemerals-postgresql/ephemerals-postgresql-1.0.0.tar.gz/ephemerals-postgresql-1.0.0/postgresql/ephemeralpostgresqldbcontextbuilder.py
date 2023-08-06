from typing import List

from postgresql import FilesManagerProtocol, FilesManager, DbManagerProtocol, EphemeralPostgreSqlDbContext


class EphemeralPostgreSqlDbContextBuilder:

    __files_manager: FilesManagerProtocol
    __scripts: List[str]

    def __init__(self, files_manager: FilesManagerProtocol = None):
        self.__files_manager = files_manager or FilesManager()
        self.__scripts = []

    def add_script_from_file(self, filepath):
        self.__scripts.append(self.__files_manager.read_all_text(filepath))
        return self

    def add_script(self, sentence):
        self.__scripts.append(sentence)
        return self

    def build(self,
              connection_string,
              db_manager: DbManagerProtocol = None):
        return EphemeralPostgreSqlDbContext(connection_string,
                                            self.__scripts,
                                            db_manager)
