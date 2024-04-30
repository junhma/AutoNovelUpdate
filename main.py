import logging
from pathlib import Path, PurePath

import auto_update.csv_input as csv_input

def main():
    #csv_input_main() # Uncomment for csv input
    logging.shutdown()

def csv_input_main():
    """
    Support for csv input. It gives the file to auto_update_csv.
    Then saves an updated reading_lists_out.csv to the folder data.
    """
    current_directory = Path.cwd()
    folder = current_directory / "data"
    BASE_NAME = r"reading_list.csv" # Edit this to change file name
    file = PurePath(folder, BASE_NAME)
    csv_input.auto_update_csv(file)

if __name__ == "__main__":
  main()