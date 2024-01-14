import re
import sqlite3
from collections import UserDict
from datetime import datetime

class ContactManager(UserDict):
    def __init__(self, db_file='database/contacts.db'):
        super().__init__()
        self.db_file = db_file
        self._create_table()
        self._load_from_db()

    def _create_table(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS contacts (
                name TEXT PRIMARY KEY,
                phones TEXT,
                email TEXT,
                birthday TEXT
            )
        ''')

        conn.commit()
        conn.close()

    def _save_to_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        for record in self.data.values():
            phones = ', '.join(str(phone) for phone in record.phones) if record.phones else None
            email = record.email.value if record.email else None
            birthday = record.birthday.value if record.birthday else None

            cursor.execute('''
                INSERT OR REPLACE INTO contacts (name, phones, email, birthday)
                VALUES (?, ?, ?, ?)
            ''', (record.name.value, phones, email, birthday))

        conn.commit()
        conn.close()

    def _load_from_db(self):
        conn = sqlite3.connect(self.db_file)
        cursor = conn.cursor()

        cursor.execute('SELECT * FROM contacts')
        rows = cursor.fetchall()

        for row in rows:
            name, phones, email, birthday = row
            phones = phones.split(', ') if phones else []
            email = Email(email) if email else None
            birthday = Birthday(birthday) if birthday else None

            contact = Record(name, email=email, birthday=birthday)
            contact.phones = [Phone(phone) for phone in phones]

            self.data[name] = contact

        conn.close()

    def add_record(self, record):
        self.__setitem__(record.name.value, record)
        self._save_to_db()

    def delete(self, name):
        super().delete(name)
        self._save_to_db()

    def load_from_file(self, file_name):
        super().load_from_file(file_name)
        self._save_to_db()

    def display_birthdays_in_period(self, days):
        today = datetime.now().date()

        for record in self.data.values():
            days_to_birthday = record.days_to_birthday()

            if days_to_birthday is not None and 0 <= days_to_birthday <= days:
                print(f"Contact '{record.name.value}' has a birthday in {days_to_birthday} days:")
                print(record)
                print("-" * 30)

    def search(self, value):
        results = []
        for record in self.data.values():
            if value.lower() in record.name.value.lower():
                results.append(record)
            for phone in record.phones:
                if value in phone.value:
                    results.append(record)
                    break
        return results


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
        if not self.is_valid_name(value):
            raise ValueError("Name must be at least one character long")
        super().__init__(value)

    @staticmethod
    def is_valid_name(value):
        return len(value.strip()) > 0


class Phone(Field):
    def __init__(self, value):
        if len(value) != 10 or not value.isdigit():
            raise ValueError("Phone number must contain 10 digits.")
        super().__init__(value)


class Email(Field):
    @classmethod
    def is_valid(cls, value):
        try:
            if re.match(r'[a-zA-Z][\w.]+@\w{2,}\.\w{2,3}', value) or value == '':
                return True
        except ValueError:
            return False

    def __init__(self, value=''):
        if not self.is_valid(value):
            print("Incorrect email! Please provide correct email.")
            raise ValueError("Not valid email")
        super().__init__(value)


class Birthday(Field):
    def __init__(self, value):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except ValueError:
            raise ValueError("Incorrect data format, should be YYYY-MM-DD")
        super().__init__(value)

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        try:
            datetime.strptime(new_value, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Incorrect date format, should be YYYY-MM-DD")
        self._value = new_value


class Record:
    def __init__(self, name, phones=None, email=None, birthday=None):
        self.name = Name(name)
        self.phones = [Phone(phone) for phone in (phones or [])]
        self.email = Email(email) if email else None
        self.birthday = Birthday(birthday) if birthday else None

    def add_phone(self, phone):
        new_phone = Phone(phone)
        self.phones.append(new_phone)

    def remove_phone(self, phone):
        for p in self.phones:
            if str(p) == phone:
                self.phones.remove(p)
                break

    def edit_phone(self, old_phone, new_phone):
        phone_exists = False
        for p in self.phones:
            if str(p) == old_phone:
                p.value = new_phone
                phone_exists = True
                break

        if not phone_exists:
            raise ValueError(f"Phone number '{old_phone}' does not exist in this record.")

    def find_phone(self, phone_number):
        for p in self.phones:
            if str(p) == phone_number:
                return p
        return None

    def edit_record(self, name, new_name=None, new_birthday=None, new_phones=None, new_email=None):
        if name in self.data:
            record = self.data[name]

            if new_name:
                record.name.value = new_name

            if new_birthday:
                record.birthday.value = new_birthday

            if new_phones:
                record.phones = [Phone(phone) for phone in new_phones]

            if new_email:
                record.email.value = new_email

            print(f"Contact '{name}' has been successfully edited.")
        else:
            print(f"The record '{name}' does not exist in the address book.")

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

    def __str__(self):
        return f"Contact name: {self.name}, phones: {'; '.join(str(p) for p in self.phones)}"
