from sqlite3 import connect

import os


connection = connect('C:/Users/ruharfa/PycharmProjects/TelegramBot/TelegramBot.db')
cursor = connection.cursor()

with connection:
    i = 0
    for dir_path, dir_names, file_names in os.walk('//s0002159/exchange/Sovetsk_Converting/1.Safety/5S Converting/New folder/'):
        print(i)
        i += 1
        if cursor.execute('SELECT * FROM Paths WHERE Path = ?', (dir_path,)).fetchone() is None:
            cursor.execute('INSERT INTO Paths (Path) VALUES (?)', (dir_path,))
            path_id = cursor.lastrowid
            for file in file_names:
                print(file)
                cursor.execute('INSERT INTO Files (Path_id, File) VALUES (?, ?)', (path_id, file))