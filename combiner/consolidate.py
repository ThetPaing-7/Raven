import csv
from pathlib import Path
import pandas as panda
from helper import read_file, get_folder, get_file_name


def combine_files(folder_path, output_file, extension=".xlsx"):

    folder = Path(folder_path)
    files = [
        file
        for file in folder.glob(f"*.{extension}")
        if file.name != f"{output_file}.csv"
    ]

    all_dataframes = []

    for file in files:
        print(f"processing {file.name}")

        data_frame = read_file(file)

        data_frame.insert(0, "source_file", file.name)

        all_dataframes.append(data_frame)

    combine_data_frame = panda.concat(all_dataframes, ignore_index=True)

    combine_data_frame.to_csv(f"{output_file}.csv", index=False)

    print("File Combine Successfully")


# Check header
def check_header(folder_path, master_file, number=2, extension="xlsx"):

    folder = Path(folder_path)

    header_check_result = []

    # Get all files
    templates = [file for file in folder.glob(f"*.{extension}")]

    # Find master file
    project_template = list(filter(lambda f: f.name == master_file, templates))

    if not project_template:
        raise FileNotFoundError("Master file not found")

    # Read master file
    master_df = read_file(project_template[0], None)
    master_file_name = get_file_name(project_template[0])
    # Take first N rows as header template
    master_header = master_df.head(number).values.tolist()
    master = {"filename": master_file_name, "header": master_header}

    print("MASTER HEADER")
    print(master)
    print("========================")

    # User file
    user_files = []

    # Get user files
    user_templates = list(filter(lambda f: f.name != master_file, templates))

    for template in user_templates:
        df = read_file(template, None)
        filename = get_file_name(template)
        user_header = df.head(number).values.tolist()
        user_files.append({"filename": filename, "header": user_header})

    print(user_files)

    # Comparing file
    for file in user_files:
        if master["header"] == file["header"]:
            print("Header Match")
        else:
            print("Need to check")


if __name__ == "__main__":
    folder = get_folder()
    check_header(folder, "students.file3.csv", number=2, extension="csv")
