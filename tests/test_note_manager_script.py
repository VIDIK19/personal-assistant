import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
src_path = f'{project_root}/src'
sys.path.append(src_path)


from note_manager import Note, NoteData



if __name__ == '__main__':
    my_data = NoteData()
    print(my_data)

    note = Note("So cool to read about everyone's home tradition they"\
                "miss the most! I'm from England but I've been living"\
                "in the States for five years and the thing I miss the most"\
                "is Bonfire Night on November 5th.")

    note.add_tag("Some story")
    note.add_tag('tag example')

    note_2 = Note("This is the second note!")
    note_2.add_tag("Tag 2")

    my_data.add_note(note)
    my_data.add_note(note_2)


    print(my_data.id_search(1))
    print(my_data.tag_search("Tag"))
    my_data.clear_data()
