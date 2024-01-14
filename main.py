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
    note_subparsers = note_parser.add_subparsers(dest='note_command')

    # Додавання нової нотатки
    create_note_parser = note_subparsers.add_parser('create', help='Додати нову нотатку')
    create_note_parser.add_argument('info', type=str, help='Текст нотатки')

    # Відкриття нотатки 
    open_note_parser = note_subparsers.add_parser('open', help="Відкрити нотатки")
    open_note_parser.add_argument('note_id', type=int, help='ID нотатки')

    # Додавання тегу
    add_tag_note_parser = note_subparsers.add_parser('add_tag', help='Додавання тегу')
    add_tag_note_parser.add_argument('note_id', type=int, help="ID нотатки")
    add_tag_note_parser.add_argument('tag', type=str, help='Назва тегу')

    # Редагування тегу нотатки
    edit_tag_note_parser = note_subparsers.add_parser('edit_tag', help='Редагування тегу' )
    edit_tag_note_parser.add_argument('note_id', type=int, help='ID нотатки')
    edit_tag_note_parser.add_argument('tag_index', type=int, help='Індекс тегу для редагування (від 0 з верху)')
    edit_tag_note_parser.add_argument('new_tag', type=str, help='Нова назва тегу')

    # Редагування тексту нотатки 
    edit_info_note_parser = note_subparsers.add_parser('edit_info', help='Редагування тексту нотатки')
    edit_info_note_parser.add_argument('note_id', type=int, help='ID нотатки')
    edit_info_note_parser.add_argument('new_info', type=str, help='Новий текст нотатки')

    # Показ БД нотаток
    show_all_note_parser = note_subparsers.add_parser('show_all', help='Показати всі нотатки')

    # Видалення нотатки
    delete_note_parser = note_subparsers.add_parser('delete', help='Видаляє нотатку')
    delete_note_parser.add_argument('note_id', type=int, help='ID нотатки')

    # Пошук за тегом нотатки
    search_note_parser = note_subparsers.add_parser('search', help='Пошук нотатки за тегом')
    search_note_parser.add_argument('tag', type=str, help='Перші літери тегу нотатки')


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

    elif args.command == 'note':
        note_manager = NoteManager()
        if args.note_command == 'create':
            note_manager.add_note(args.info)
            print('Нотатку створено')
            note_manager.show_data()
        elif args.note_command == 'open':
            note_manager.open_note(args.note_id)
        elif args.note_command == 'add_tag':
            note_manager.add_tag(args.note_id, args.tag)
            print('Тег додано')
            note_manager.show_data()
        elif args.note_command == 'edit_tag':
            note_manager.edit_tag(args.note_id, args.tag_index, args.new_tag)
            print('Тег змінено')
            note_manager.show_data()
        elif args.note_command == 'edit_info':
            note_manager.edit_info(args.note_id, args.new_info)
            print('Текст нотатки змінено')
            note_manager.open_note(args.note_id)
        elif args.note_command == 'show_all':
            note_manager.show_data()
        elif args.note_command == 'delete':
            note_manager.delete_note(args.note_id)
            print('Нотатку видалено')
            note_manager.show_data()
        elif args.note_command == 'search':
            note_manager.search_tag(args.tag)


            


        


    
if __name__ == '__main__':
    main()


