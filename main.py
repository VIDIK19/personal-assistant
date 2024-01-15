from src.note_manager import NoteManager



def main():
    note_manager = NoteManager()

    while True:
        user_input = input(">>>")

        # створення списку слів із юзер-інпута
        lst_of_args = user_input.lower().strip().split(" ")

        # перше слово з юзер інпута - команда, наступні слова - аргументи
        command = lst_of_args[0]

        # завершення програми
        if command == "exit":
            break

        elif command == 'create_note':
            # Запрашуємо ввести текст нотатки 
            info = input(">>>Введіть текст нотатки:")
            # Додає нотатку в БД 
            note_manager.add_note(info)
            # Показує БД
            note_manager.show_data()
        
        elif command == 'add_tag':
            # Запрашуємо id нотатки
            note_id = input(">>>Введіть ID нотатки, до якої хочете додати тег:")
            # Запрашуємо тег
            tag = input(">>>Введіть тег:")
            # Додаємо тег в нотатку
            note_manager.add_tag(int(note_id), tag)
        
        # Це маленька чатсина функціоналу - просто приклад
if __name__ == '__main__':
    main()     