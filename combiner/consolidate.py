import csv
from pathlib import Path
import pandas as panda
from file_helper import read_file, get_folder, get_file_name
from compare_helper import compare_two_lists, to_data_frame,  show_columns_difference,check_header_counts, flatern_to_list


def combine_files(
    folder_path,
    output_file="combined",
    extension="xlsx",
    sheets="all",
    header_include=0,
):

    folder = Path(folder_path)
    files = [
        file
        for file in folder.glob(f"*.{extension}")
        if file.name != f"{output_file}.csv"
    ]


    all_dataframes = []

    for file in files:
        print(f"processing {file.name}")

        data_frame = read_file(file, header_include=header_include, sheet_name=sheets)

        # if the file is csv file
        if isinstance(data_frame, panda.DataFrame):

            data_frame.insert(0, "source_file", file.name)
            all_dataframes.append(data_frame)

        # if the file is excel sheet
        elif isinstance(data_frame, dict):
            for sheet, df in data_frame.items():
                print(f"Combining sheet: {sheet}")
                df.insert(0, "sheet_name", sheet)
                df.insert(0, "soruce_file", file.name)

                all_dataframes.append(df)

    # combine all
    combine_data_frame = panda.concat(all_dataframes, ignore_index=True)

    combine_data_frame.to_csv(f"{output_file}.csv", index=False)

    print("File Combine Successfully")


# Check header
def check_header(folder_path, master_file, number=2, extension="xlsx", sheet_name = None):

    folder = Path(folder_path)

    header_check_result = []

    # Get all files
    templates = [file for file in folder.glob(f"*.{extension}")]

    # Find master file
    project_template = list(filter(lambda f: f.name == master_file, templates))

    if not project_template:
        raise FileNotFoundError("Master file not found")

    # Read master file
    master_df = read_file(project_template[0],sheet_name = sheet_name,header_include=None)
    master_file_name = get_file_name(project_template[0])
    # Take first N rows as header template
    master_header = master_df.head(number).values.tolist()
    master = {"filename": master_file_name, "header": master_header}

    #   print("MASTER HEADER")
    # print(master)
    # print("========================")

    # User file
    user_files = []

    # Get user files
    user_templates = list(filter(lambda f: f.name != master_file, templates))

    for template in user_templates:
        df = read_file(template, sheet_name = sheet_name,header_include=None)
        filename = get_file_name(template)
        user_header = df.head(number).values.tolist()
        user_files.append({"filename": filename, "header": user_header})

    # print(user_files)

    # Comparing file
    for file in user_files:

        master_lists = flatern_to_list(master["header"])
        user_lists = flatern_to_list(file["header"])

        # Header columns are not equal
        if check_header_counts(master_lists,user_lists) == False:
            print(f"{master["filename"]:<15} | {file["filename"]:<15}")
            show_columns_difference(master_lists,user_lists)
            print("=" * 10)
        elif check_header_counts(master_lists,user_lists) == True:
            if compare_two_lists(master["header"], file["header"]):
                print(f'\033[92m{file["filename"]} Header Match\033[0m')
            else:
                master_frame = to_data_frame(master["header"], master["filename"])
                file_frame = to_data_frame(file["header"], file["filename"])
                comparison  = master_frame.compare(file_frame,result_names=("project_file","user_file"),keep_equal=True)
                print(f'\033[91m{file["filename"]} Need to Check\033[0m')
                print(comparison)


if __name__ == "__main__":
    folder = get_folder()
    check_header(folder,"students_file1.csv",number=1,extension="csv")
