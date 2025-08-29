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

# Read the result for a single F1 race from formula1.com to html file
def read_f1_race_to_html_file(race_url, filename):
    response = requests.get(race_url)
    with open(filename, "wb") as f:
            f.write(response.content)

# Read the results of all F1 races of a season from formula1.com to html files
def read_f1_season_to_html_files(year, directory):
    season_url = "https://www.formula1.com/en/results/" + str(year) + "/races"
    response = requests.get(season_url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table") # Find the first table element in the html, because that contains the race overview
    race_no=0
    for a in table.find_all("a"): # Find all the a elements in the table, because they are the links to the races
        race_no += 1
        url = a['href']
        race_url = season_url + url[28:]
        filename = directory + str(year) + "-" + str(race_no) + ".html"
        read_f1_race_to_html_file(race_url, filename)
        
