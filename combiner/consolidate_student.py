import csv
from pathlib import Path


def consolidate(folder_path, extension):

    folder = Path(folder_path)
    csv_files = [
        file
        for file in folder.glob(f"*.{extension}")
        if file.name != "combine_student_file_v2.csv"
    ]

    with open("combine_student_file_v2.csv", "w", newline="") as outfile:
        writer = csv.writer(outfile)

        for file in csv_files:
            with open(file, "r") as infile:
                print(f"processing {file.name}")
                reader = csv.reader(infile)

                for row in reader:
                    writer.writerow([file.name, *row])


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
    return f'{Path(master_file.name).stem}{Path(master_file.name).suffix}'


# Check header
def check_header(folder_path):
    folder = Path(folder_path)

    # Take only the desire file type
    templates = [file for file in folder.glob("*csv")]

    # To store master file name and header
    main_file = {}

    # choose a master file header to check with other file header
    with open(templates[0], "r") as master_file:
        reader = csv.reader(master_file, delimiter=",")

        # Getting the master file name and join with extension
        main_file["master_file_name"] = get_file_name(master_file)
        main_file["header"] = next(reader)
        print("====================================")

    # Getting the header and name of rest of the file

    remmaing_files = {
        "file_name" : [],
        "header" : []
    }

    for template in templates[1:]:
        with open(template, "r") as file:
            reader = csv.reader(file, delimiter=",")
            # number of row would like to take
            for i, row in enumerate(reader):
                remmaing_files["header"].append(row)
                remmaing_files["file_name"].append(get_file_name(file))
                if i == 0:
                    break

    # Comparing master_header with reaming header
    for header in remmaing_files["header"]:
        if header != main_file["header"]:
            print("Need to check")
        else:
            print("same header")


# check blank row and remove
def exclude_blank_row(): 
    ...

folder_path = get_folder()
check_header(folder_path)
