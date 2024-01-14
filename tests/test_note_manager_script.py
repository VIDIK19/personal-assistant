import os
import sys

current_file_path = os.path.abspath(__file__)
project_root = os.path.dirname(os.path.dirname(current_file_path))
src_path = f'{project_root}/src'
sys.path.append(src_path)


from note_manager import Note, NoteData



if __name__ == '__main__':
    pass
    #   add_note_example
    # note_manager = NoteManager()
    # note_manager.add_note("HEllo, this is an example of the note that you can create with my module."\
    #                         "Good Luck!")
    # note_manager.add_note("This is the second note")
    # note_manager.show_data()
    # note_manager.clear_data()

    #   add_tag_example

    # note_manager.add_tag(1, "This is my tag")
    # note_manager.add_tag(1, "This is second tag")
    # note_manager.add_tag(2, "Tag of the second note")
    # note_manager.show_data()
    # note_manager.clear_data()

    #   delete_note_example

    # note_manager.delete_note(1)
    # note_manager.show_data()
    # note_manager.clear_data()

    #   open_note_example

    # note_manager.open_note(2)
    # note_manager.clear_data()

    #   edit_tag_example
    # note_manager.edit_tag(1, 0, "This is a new tag for first note")
    # note_manager.show_data()
    # note_manager.clear_data()

    #   search_tag_exampe
    # note_manager.search_tag("This")
    # note_manager.clear_data()

