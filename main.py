from src.note_manager import NoteManager
from src.contact_manager import ContactManager, Name, Email, Phone, Birthday, PhoneError, BirthdayError, EmailError, Record
from src.file_manager import sort_folder
from pathlib import Path

def main():
    note_manager = NoteManager()
    contact_manager = ContactManager()

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
            print("Bye!")

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
                while True:
                    # Запрашуємо id нотатки
                    note_id = int(input(">>>Введіть ID нотатки, до якої хочете додати тег:"))
                    if not note_id in note_manager.data.data.keys():
                        print("Нотатки за таким ID не існує")
                        continue
                    # Запрашуємо тег
                    tag = input(">>>Введіть тег:")
                    # Додаємо тег в нотатку
                    note_manager.add_tag(note_id, tag)
                    print("Тег додано")
                    note_manager.show_data()
                    break

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
                while True:
                    note_manager.show_data()
                    print("Виберіть нотатку для редагування")
                    note_id = int(input(">>>ID нотатки:"))
                    if not note_id in note_manager.data.data.keys():
                        print("Нотатки за таким ID не існує")
                        continue
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
                        if not tag_index in range(0, len(note_manager.data.data[note_id].tags)):
                            print("Не існує тегу за таким індексом")
                            continue
                        new_tag = input(">>>Нова назва тегу:")
                        note_manager.edit_tag(note_id, tag_index, new_tag)
                    else:
                        break
                    print("Нотатку відредаговано")
                    note_manager.open_note(note_id)
                    break

            elif command_arg == "open":
                note_manager.show_data()
                while True:
                    print("Виберіть нотатку (ID)")
                    note_id = int(input(">>>"))
                    if not note_id in note_manager.data.data.keys():
                        print("Нотатки за таким ID не існує")
                        continue
                    note_manager.open_note(note_id)
                    break

            elif command_arg == "search":
                print("Впишіть тег для пошуку нотаток (можна перші літери)")
                note_tag = input(">>>")
                note_manager.search_tag(note_tag)

            else:
                print("Нема такої команди для менеджеру нотаток")

        elif command == 'contact':           
            if command_arg == 'add':
                print("Впишіть ім'я контакту")
                name = input(">>>")
                name = Name(name)
                phone = None
                email = None
                birthday = None
                print("Впишіть телефон контакту")
                while True:
                    try:
                        phone = input('>>>')
                        phone = Phone(phone)
                        break
                    except PhoneError:
                        print("Телефон має бути десятизначним та повністю із цифр")
                        continue
                print('Впишіть email контакту (опціонально)')
                while True:
                    try:
                        email = input(">>>")
                        if email == '':
                            break
                        email = Email(email)
                        break
                    except EmailError:
                        print('Недійсна електронна пошта, спробуйте ще')
                        continue
                print('Впишіть день народження (опціонально)')
                while True:
                    try:
                        birthday = input('>>>')
                        if birthday == '':
                            break
                        birthday = Birthday(birthday)
                        break
                    except BirthdayError:
                        print('Недійсний формат дня народження, треба YYYY-MM-DD')
                record = Record(name, phone, email, birthday)
                contact_manager.add_record(record)
                contact_manager.show_data()
            elif command_arg == 'show_data':
                contact_manager.show_data()

            elif command_arg == 'clear':
                print('Ви впевнені, що хочете очистити список ВСІХ контактів? (yes/так)')
                qst = input('>>>')
                if qst == "yes":
                    contact_manager.clear_data()

            elif command_arg == 'delete':
                contact_manager.show_data()
                print('Який контакт бажаєте видалити? (Впишіть ID)')
                while True:
                    record_id = input('>>>')
                    try:
                        contact_manager.delete_record(int(record_id))
                        print("Контакт видалено.")
                        break
                    except KeyError:
                        print("Контакту за таким ID немаєю")
                        continue
            elif command_arg == 'edit':
                while True:
                    print('Впишіть ID нотатки')
                    record_id = input('>>>')
                    if record_id.isdigit():
                        while True:
                            print('Що хочете зробити? (delete_phone | add_phone | edit_birthday | delete_email | add_email )')
                            qst = input(">>>")
                            if qst == 'delete_phone':
                                print('Введіть індекс телефону (з верху від 0)')
                                while True:
                                    phone_ind = input(">>>")
                                    if not phone_ind.isdigit():
                                        print('Індекс має бути цифрою')
                                        continue
                                    phone_ind = int(phone_ind)
                                    try:
                                        contact_manager.delete_phone(record_id, phone_ind)
                                    except KeyError:
                                        print('нема такого індексу')
                                        continue
                                    break
                                break
                            elif qst == 'add_phone':
                                print("Введіть номер телефону, який хочете додати")
                                while True:
                                    phone = input('>>>')
                                    try:
                                        phone = Phone(phone)
                                        contact_manager.add_phone(phone)
                                        break
                                    except PhoneError:
                                        print("Телефон має бути десятизначним та повністю із цифр")
                                        continue
                                break
                            elif qst == 'edit_birthday':
                                print("Введіть нову дату народження")
                                while True:
                                    try:
                                        new_birthday = input('>>>')
                                        new_birthday = Birthday(new_birthday)
                                        contact_manager.edit_birthday(record_id, new_birthday)
                                        break
                                    except BirthdayError:
                                        print('Недійсний формат дня народження, треба YYYY-MM-DD')
                                        continue
                            elif qst == 'delete_email':
                                print('Впишіть індекст імейлу, який хочете видалити (з верху від 0)')
                                while True:
                                    ind = input('>>>')
                                    if not ind.isdigit():
                                        print('Індекс має бути цифрою')
                                        continue
                                    try:
                                        contact_manager.delete_email(record_id, ind)
                                        break
                                    except IndexError:
                                        print('нема такого індексу')
                                        continue
                            elif qst == 'add_email':
                                print("Впишіть новий імейл")
                                while True:
                                    new_email = input('>>>')
                                    try:
                                        new_email = Email(new_email)
                                        contact_manager.add_email(new_email)
                                        break
                                    except EmailError:
                                        print('Недійсна електронна пошта, спробуйте ще')
                                        continue
                                        
                            else:
                                print('Такої команди нема') 
                                continue
                        break
                    else:
                        print('ID має бути цифрою')
                        continue
            elif command_arg == 'search':
                print("Впишіть ім'я для пошуку")    
                name = input('>>>')
                contact_manager.name_search(name)
            else: 
                print('Нема такої команди для менеджеру контактів')        

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
