import unittest
import sqlite3
import os
import sys

sys.path.append('d:/personal-assistant')
from src.contact_manager import ContactManager

class TestContactManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.db_path = 'test_contacts.db'
        cls.conn = sqlite3.connect(cls.db_path)
        cls.conn.execute("DROP TABLE IF EXISTS contacts")
        cls.conn.execute('''CREATE TABLE contacts (
                            id INTEGER PRIMARY KEY AUTOINCREMENT,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT NOT NULL,
                            birthday DATE NOT NULL
                        );''')
        cls.conn.close()

    def setUp(self):
        self.conn = sqlite3.connect(self.db_path)
        self.manager = ContactManager(self.db_path)

    def tearDown(self):
        self.conn.close()

    @classmethod
    def tearDownClass(cls):
        try:
            os.remove(cls.db_path)
        except PermissionError as e:
            print(f"Не вдалося видалити тестову базу даних: {e}")

    def test_add_and_search_contact(self):
        self.manager.add_contact("Іван Іваненко", "123-456-7890", "ivan@example.com", "1990-01-01")
        result = self.manager.search_contact("Іван")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0][1], "Іван Іваненко")

if __name__ == '__main__':
    unittest.main()

