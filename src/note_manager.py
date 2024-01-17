from tabulate import tabulate
from collections import UserDict
import pickle
import os



current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
DATA_PATH = f'{project_root}\database\\notes.pkl'


class NoteManager:
    def __init__(self):
        self.data = NoteData()

    def show_data(self):
        return print(self.data.table(self.data))
    
    def clear_data(self):
        self.data.clear_data()
    
    def add_note(self, info:str):
        note = Note(info)
        self.data[note.note_id] = note
        self.data.save_data()
    
    def edit_info(self, note_id:int, new_info:str):
        self.data[note_id].info = new_info

    def add_tag(self, note_id:int, tag:str):
        note = self.data[note_id]
        note.tags.append(tag)
        self.data.save_data()

    def delete_note(self, note_id:int):
        del self.data[note_id]
        self.data.save_data()

    def open_note(self, note_id:int) -> str(tabulate):
        return print(self.data[note_id].table())
    
    def edit_tag(self, note_id:int, tag_index:int, new_tag:str): # tag and info through console
        self.data[note_id].tags[tag_index] = new_tag
        self.data.save_data()

    def search_tag(self, search_tag:str) -> str(tabulate):
        matches = {}
        for note in self.data.values():
            for tag in note.tags:
                if tag.startswith(search_tag):
                    matches[note.note_id] = note
        if len(matches.keys()) == 0:
            return print("Нотаток за таким тегом не знайдено")
        return print(NoteData.table(matches))
                
        

class Note:
    note_counter = 0

    def __init__(self, info:str):
        Note.note_counter += 1
        self.note_id = Note.note_counter 
        self.tags = []
        self.info = info
        
        
    def table(self) -> str:
        header = [f'              Note ID: {self.note_id}']


        field_1 = ['Tags',]
        text_block = ''
        for tag in self.tags:
            text_block += "> " + tag + "\n"
        
        field_1.append(text_block)

        field_2 = ['Info', ]
        width_of_string = 0

        lst_for_info = [] 

        while width_of_string < len(self.info):
            lst_for_info.append(self.info[width_of_string: width_of_string + 70])
            width_of_string += 70
        
        info = "\n".join(lst_for_info)
        field_2.append(info)

        table = tabulate([field_1, field_2], headers=header, tablefmt='grid' )
        
        return str(table)


class NoteData(UserDict):
    def __init__(self, data=None):
        super().__init__()
        if not data is None:
            self.data = data
        self.load_data()

    @staticmethod
    def table(data):
        headers = ["Note ID", "Tags", "Info"]
        fields = []

        for note in data.values():
            tag_block = ''
            for tag in note.tags:
                
                tag_block += "> " + tag + "\n"

            info_block = note.info[:40] + "\n" + "..."
            field = [note.note_id, tag_block, info_block]

            fields.append(field)
        
        table = tabulate(fields, headers=headers, tablefmt='grid')
        return str(table)
    
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
    
    def __str__(self):
        return self.table(self.data)
