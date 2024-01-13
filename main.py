import argparse
from src.contact_manager import ContactManager
from src.file_manager import FileManager
from src.note_manager import NoteManager
from pathlib import Path

def main():
    parser = argparse.ArgumentParser(description="Персональний помічник")
    subparsers = parser.add_subparsers(dest='command')

    # Підпарсер для contact_manager
    contact_parser = subparsers.add_parser('contact', help='Керування контактами')
    contact_subparsers = contact_parser.add_subparsers(dest='contact_command')
    
    # Додавання нового контакту
    add_contact_parser = contact_subparsers.add_parser('add', help='Додати новий контакт')
    add_contact_parser.add_argument('name', type=str, help="Ім'я контакту")
    add_contact_parser.add_argument('phone', type=str, help="Номер телефону контакту")
    add_contact_parser.add_argument('email', type=str, help="Email контакту")
    add_contact_parser.add_argument('birthday', type=str, help="Дата народження контакту (формат: РРРР-ММ-ДД)")

    # Пошук контакту
    search_contact_parser = contact_subparsers.add_parser('search', help='Пошук контакту за іменем')
    search_contact_parser.add_argument('name', type=str, help="Ім'я контакту для пошуку")

    # Підпарсер для file_manager
    file_parser = subparsers.add_parser('file', help='Керування файлами')
    file_parser.add_argument('path', type=str, help="Шлях до папки для сортування файлів")

    # Підпарсер для note_manager
    note_parser = subparsers.add_parser('note', help='Керування нотатками')
    # Тут можна додати команди та аргументи для note_manager

    args = parser.parse_args()

    if args.command == 'contact':
        contact_manager = ContactManager('database/contacts.db')
        if args.contact_command == 'add':
            contact_manager.add_contact(args.name, args.phone, args.email, args.birthday)
            print(f"Контакт {args.name} додано.")
        elif args.contact_command == 'search':
            contacts = contact_manager.search_contact(args.name)
            for contact in contacts:
                print(contact)
    
    elif args.command == 'file':
        file_manager = FileManager()
        file_manager.sort_folder(Path(args.path))
        print(f"Файли у папці {args.path} відсортовано.")

    # Тут можна додати логіку для note_manager
    
if __name__ == '__main__':
    main()


