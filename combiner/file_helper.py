import pandas as pd
from pathlib import Path


# Read csv, excel files by extension
def read_file(file, header_include = None, sheet_name=None):

    extension = file.suffix.lower()

    if extension == ".csv":
        return pd.read_csv(file, header=header_include)

    elif extension in [".xlsx", ".xls"]:

        # All sheet
        if sheet_name == "all":
            return pd.read_excel(file, sheet_name=None, header=header_include)

        # one or selected sheets
        return pd.read_excel(file, sheet_name=sheet_name, header=header_include)

    else:
        return f"Unsportted file type: {extension}"


# Get folder from user
# check if user give a floder
# files in folder
def get_folder():
    while True:
        folder = input("folder:").strip()

        path_object = Path(folder)
        # user give blank folder
        if len(folder) < 1:
            print("Please enter a valid folder path")
        # Is Input is a folder
        elif path_object.is_dir() and path_object.exists():
            print("It is a folder")
            return folder
        elif path_object.is_file():
            print("It is a file, not a folder \n Please try again")
        else:
            print("Please enter valid folder path")


# get file name and join by file extension
def get_file_name(master_file):
    return f"{Path(master_file.name).stem}{Path(master_file.name).suffix}"
