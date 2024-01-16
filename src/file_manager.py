from pathlib import Path
from tabulate import tabulate

CATEGORIES = {
    "AUDIO": [".mp3", ".wav", ".flac", ".wma"],
    "DOCS": [".docx", ".txt", ".xlsx", "xls", ".pptx", ".doc"],
    "PICT": [".jpeg", ".png", ".jpg", ".svg"],
    "MOVIES": [".avi", ".mp4", ".mov", ".mkv"],
    "ARHiVE": [".zip", ".gz", ".tar"],
    "PDF": [".pdf"],
}


def get_categories(file: Path) -> str:
    ext = file.suffix.lower()
    for cat, exts in CATEGORIES.items():
        if ext in exts:
            return cat

    return "OTHER"


def move_file(file: Path, category: str, root_dir: Path) -> None:
    target_dir = root_dir.joinpath(category)
    if not target_dir.exists():
        target_dir.mkdir()
    new_path = target_dir.joinpath((file.stem) + file.suffix)
    file = file.replace(new_path)
    lst_file = []
    lst_file.append((root_dir, category, file.name))
    columns = ["File location", "Name Folder", "Name File"]
    print(tabulate((lst_file), headers=columns, tablefmt="grid"))


def sort_folder(path: Path) -> None:
    for element in path.glob("**/*"):
        if element.is_file():
            category = get_categories(element)
            move_file(element, category, path)
