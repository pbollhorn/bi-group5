import os
import pandas as pd
import requests
from bs4 import BeautifulSoup
from io import StringIO

def readCsvFileIntoDataFrame(filename):
    df = pd.read_csv(filename)
    return df

def readExcelWorksheetIntoDataFrame(filename):
    df = pd.read_excel(filename)
    return df


def read_f1_race_result(race_url):
    response = requests.get(race_url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table") # Find the table
    string = StringIO(str(table)) # Convert table to string
    df = pd.read_html(string)[0] # Convert string to pandas dataframe
    return df

def read_f1_season_results(year):
    season_url = "https://www.formula1.com/en/results/" + str(year) + "/races"
    response = requests.get(season_url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table") # Find the table
    
    season_results = {} # Empty dictionary
    race_no=0
    
    for a in table.find_all("a"): # Find all links in the table, because they are the links to races
        race_no+=1
        relativeUrl=a['href']
        race_url=season_url+relativeUrl[28:]
        season_results[race_no] = read_f1_race_result(race_url)
        
    return season_results

# Helper function to fix driver name: Replace escape code with space, and add space before 3-letter code
def fix_driver_name(original):
    fixed = original.replace("\xa0", " ")
    fixed = fixed[0:-3] + " " + fixed[-3:]
    return fixed

# Read the result for a single F1 race from html file to data frame
def read_f1_race_to_data_frame(file_path):
    # file_path="html/1950-1.html"
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()
    soup = BeautifulSoup(html_content, "html.parser")
    table = soup.find("table") # Find the first table element in the html, because that contains the race result
    df = pd.read_html(StringIO(str(table)))[0] # Convert table to pandas data frame
    df["DRIVER"] = df["DRIVER"].apply(fix_driver_name)
    return df

# Read the results of all F1 races of a season from html files to a dictionary of data frames
def read_f1_season_to_dictionary(year, directory):
    
    race_no = 0
    season = {}
    
    while True:
        race_no += 1
        file_path = directory + str(year) + "-" + str(race_no) + ".html"
        if not os.path.exists(file_path):
            break
        season[race_no] = read_f1_race_to_data_frame(file_path)
    
    return season
    


# Read the result for a single F1 race from formula1.com to html file
def read_f1_race_to_html_file(race_url, file_path):
    response = requests.get(race_url)
    with open(file_path, "wb") as f:
            f.write(response.content)

# Read the results of all F1 races of a season from formula1.com to html files
def read_f1_season_to_html_files(year, directory):
    season_url = "https://www.formula1.com/en/results/" + str(year) + "/races"
    response = requests.get(season_url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table") # Find the first table element in the html, because that contains the season overview
    race_no = 0
    for a in table.find_all("a"): # Find all the a elements in the table, because they are the links to the races
        race_no += 1
        url = a['href']
        race_url = season_url + url[28:]
        file_path = directory + str(year) + "-" + str(race_no) + ".html"
        read_f1_race_to_html_file(race_url, file_path)
        
