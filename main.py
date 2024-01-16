from src.note_manager import NoteManager
from src.file_manager import sort_folder
from pathlib import Path

def main():
    note_manager = NoteManager()

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
                print("Нема такої команди")

        
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
            print("Нема такого менеджера")
        # Це маленька чатсина функціоналу - просто приклад
        
        


if __name__ == "__main__":
    main()
