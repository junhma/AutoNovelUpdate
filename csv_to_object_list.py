# ok

import pandas as pd
from novel import Novel

def csv_to_object_list(req):
    dfcsv = pd.read_csv(req)  # csv to dataframe
    novels = list()

    for index in dfcsv.index:
        current_novel = Novel(
            dfcsv['title'][index], dfcsv['latest_chapter'][index], dfcsv['link'][index])
        novels.append(current_novel)
    
    return novels