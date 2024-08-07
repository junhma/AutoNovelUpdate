# AutoNovelUpdate

Automatically update new novel chapters from and to a csv file. Currently support 小説家になろう(syosetu) and NovelUpdates.

## How to use csv input

First, save a list of novels you want to a spreadsheet, then convert that to a csv file called `reading_list.csv`. The csv file must have a column called "title", and another called "link". It's optional that the csv has a "latest_chapter" column. The latest chapter number will be updated to the "latest_chapter" column. Save it to the folder "data".

Uncomment the line `csv_input_main()` in "main.py" then run it. Your updated csv is `reading_lists_out.csv`, saved to the folder `data`.
