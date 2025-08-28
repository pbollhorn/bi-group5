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


def readF1RaceResult(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table") # Find the table
    string = StringIO(str(table)) # Convert table to string
    df = pd.read_html(string) # Convert string to pandas
    return df