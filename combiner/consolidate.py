import csv
from pathlib import Path
import pandas as panda

def main(folder_path, extension,output_file):

    folder = Path(folder_path)
    files = [
        file
        for file in folder.glob(f"*.{extension}")
        if file.name != f'{output_file}.csv'
    ]
    

    all_dataframes = []

    for file in files:
        print(f"processing {file.name}")

        # for csv file
        if file.suffix.lower() == ".csv":
            data_frame = panda.read_csv(file)
        
        if file.suffix.lower() in [".xlsx", ".xls"]:
            data_frame = panda.read_excel(file)

        
        data_frame.insert(0, "source_file", file.name)

        all_dataframes.append(data_frame)

    combine_data_frame = panda.concat(all_dataframes, ignore_index=True)

    combine_data_frame.to_csv(f'{output_file}.csv', index = False)

    print("File Combine Successfully")



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
def check_header(folder_path, extension):
    folder = Path(folder_path)

    #result
    header_check_result = []


    # Take only the desire file type
    templates = [file for file in folder.glob(f'*.{extension}')]

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

    remmaing_files = []

    for template in templates[1:]:
        with open(template, "r") as file:
            reader = csv.reader(file, delimiter=",")
            # number of row would like to take
            for i, row in enumerate(reader):
                remmaing_files.append({"file_name": get_file_name(file), "header": row})
                if i == 0:
                    break

    #Comparing master_header with reaming header
    for temp in remmaing_files:
        if temp['header'] != main_file['header']:
            header_check_result.append(f'{temp["file_name"]} >> Need to check')
        else:
            header_check_result.append(f'{temp["file_name"]} >> Same Header')

    return header_check_result


if __name__ == "__main__":
    folder = get_folder()
    main(folder,"xlsx","Test")
    