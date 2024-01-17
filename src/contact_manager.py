import re
import os
from collections import UserDict
from datetime import datetime, timedelta
import pickle
import sqlite3
from tabulate import tabulate

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
DATA_PATH = f'{project_root}\database\\contacts.db'

class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)
    
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

class Name(Field):
    def __init__(self, value):
        super().__init__(value)

    @staticmethod
    def is_valid_name(value):
        """return boolean from check"""
        return len(value.strip()) > 0

class Phone(Field):
    @staticmethod
    def is_valid_phone(value):
        """Повертає булеве значення з перевірки"""
        return value.isdigit() and len(value) == 10

    def __init__(self, value):
        if not Phone.is_valid_phone(value):
            raise ValueError("Номер телефону повинен бути десятизначним рядком із цифр")
        super().__init__(value)

    def __set__(self, instance, value):
        if not Phone.is_valid_phone(value):
            raise ValueError("Номер телефону повинен бути десятизначним рядком із цифр")
        super().__set__(instance, value)


class Email(Field):
    @classmethod
    def is_valid(cls, value):
        try:
            if re.match(r'[a-zA-Z][\w.]+@\w{2,}\.\w{2,3}', value) or value == '':
                return True
        except ValueError:
            return False

    def __init__(self, value=''):
        if not Email.is_valid(value):
            print(f'Некоректна електронна пошта! Будь ласка, введіть правильну електронну адресу.')
            raise ValueError(f'Не дійсна електронна адреса')
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Неправильний формат даних, повинно бути YYYY-MM-DD")
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Неправильний формат дати, повинно бути YYYY-MM-DD")
        self._value = new_value

latest_id = 0

class Record:
   
    def __init__(self, name, birthday=None):
        global latest_id  # Use the global variable
        latest_id += 1  # Increment the latest_id for each new contact
        self.id = latest_id
        self.name = Name(name)
        self.phones = []
        self.emails = []
        self.birthday = Birthday(birthday) if birthday else None

    # def set_id(self, contact_id):
        
    #     self.id = contact_id

    # Додає номер телефону до запису
    def add_phone(self, phone):
        if phone.isdigit() and len(phone) == 10:
            new_phone = Phone(phone)
            self.phones.append(new_phone)
        else:
            print(f"Некоректний номер телефону: {phone}. Номер телефону повинен містити 10 цифр.")

    # Видаляє номер телефону з запису
    def remove_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                break

    #  Редагує існуючий номер телефону в записі
    def edit_phone(self, old_phone, new_phone):
        phone_exists = False
        for i, p in enumerate(self.phones):
            if str(p) == old_phone:
            # Видаляє старий номер телефону
                del self.phones[i]
            # Додає новий номер телефону
                self.add_phone(new_phone)
                phone_exists = True
                break

        if not phone_exists:
            raise ValueError(f"Номер телефону '{old_phone}' не існує в цьому записі.")

    # Знаходить номер телефону в записі
    def find_phone(self, phone_number):
        for p in self.phones:
            if str(p) == phone_number:
                return p  # Повертає значення номеру телефону
        return None  # Повертає None, якщо номер не знайдено
    
    # Додає електронну адресу до запису
    def add_email(self, email):
        new_email = Email(email)
        self.emails.append(new_email)

    # Редагує існуючу електронну адресу в записі
    def edit_email(self, old_email, new_email):
    # Знаходить індекс старої електронної адреси
        index_of_old_email = next((i for i, email in enumerate(self.emails) if str(email) == old_email), None)

        if index_of_old_email is not None:
        # Якщо стара електронна адреса знайдена
            new_email_object = Email(new_email)
            self.emails[index_of_old_email] = new_email_object
        else:
        # Якщо стара електронна адреса не знайдена, викидає помилку
            raise ValueError(f"Електронна адреса '{old_email}' не існує в цьому записі.")

    # Підраховує кількість днів до дня народження
    def days_to_birthday(self):
        if self.birthday:
            today = datetime.now().date()
            birthday_date = datetime.strptime(self.birthday.value, "%Y-%m-%d").date()

            next_birthday_year = today.year
            if (today.month, today.day) > (birthday_date.month, birthday_date.day):
                next_birthday_year += 1

            birthday_date = birthday_date.replace(year=next_birthday_year)
            days_to_birthday = (birthday_date - today).days
            return days_to_birthday
        else:
            return None
    
    # Рядкове представлення запису
    def __str__(self):
        phones_str = '; '.join(str(phone) for phone in self.phones)
        emails_str = '; '.join(str(email) for email in self.emails)
        birthday_str = f", день народження: {self.birthday.value}" if self.birthday else ""
        return f"Ім'я контакту: {self.name}, телефони: {phones_str}, електронні адреси: {emails_str}{birthday_str}"


# Клас AddressBook, що розширює UserDict для управління записами
class AddressBook(UserDict):
    # Додає запис до адресної книги
    def add_record(self, record):
        self.data[record.name.value] = record

    # Знаходить запис за ім'ям в адресній книзі
    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        name_lower = name.lower().strip()
        if name_lower in self.data:
            del self.data[name]
        else:
            print(f"Запис '{name}' не існує в адресній книзі.")

    def __iter__(self, chunk_size=5):
        records = list(self.data.values())  # Список всіх записів
        current = 0

        while current < len(records):
            yield records[current : current + chunk_size]  # Повертає N записів
            current += chunk_size

    # Зберігає дані у файл за допомогою серіалізації pickle
    def save_to_file(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self.data, fh)

    # Завантажує дані з файлу за допомогою десеріалізації pickle
    def load_from_file(self, file_name):   
        with open(file_name, 'rb') as fh:
            self.data = pickle.load(fh)

    # Пошук записів за значенням у імені або номері телефону
    def search(self, value):
        results = []
        for record in self.data.values():
            # Перевіряє, чи значення співпадає в імені (без врахування регістру)
            if value.lower() in record.name.value.lower():
                results.append(record)
            # Перевіряє, чи значення співпадає в будь-якому номері телефону
            for phone in record.phones:
                if value in phone.value:
                    results.append(record)
                    break  # Зупиняється після знаходження відповідності в телефонах, щоб уникнути дублікатів
        return results
    
    def show_all_data(self):
        table_data = []
        for record in self.data.values():
            phones_str = '; '.join(str(phone) for phone in record.phones)
            emails_str = '; '.join(str(email) for email in record.emails)
            birthday_str = record.birthday.value if record.birthday else ""
            table_data.append([record.name.value, phones_str, emails_str, birthday_str])

        headers = ["Ім'я", "Номери телефонів", "Електронна пошта", "День народження"]
        table_str = tabulate(table_data, headers, tablefmt="grid", colalign=("center", "center", "center", "center"))
        print(table_str)
  

class AddressBookDatabase:
    @staticmethod
    def create_table():
        connection = sqlite3.connect(DATA_PATH)
        cursor = connection.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                birthday DATE,
                phone TEXT,
                email TEXT
            )
        ''')
        connection.commit()
        connection.close()

    @staticmethod
    def insert_records(records):
        connection = sqlite3.connect(DATA_PATH)
        cursor = connection.cursor()

        for record in records:
            existing_record = AddressBookDatabase.retrieve_record_by_name(cursor, record.name.value)

            if existing_record:
                # If a record with the same name already exists, update the existing record
                cursor.execute('''
                    UPDATE contacts
                    SET name=?, birthday=?, phone=?, email=?
                    WHERE id=?
                ''', (record.name.value,
                      record.birthday.value if record.birthday else None,
                      ";".join(str(phone) for phone in record.phones if phone.value),  # Exclude empty phone numbers
                      ";".join(str(email) for email in record.emails),
                      existing_record[0]))  # Use the existing record's ID
            else:
                # If no record with the same name exists, insert a new record
                cursor.execute('''
                    INSERT INTO contacts (name, birthday, phone, email)
                    VALUES (?, ?, ?, ?)
                ''', (record.name.value,
                      record.birthday.value if record.birthday else None,
                      ";".join(str(phone) for phone in record.phones if phone.value),  # Exclude empty phone numbers
                      ";".join(str(email) for email in record.emails)))

        connection.commit()
        connection.close()

    @staticmethod
    def edit_phone(name, old_phone, new_phone):
        connection = sqlite3.connect(DATA_PATH)
        cursor = connection.cursor()

        cursor.execute('SELECT * FROM contacts WHERE name=?', (name,))
        record = cursor.fetchone()

        if record:
        # Отримує список існуючих номерів телефонів та розбиває його
            existing_phones = record[2].split("; ")
        
        # Перевіряє, чи старий номер телефону існує у списку
            if old_phone in existing_phones:
            # Видаляє старий номер телефону
                existing_phones.remove(old_phone)
            # Додає новий номер телефону
                existing_phones.append(new_phone)
            
            # Оновлює базу даних з новим списком номерів телефонів
                cursor.execute('UPDATE contacts SET phone=? WHERE name=?', ("; ".join(existing_phones), name))
                connection.commit()
            else:
                print(f"Номер телефону '{old_phone}' не знайдено для контакту '{name}'.")
        else:
            print(f"Контакт '{name}' не знайдено в базі даних.")

        connection.close()

    @staticmethod
    def retrieve_record_by_name(cursor, name):
        cursor.execute('''
            SELECT * FROM contacts
            WHERE name=?
        ''', (name,))
        return cursor.fetchone()

    @staticmethod
    def retrieve_records():
        connection = sqlite3.connect(DATA_PATH)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM contacts")
        rows = cursor.fetchall()
        connection.close()
        return rows
    
    
class ContactManager:
    def __init__(self, db_path=f'{project_root}\database\\contacts.db'):
        self.db_path = db_path
        self.connection = sqlite3.connect(self.db_path)
        self.cursor = self.connection.cursor()
        self.address_book = AddressBook()
        # self.records = {}

    def execute_query(self, query, parameters=None, get_id=False):
        self.cursor.execute(query, parameters) if parameters else self.cursor.execute(query)
        self.connection.commit()

        if get_id:
            return self.cursor.lastrowid
        else:
            return self.cursor.fetchall()
    
    def add_record(self, record):
        self.address_book.add_record(record)

    # def add_contact(self, record):
        # query = "INSERT INTO contacts (record_id, name, birthday, phones, emails) VALUES (?, ?, ?, ?)"
        # parameters = (record.name.value, record.birthday.value, "; ".join(record.phones), "; ".join(record.emails))
        # record_id = self.execute_query(query, parameters, get_id=True)
        # record.set_id(record_id)
    
    def add_contact(self, name, phone, email, birthday):
        new_contact = Record(name, birthday)
        new_contact.add_phone(phone)
        new_contact.add_email(email)
        self.address_book.add_record(new_contact)
        self.insert_records()

    def update_contact(self, record):
        query = "UPDATE contacts SET name=?, birthday=?, phones=?, emails=? WHERE id=?"
        parameters = (record.name.value, record.birthday.value, "; ".join(record.phones), "; ".join(record.emails), record.id)
        self.execute_query(query, parameters)

    def generate_contact_id(self):
        # Генерування унікального ID для контакту, використовуючи логіку зберігання
        # поточного максимального ID та додавання 1 до нього.
        if not self.contacts:
            return 1
        max_id = max(contact.id for contact in self.contacts)
        return max_id + 1
    
    def add_name(self, name:str):
        record = Record(name)
        self.add_name(record)

    def add_record(self, record):
        self.address_book.add_record(record)

    def edit_contact_phone(self, name, old_phone, new_phone):
        self.address_book.data[name].edit_phone(old_phone, new_phone)
        self.insert_records()


    def edit_contact_email(self, name, old_email, new_email):
        try:
            self.address_book.data[name].edit_email(old_email, new_email)
            # self.insert_records()
        except ValueError as e:
            print(f"Помилка редагування електронної адреси: {e}")
        self.insert_records()
        
        
    def find(self, name):
        name = name.lower().strip()  # відсікаємо пробіли та переводимо в нижній регістр
        for record in self.records.values():
            if record.name.lower().strip() == name:
                return record
        return None

    def delete_contact(self, name):
        # Видалення контакту з адресної книги
        self.address_book.delete(name)
        # Оновлення бази даних після видалення
        self.insert_records()
  
    def search_contact(self, name):
        results = []
        for record in self.address_book.data.values():
            if name.lower() in record.name.value.lower():
                results.append(str(record))
        return results

    def create_table(self):
        AddressBookDatabase.create_table()

    def insert_records(self):
        AddressBookDatabase.insert_records(self.address_book.data.values())

    def retrieve_records(self):
        return AddressBookDatabase.retrieve_records()
    
    def clear_data(self):
        AddressBookDatabase.clear_table()
    
    def upcoming_birthdays(self, days=7):
        days_input = input("Період найближчих днів народжень у днях: ")
        try:
            days = int(days_input)
        except ValueError:
            print("Неправильний формат числа. Використано значення за замовчуванням (7 днів).")
        query = "SELECT * FROM contacts WHERE strftime('%m-%d', birthday) BETWEEN strftime('%m-%d', date('now')) AND strftime('%m-%d', date('now', ?))"
        parameters = (f'{days} days', )
        result = self.execute_query(query, parameters)
        return result
    
    def display_upcoming_birthdays(self):
        upcoming_birthdays_records = self.upcoming_birthdays()
        print("\nКонтакти з наближеними днями народженнями:")
        if upcoming_birthdays_records:
            self.display_records(upcoming_birthdays_records)
        else:
            print("Немає контактів з найближчими днями народження.")

    def display_records(self, records):
        # Форматування та виведення таблиці
        table_data = []
        for row in records:
            record_id, name, birthday, phones, emails = row
            record = Record(name, birthday)
            # Обробка номерів телефонів і електронних адрес
            phones = phones.split("; ")
            emails = emails.split("; ")

            for phone in phones:
                record.add_phone(phone)
            for email in emails:
                record.add_email(email)
