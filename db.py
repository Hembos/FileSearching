from sqlite3 import connect

import os

from config import get_db_path


class DB:
    def __init__(self):
        """Подключение к бд"""
        self.connection = connect(get_db_path())
        self.cursor = self.connection.cursor()

    def recording_path_and_files(self, start):
        """Записывает пути и файлы в базу данных"""
        with self.connection:
            i = 0
            for dir_path, dir_names, file_names in os.walk(start):
                print(i)
                i += 1
                if self.cursor.execute('SELECT * FROM Paths WHERE Path = ?', (dir_path,)).fetchone() is None:
                    self.cursor.execute('INSERT INTO Paths (Path) VALUES (?)', (dir_path,))
                    path_id = self.cursor.lastrowid
                    for file in file_names:
                        self.cursor.execute('INSERT INTO Files (Path_id, File) VALUES (?, ?)', (path_id, file))

    def file_searching(self, file_name):
        """Ищет файл в базе данных и возвращает существующие пути к файлам с таким названием"""
        with self.connection:
            path_ids = self.cursor.execute('SELECT Path_id FROM Files WHERE File = ?', (file_name,)).fetchall()
            paths = []
            for path_id in path_ids:
                paths.append(self.cursor.execute('SELECT Path FROM Paths WHERE Id = ?', (path_id[0],)).fetchone()[0])

        return paths
