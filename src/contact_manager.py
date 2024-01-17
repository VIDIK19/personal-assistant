from collections import UserDict
from tabulate import tabulate
from datetime import datetime
import re
import os
import pickle


current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
DATA_PATH = f'{project_root}\database\contacts.pkl'






class PhoneError(Exception):
    pass

class BirthdayError(Exception):
    pass

class EmailError(Exception):
    pass



class Name:
    def __init__(self, name:str):
        self.value = name


class Phone:
    def __init__(self, phone:int):
        if Phone.is_valid_phone(phone):
            self.value = phone
        else:
            raise PhoneError
        
    @staticmethod
    def is_valid_phone(value):
        return value.isdigit() and len(value) == 10



class Birthday:
    def __init__(self, birthday:str):
        try:
            datetime.strptime(birthday, "%Y-%m-%d")
            self.value = birthday
        except ValueError:
            raise BirthdayError

    def __str__(self):
        return self.value

class Email:
    def __init__(self, email:str):
        if Email.is_valid(email):
            self.value = email
        else:
            raise EmailError

    @staticmethod
    def is_valid(value):
        if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', value) or value == '':
            return True
        return False

    def __str__(self):
        return self.value
    
class Record:
    record_counter = 0
    def __init__(self, name:Name, phone:Phone, email:Email=None, birthday:Birthday=None):
        Record.record_counter += 1
        self.record_id = self.record_counter
        self.name = name
        self.phones = [phone, ]
        self.emails = [email, ]
        self.birthday = birthday 

class ContactData(UserDict):
    def __init__(self, data=None):
        super().__init__()
        if not data is None:
            self.data = data
        self.load_data()

    @staticmethod
    def table(data:dict):
        headers = ["ID", "Name", "Emails", "Phones", "Birthday"]
        fields = []


        for record in data.values():
            email_block = ''
            phone_block = ''
            for email in record.emails:
                if email != None:
                    email_block += f'> {str(email)} \n'
            for phone in record.phones:
                phone_block += f'> {phone.value} \n'
            if record.birthday != None:
                birthday_block = str(record.birthday)
            else:
                birthday_block = ''
            
            field = [record.record_id, record.name.value, email_block, phone_block, birthday_block]

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
                    Record.record_counter = list(self.data.keys())[-1]
                else:
                    Record.record_counter = 0
        except FileNotFoundError:
            self.data = {}

    def clear_data(self):
        self.data = {}
        self.save_data()


class ContactManager:
    def __init__(self):
        self.data = ContactData()

    def add_record(self, record:Record):
        self.data.data[record.record_id] = record
        self.data.save_data()

    def show_data(self):
        print(ContactData.table(self.data.data))
        
    def clear_data(self):
        self.data.clear_data()
        self.data.save_data()
    
    def delete_record(self, record_id):
        del self.data[record_id] 
        
        
    def show_record(self, record_id):
        record_dict = {}
        record_dict[record_id] = self.data.data[record_id]
        print(ContactData.table(record_dict))

    def delete_phone(self, record_id:int, phone_ind:int):
        del self.data.data[record_id].phones[phone_ind]
        
    def add_phone(self, record_id:int, phone:Phone):
        self.data.data[record_id].phones.append(phone)

    def edit_birthday(self, record_id:int, new_birthday:Birthday):
        self.data.data[record_id].birthday = new_birthday

    def delete_email(self,record_id:int, email_index:int):
        del self.data.data[record_id].emails[email_index]
    
    def add_email(self, record_id:int, new_email:Email):
        self.data.data[record_id].emails.append(new_email)

    def name_search(self, search_name:str):
        matches = {}
        for record in self.data.data.values():
            if record.name.value.startswith(search_name):
                matches[record.record_id] = record
        print(ContactData.table(matches))
