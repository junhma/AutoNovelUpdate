import pathlib
import autoupdate.edit as edit

BASE_FOLDER = pathlib.Path(__file__).parent.resolve()
BASE_NAME = r"reading_list_novels.csv"
file = pathlib.Path(BASE_FOLDER, BASE_NAME)

edit.convert(file, BASE_FOLDER)