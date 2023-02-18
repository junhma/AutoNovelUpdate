from pathlib import Path
import autoupdate.edit as edit


BASE_FOLDER = Path(__file__).parent.resolve()
BASE_NAME = r"reading lists - 小説.csv"
#BASE_NAME = r"reading_lists_debug.csv"

file = Path(BASE_FOLDER, BASE_NAME)

edit.convert(file, BASE_FOLDER)
