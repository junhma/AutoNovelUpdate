import logging
from pathlib import Path, PurePath

import auto_update.edit as edit

current_directory = Path.cwd()
folder = current_directory / "data"
BASE_NAME = r"reading lists - 小説.csv"
file = PurePath(folder, BASE_NAME)

edit.auto_update(file)
logging.shutdown()