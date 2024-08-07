"""
Convert a Google sheets link to DataFrame, then call the method update.update_chapter on the DataFrame.
Update the "latest_chapter" column of the Google sheet.
"""
import gspread
import pandas as pd
from pyvirtualdisplay.display import Display
import auto_update.update as update
import json

async def auto_update_google_sheet():
    with open("config/config.json") as f:
        config = json.load(f)
    sheet_name = config.get("sheet_name")
    worksheet_name = config.get("worksheet_name")

    gc = gspread.service_account(filename='config/credentials.json') # type: ignore
    sh = gc.open(sheet_name)
    worksheet = sh.worksheet(worksheet_name)

    df = pd.DataFrame(worksheet.get_all_records())
    with Display(visible=False, size=(1080,720)):
        df_updated = await update.update_chapter(df)
    df_updated_series = df_updated['latest_chapter'].fillna(0)
    df_updated_list = df_updated_series.to_list()
    # Find the column index where 'latest_chapter' is located
    column_index = df_updated.columns.get_loc('latest_chapter') + 1  # Convert to 1-based index
    # Convert column index to letter representation
    column_letter = chr(65 + column_index - 1)  # A=65, B=66, etc.
    df_updated_values = [[df_updated_series.name]] +[[value] for value in df_updated_list]
    worksheet.update(range_name = f"{column_letter}:{column_letter}", values = df_updated_values)

    #raise GSpreadException(gspread.exceptions.GSpreadException: the header row in the worksheet is not unique, try passing 'expected_headers' to get_all_records