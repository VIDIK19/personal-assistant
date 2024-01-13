"""
 В цьому модулі реалізовано два класи, Note та NoteData.

 1. Note
    При створенні екземпляра приймає один аргумент - текст нотатки.
    Кожен екземпляр має унікальний ID, за яким зберігається у класі NoteData.
    Має методи add_tag, edit_tag, edit_info.
    ! Методи edit_tag та edit_info ще будуть дороблятися - хочу, щоб у консоль виводило 
        наявний текст, який можна редагувати, а не писати текст наново.
    Магічний метод __str__ виводить у консоль таблицю для зручного відображення нотатки.
 2. NoteData(UserDict)
    При ініціалізації підвантажує дані з файлу в папці database, якщо такий є.
    Метод add_note приймає за аргумент екземпляр класу Note та зберігає його у словнику {note_id: Note}
    Метод id_search приймає за аргумент ID нотатки та повертає нотатку у вигляді таблиці
    Метод tag_search приймає строку та шукає співпадіння з тегами нотаток у БД (повертає у вигляді таблиці для БД)
    Метод delete_note видаляє нотатку за ID.
    Метод clear_data очищує БД (файл теж чистить)
    
"""



from tabulate import tabulate
from collections import UserDict
import pickle
import os



current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
DATA_PATH = f'{project_root}\database\\notes.pkl'


class Note:
    note_counter = 0

    def __init__(self, info:str):
        Note.note_counter += 1
        self.note_id = Note.note_counter 
        self.tags = []
        self.info = info
        
        

    def add_tag(self, tag:str) -> None:
        self.tags.append(tag)

    def edit_tag(self, old_tag_ind, new_tag:str) -> None:
        self.tags[old_tag_ind] = new_tag
    
    def edit_info(self, new_info:str) -> None:
        self.info = new_info


    def table(self) -> str:
        header = [f'              Note ID:{self.note_id}']

        field_1 = ['Tags',]
        text_block = ''
        for tag in self.tags:
            text_block += "> " + tag + "\n"
        
        field_1.append(text_block)

        field_2 = ['Info', ]
        width_of_string = 0

        lst_for_info = [] 

        while width_of_string < len(self.info):
            lst_for_info.append(self.info[width_of_string: width_of_string + 40])
            width_of_string += 40
        
        info = "\n".join(lst_for_info)
        field_2.append(info)

        table = tabulate([field_1, field_2], headers=header, tablefmt='grid' )
        
        return str(table)

class NoteData(UserDict):
    def __init__(self):
        super().__init__()
        self.load_data()

    def add_note(self, note:Note) -> None:
        self.data[note.note_id] = note
        self.save_data()
    
    def id_search(self, note_id: int) -> str:
        if note_id in self.data:
            return self.data[note_id].table()

            

    def tag_search(self, tag:str) -> str:
        search_dict = {}
        for note in self.data.values():
            for el in note.tags:
                if el.startswith(tag):
                    search_dict[note.note_id] = note

        headers = ["Note ID", "Tags", "Info"]
        fields = []

        for note in search_dict.values():
            tag_block = ''
            for tag in note.tags:
                tag_block += "> " + tag + "\n"

            info_block = note.info[:20] + "\n" + "..."
            field = [note.note_id, tag_block, info_block]

            fields.append(field)
        
        table = tabulate(fields, headers=headers, tablefmt='grid')
        return (table)


    def delete_note(self, note_id) ->None:
        del self.data[note_id]
        self.save_data()

    def open_note(self, note_id) -> str:
        return self.data[note_id].table()


    def save_data(self):
        with open(DATA_PATH, 'wb') as file:
            pickle.dump(self.data, file)

    
    def load_data(self):
        try:
            with open(DATA_PATH, "rb") as file:
                self.data = pickle.load(file)
                if self.data.keys():
                    Note.note_counter = list(self.data.keys())[-1]
                else:
                    Note.note_counter = 0
        except FileNotFoundError:
            self.data = {}

    def clear_data(self):
        self.data = {}
        self.save_data()
    

    def data_table(self):
        headers = ["Note ID", "Tags", "Info"]
        fields = []

        for note in self.data.values():
            tag_block = ''
            for tag in note.tags:
                tag_block += "> " + tag + "\n"

            info_block = note.info[:20] + "\n" + "..."
            field = [note.note_id, tag_block, info_block]

            fields.append(field)
        
        table = tabulate(fields, headers=headers, tablefmt='grid')
        return table

