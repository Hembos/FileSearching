from tkinter import Tk, Label, Button, Entry
from tkinter.filedialog import askopenfilename, askdirectory
import threading

from config import get_db_path

from db import DB


class App(Tk):
    def __init__(self):
        """Инициализация окна и виджетов"""
        super().__init__()
        self.geometry('700x600')
        self.title('Поиск файлов')

        self.db_path_lbl = Label(self, text='Путь к базе данных: ' + get_db_path())
        self.db_path_lbl.grid(column=0, row=0)
        self.db_path_btn = Button(self, text="Изменить путь", command=self.choose_db)
        self.db_path_btn.grid(column=1, row=0)

        self.add_files_btn = Button(self, text='Добавить новые файлы', command=self.a)
        self.add_files_btn.grid(column=0, row=1)

        self.search_file_txt = Entry(self, width=100)
        self.search_file_txt.grid(column=0, row=4)

        self.search_btn = Button(self, text='Найти', command=self.search_file)
        self.search_btn.grid(column=1, row=4)

        self.search_result_lbl = Label(self, text='')
        self.search_result_lbl.grid(column=0, row=5)

        self.add_files_txt = Entry(self, width=100)
        self.add_files_txt.grid(column=0, row=6)

        self.file_to_pdf_btn = Button(self, text='Конвертировать', command=self.file_to_pdf)
        self.file_to_pdf_btn.grid(column=1, row=7)

        self.file_to_pdf_txt = Entry(self, width=100)
        self.file_to_pdf_txt.grid(column=0, row=7)

    def choose_db(self):
        """Выбор файла с базой данных"""
        file_types = (("База данных", "*.db"), )
        file_name = askopenfilename(title="Открытый файл", initialdir='/', filetypes=file_types)
        print(file_name)

        with open('config.txt', 'r') as file:
            path = False
            lines = file.readlines()

            for i in range(len(lines)):
                if lines[i].find('DATABASE_PATH=') == 0:
                    lines[i] = 'DATABASE_PATH=' + file_name
                    path = True
                    break

        with open('config.txt', 'w') as file:
            if not path:
                lines.append('DATABASE_PATH=' + file_name)

            for line in lines:
                file.write(line + '\n')

        self.db_path_lbl.config(text='Путь к базе данных: ' + get_db_path())

    def a(self):
        thread = threading.Thread(target=self.add_files_in_db)
        thread.start()

    def add_files_in_db(self):
        """Добавляет файлы в базу данных при нажатии на кнопку"""
        if self.add_files_txt.get() != "":
            directory = self.add_files_txt.get()
        else:
            directory = askdirectory(title="Открыть папку", initialdir="/")

        lbl_proc = Label(self, text='В процесе...')
        lbl_proc.grid(column=0, row=3)

        data_base = DB()
        data_base.recording_path_and_files(directory)

        lbl_proc.config(text='Готово')

    def search_file(self):
        """Поиск файла"""
        file = self.search_file_txt.get()

        data_base = DB()
        paths = data_base.file_searching(file)

        text = ''
        for path in paths:
            text += path + '\n'

        self.search_result_lbl.config(text=text)

    def file_to_pdf(self):
        """Переводит file в pdf"""
        directory = self.file_to_pdf_txt.get()

        
