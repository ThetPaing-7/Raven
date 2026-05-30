import pandas as pd

# Read csv, excel files by extension
def read_file(file):
    
    extension = file.suffix.lower()

    if extension == ".csv":
        data_frame = pd.read_csv(file)
    
    if extension in [".xlsx", ".xls"]:
        data_frame = pd.read_excel(file)
    
    return data_frame