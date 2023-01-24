#stub

import pandas as pd

# REQUIRE: list of Novel objects
# RETURN: modified excel file

def object_list_to_excel(novels):
    df = pd.read_csv(req)  # csv to dataframe

    for index in dfcsv.index:
        current_novel = Novel(
            dfcsv['title'][index], dfcsv['latest_chapter'][index], dfcsv['link'][index])
        novels.append(current_novel)
        
    modified_excel = df.to_excel('saved_file.xlsx', index=False)
    return modified_excel
