import pandas as pd
from file_helper import read_file


# compare given two lists
def compare_two_lists(list_one, list_two):
    return list_one == list_two


def to_data_frame(header, filename):
    master_lists = header
    master_lists = [item for newlist in master_lists for item in newlist]
    master_frame = pd.DataFrame(master_lists)
    return master_frame


def get_header(file_path, rows=2, sheet_name=None):

    data = read_file(file_path, sheet_name=sheet_name, header_include=None)

    # CSV or single-sheet Excel
    if isinstance(data, pd.DataFrame):

        return data.head(rows).fillna("").values.tolist()

    # Multi-sheet Excel
    if isinstance(data, dict):

        headers = {}

        for sheet, df in data.items():

            headers[sheet] = df.head(rows).fillna("").values.tolist()

        return headers

    raise TypeError(f"Unsupported type: {type(data)}")


def flatten(data):
    return [item for row in data for item in row]


def check_header_counts(project_file, user_file):
    return len(project_file) == len(user_file)


def show_columns_difference(master_columns, user_columns):

    max_length = max(len(master_columns), len(user_columns))

    print(f"{'Pos':<5}" f"{'Master':<30}" f"{'User':<30}")

    print("-" * 65)

    for index in range(max_length):

        master_value = (
            str(master_columns[index])
            if index < len(master_columns)
            else "\x1b[31mExtra\x1b[0m"
        )

        user_value = (
            str(user_columns[index])
            if index < len(user_columns)
            else "\x1b[31mMissing\x11B[0m"
        )

        if master_value != user_value:

            print(f"{index + 1:<5}" f"{master_value:<30}" f"{user_value:<30}")


def compare_headers(master_header, user_header):

    master_flat = flatten(master_header)
    user_flat = flatten(user_header)

    if len(master_flat) != len(user_flat):
        return False

    return master_header == user_header
