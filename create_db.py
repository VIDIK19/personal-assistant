import sqlite3
import os

# Визначаємо шлях до папки database
db_directory = 'database'
db_filename = 'contacts.db'
db_path = os.path.join(db_directory, db_filename)

# Переконуємося, що папка існує
if not os.path.exists(db_directory):
    os.makedirs(db_directory)

# Створюємо або відкриваємо базу даних
conn = sqlite3.connect(db_path)

# Створюємо таблицю контактів, якщо вона ще не існує
conn.execute('''CREATE TABLE IF NOT EXISTS contacts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    phone TEXT NOT NULL,
                    email TEXT NOT NULL,
                    birthday DATE NOT NULL
                );''')

# Закриваємо з'єднання з базою даних
conn.close()

print(f"База даних створена за шляхом: {db_path}")

