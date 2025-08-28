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
    
    
    season_results = {} # empty dictionary
    race_no=0
    
    for a in table.find_all("a"): # Find all links in the table
        relativeUrl=a['href']
        race_url=season_url+relativeUrl[28:]
        print(race_url)
        df = read_f1_race_result(race_url) # pandas frame for race result
        print(df)
        
        race_no+=1
        season_results[race_no] = df
        
    return season_results
    
    
    # string = StringIO(str(table)) # Convert table to string
    # df = pd.read_html(string) # Convert string to pandas
    # return df