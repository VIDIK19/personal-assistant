from src.note_manager import NoteManager
from src.contact_manager import ContactManager
from src.file_manager import sort_folder
from pathlib import Path

def main():
    note_manager = NoteManager()
    contact_manager = ContactManager()

    contact_manager.create_table()

    while True:
        user_input = input(">>>")

        # створення списку слів із юзер-інпута
        lst_of_args = user_input.lower().strip().split(" ")

        # перше слово з юзер інпута - команда, наступні слова - аргументи
        command = lst_of_args[0]

        if command == "":
            continue

        # завершення програми
        if command == "exit":
            break

        try:
            command_arg = lst_of_args[1]
            # Обробка випадку коли користувач не ввів аргумент для command

        except IndexError:
            print("Команду для мендежеру не передано")
            continue

        if command == "note":
            if command_arg == "create":
                # Запрашуємо ввести текст нотатки
                info = input(">>>Введіть текст нотатки:")
                # Додає нотатку в БД
                note_manager.add_note(info)
                print("Нотатку зроблено")
                note_manager.show_data()

            elif command_arg == "add_tag":
                # Запрашуємо id нотатки
                note_id = input(">>>Введіть ID нотатки, до якої хочете додати тег:")
                # Запрашуємо тег
                tag = input(">>>Введіть тег:")
                # Додаємо тег в нотатку
                note_manager.add_tag(int(note_id), tag)
                print("Тег додано")
                note_manager.show_data()

            elif command_arg == "data":
                note_manager.show_data()

            elif command_arg == "clear":
                print("Ви впевнені, що хочете видалити всі нотатки? Напишіть (yes/так)")
                user_input_1 = input(">>>")
                if user_input_1 in ("yes", "так"):
                    note_manager.clear_data()
                    print("Всі нотатки видалено")
                    note_manager.show_data()

            elif command_arg == "edit":
                print("Виберіть нотатку для редагування")
                note_id = int(input(">>>ID нотатки:"))
                note_manager.open_note(note_id)
                print("Що хочете відредагувати? (info/tag)")
                user_choice = input(">>>")
                if user_choice == "info":
                    new_info = input(">>>Новий текст нотатки:")
                    note_manager.edit_info(note_id, new_info)
                elif user_choice == "tag":
                    tag_index = int(
                        input(">>>Введіть індекс тегу для редагування (з верху від 0):")
                    )
                    new_tag = input(">>>Нова назва тегу:")
                    note_manager.edit_tag(note_id, tag_index, new_tag)
                else:
                    continue
                print("Нотатку відредаговано")
                note_manager.open_note(note_id)

            elif command_arg == "open":
                note_manager.show_data()
                print("Виберіть нотатку (ID)")
                note_id = int(input(">>>"))
                note_manager.open_note(note_id)

            elif command_arg == "search":
                print("Впишіть тег для пошуку нотаток (можна перші літери)")
                note_tag = input(">>>")
                note_manager.search_tag(note_tag)

            else:
                print("Нема такої команди для менеджеру нотаток")

        elif command == 'contact':           
            if command_arg == 'add':
                name = input("Ім'я контакту: ")
                phone = input("Номер телефону контакту: ")
                email = input("Email контакту: ")
                birthday = input("Дата народження контакту (формат: РРРР-ММ-ДД): ")
                contact_manager.add_contact(name, phone, email, birthday)
                print(f"Контакт {name} додано.")

            elif command_arg == 'edit_phone':
                name = input("Ім'я контакту для редагування номера телефону: ")
                old_phone = input("Старий номер телефону: ")
                new_phone = input("Новий номер телефону: ")

                try:
                    contact_manager.edit_phone(name, old_phone, new_phone)
                    print(f"Номер телефону '{old_phone}' в контакту '{name}' відредаговано на '{new_phone}'.")
                except ValueError as e:
                    print(f"Помилка: {e}")

            elif command_arg == 'edit_email':
                name = input("Ім'я контакту для редагування email: ")
                old_email = input("Старий email: ")
                new_email = input("Новий email: ")
                record = contact_manager.find(name)  
                if record:
                    contact_manager.edit_email(record, old_email, new_email)
                else:
                    print(f"Контакт з ім'ям {name} не знайдено.")
 
            elif command_arg == 'search':
                name = input("Ім'я контакту для пошуку: ")
                contacts = contact_manager.search_contact(name)
                for contact in contacts:
                    print(contact)

            elif command_arg == 'show_all_data':
                records = contact_manager.retrieve_records()
                if not records:
                    print("Немає даних для відображення.")
                else:
                    contact_manager.display_records(records)

            elif command_arg == 'del_contact':
                name_to_delete = input("Введіть ім'я користувача, дані якого потрібно видалити: ")
                contact_manager.delete_contact(name_to_delete)
                print(f"Контакт {name_to_delete} видалено.")

            else: 
                print('Нема такої команди для менеджера контактів')

        
        elif command == "file":
            if command_arg == 'sort_folder':
                print('Введіть шлях до папки:')
                path_str = input(">>>")
                path = Path(path_str)
                
                if path.exists() and path.is_dir():
                    sort_folder(path)
                    print('Файли відсортовано')
                else:
                    print(f'Папки за шляхом {path_str} не існує або це не папка.')
            else: 
                print('Нема такої команди для менеджера файлів')
        else:
            print("Нема такого менеджера")
        # Це маленька чатсина функціоналу - просто приклад
        
        


if __name__ == "__main__":
    main()
