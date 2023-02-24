from pathlib import Path, PurePath
import autoupdate.edit as edit

BASE_FOLDER = PurePath(Path.home(), "Documents/GitHub/autoupdate")
BASE_NAME = r"reading lists - 小説.csv"
#BASE_NAME = r"reading_lists_debug.csv"

file = PurePath(BASE_FOLDER, BASE_NAME)

edit.convert(file, BASE_FOLDER)
