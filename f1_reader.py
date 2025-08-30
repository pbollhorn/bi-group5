import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

# Read the result for a F1 race from html file to data frame,
# and then clean up the data in the data frame.
# race_title and race_note are added as metadata (attrs) to the data frame.
def read_f1_race_from_html_file_to_data_frame(file_path):
    
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table")
    df = pd.read_html(StringIO(str(table)))[0]
    
    df.attrs["race_title"] = soup.title.text[:-14]
    
    # Delete last row if it just contains a note, and instead add the note as metadata
    last = df["POS."].iloc[-1]
    if isinstance(last, str) and len(last)>=4:
        df.attrs["race_note"] = last
        df = df.iloc[:-1]
    
    df["DRIVER"] = df["DRIVER"].apply(fix_driver_name)
    
    df["PTS."] = df["PTS."].apply(float)
        
    return df


# Helper function to fix driver name:
# - Replace escape code with space
# - Add space before 3-letter code
def fix_driver_name(original):
    fixed = original.replace("\xa0", " ")
    fixed = fixed[0:-3] + " " + fixed[-3:]
    return fixed


# Read the results of all F1 races of a season from html files to a dictionary of data frames
def read_f1_season_from_html_files_to_dictionary(year, directory):
    
    race_no = 0
    season = {}
    
    while True:
        race_no += 1
        file_path = os.path.join(directory, f"{year}-{race_no}.html")
        if not os.path.exists(file_path):
            break
        season[race_no] = read_f1_race_from_html_file_to_data_frame(file_path)
    
    return season
    
    
# Read the result for a F1 race from formula1.com to html file
def read_f1_race_from_website_to_html_file(race_url, file_path):
    response = requests.get(race_url)
    with open(file_path, "wb") as f:
            f.write(response.content)


# Read the results of all F1 races of a season from formula1.com to html files
def read_f1_season_from_website_to_html_files(year, directory):
    season_url = f"https://www.formula1.com/en/results/{year}/races"
    response = requests.get(season_url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table") # Find the first table element in the html, because that contains the season race overview
    race_no = 0
    for a in table.find_all("a"): # Find all the a elements in the table, because they are the links to the races
        race_no += 1
        href = a['href']
        race_url = season_url + href[28:]
        file_path = os.path.join(directory, f"{year}-{race_no}.html")
        read_f1_race_from_website_to_html_file(race_url, file_path)