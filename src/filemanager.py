import os
from pathlib import Path
import sys

import shutil

CATEGORIES = {
    "AUDIO": [".mp3", ".wav", ".flac", ".wma"],
    "DOCS": [".docx", ".txt", ".xlsx", "xls", ".pptx", ".doc"],
    "PICT": [".jpeg", ".png", ".jpg", ".svg"],
    "MOVIES": [".avi", ".mp4", ".mov", ".mkv"],
    "ARHiVE": [".zip", ".gz", ".tar"],
    "PDF": [".pdf"],
}
CYRILLIC_SYMBOLS = "aбвгдeёжзийклмнопpcтyфхцчшщъыьэюяєiїґ"
TRANSLATION = (
    "a",
    "b",
    "v",
    "g",
    "d",
    "e",
    "e",
    "j",
    "z",
    "u",
    "j",
    "k",
    "l",
    "m",
    "n",
    "o",
    "p",
    "r",
    "s",
    "t",
    "u",
    "f",
    "h",
    "ts",
    "ch",
    "sh",
    "sch",
    "",
    "u",
    "",
    "e",
    "yu",
    "ya",
    "je",
    "i",
    "ji",
    "g",
)
TRANS = {}
SYMB = ("!", "№", "$", "%", "&", "(", ")", "+", "-", "_", "#", " ")
for c, l in zip(CYRILLIC_SYMBOLS, TRANSLATION):
    TRANS[ord(c)] = l
    TRANS[ord(c.upper())] = l.upper()
    TRANS[ord(c.lower())] = l.lower()
for i in SYMB:
    TRANS[ord(i)] = "_"


def normalize(file: Path) -> None:
    return file.translate(TRANS)


f = []


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    return "OTHER"


categor = []


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_path = target_dir.joinpath(normalize(file.stem) + file.suffix)
    categor.append(file.name)
    print(category)
    # if not new_path.exists():
    file = file.replace(new_path)
    print(file.name, target_dir)
    # if file.is_file() and file.suffix in [".zip", ".gz", ".tar"]:
    #     if file.is_file() and file.suffix in [
    #         ".zip",
    #         ".gz",
    #         ".tar",
    #     ]:
    #         shutil.unpack_archive(file, target_dir.joinpath(file.stem))
    # return shutil.unpack_archive(file, target_dir)


def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
            # if element.is_dir():
            #     if element.stat().st_size == 0:
            #         try:
            #             os.rmdir(element)
            #         except OSError:
            #             continue
            # return os.rmdir(element)


# def del_folder(path: Path) -> None:
#     for element in list(path.glob("**/*"))[::-1]:
#         if element.is_dir():
#             try:
#                 os.rmdir(element)
#             except OSError:
#                 continue
# return del_folder(path)


def append_list(file: Path, category: str, root_dir: Path):  # root_dir: Path
    for file in list(file.glob("**/*")):
        if file.is_file():
            print(file.name, category)
    # return element.name, category


def main():
    try:
        path = Path(sys.argv[1])
    except IndexError:
        return "No path to folder"
    if not path.exists():
        return "Folder does not exists"

    sort_folder(path)

    # del_folder(path)
    return "All ok"


if __name__ == "__main__":
    main()
