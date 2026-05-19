import csv
from pathlib import Path

def combine(folder_path,extension):
    
    folder = Path(folder_path)
    csv_files = [
        file for file in folder.glob(f'*.{extension}')
        if file.name != "combine_student_file_v2.csv"
    ]

    with open("combine_student_file_v2.csv","w", newline="") as outfile:
        writer = csv.writer(outfile)

        for file in csv_files:
            with open(file,"r") as infile:
                print(f"processing {file.name}")
                reader = csv.reader(infile)
                
                for row in reader:
                    writer.writerow([file.name,*row])


# Get folder from user
# check if user give a floder
# files in folder

def get_folder():
    while True:
        folder = input("folder:" ).strip()
        path_object = Path(folder)
    # Is Input is a folder
        if path_object.is_dir() and path_object.exists():
            print("It is a folder")
            return folder
        elif path_object.is_file():
            print("It is a file, not a folder \n Please try again")
        else:
            print("Please valid folder path")




def check_header():
    ...
# header check 


# check blank row and remove
def exclude_blank_row():
    ...


get_folder()