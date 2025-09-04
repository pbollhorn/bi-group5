import pandas as pd

def read_csv_file_to_data_frame(file_path):
    df = pd.read_csv(file_path)
    return df

def read_excel_file_to_data_frame(file_path, skiprows=None):
    df = pd.read_excel(file_path, skiprows=skiprows)
    return df