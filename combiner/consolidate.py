import csv
from pathlib import Path
import pandas as pd
from file_helper import read_file, get_folder,get_file_name
from compare_helper import *


def combine_files(
    folder_path,
    output_file="combined",
    extension="xlsx",
    sheets="all",
    header_include=0,
):

    folder = Path(folder_path)

    files = list(folder.glob(f"*.{extension}"))

    if not files:
        raise FileNotFoundError(
            f"No .{extension} files found"
        )

    all_dataframes = []

    for file in files:

        print(f"Processing {file.name}")

        data = read_file(
            file,
            sheet_name=sheets,
            header_include=header_include
        )

        # CSV or single-sheet Excel
        if isinstance(data, pd.DataFrame):

            df = data.copy()

            df.insert(
                0,
                "source_file",
                file.name
            )

            all_dataframes.append(df)

        # Multi-sheet Excel
        elif isinstance(data, dict):

            for sheet_name, df in data.items():

                print(
                    f"  Combining sheet: {sheet_name}"
                )

                sheet_df = df.copy()

                sheet_df.insert(
                    0,
                    "sheet_name",
                    sheet_name
                )

                sheet_df.insert(
                    0,
                    "source_file",
                    file.name
                )

                all_dataframes.append(sheet_df)

    if not all_dataframes:
        raise ValueError(
            "No data found to combine"
        )

    combined_df = pd.concat(
        all_dataframes,
        ignore_index=True
    )

    output_path = folder / f"{output_file}.csv"

    combined_df.to_csv(
        output_path,
        index=False
    )

    print(
        f"Successfully combined "
        f"{len(all_dataframes)} datasets"
    )

    print(
        f"Output saved to: {output_path}"
    )

    return combined_df


def check_header(
    folder_path,
    master_file,
    rows=2,
    sheet_name=0
):
    """
    Compare the first N rows (header template)
    of all files against a master file.
    """

    folder = Path(folder_path)

    master_path = folder / master_file

    if not master_path.exists():
        raise FileNotFoundError(
            f"Master file '{master_file}' not found"
        )

    # Master Header
    master_header = get_header(
        master_path,
        rows=rows,
        sheet_name=sheet_name
    )

    master_flat = flatten(master_header)

    # User Files
    files = [
        file
        for file in folder.iterdir()
        if file.is_file()
        and file != master_path
        and file.suffix.lower() in [
            ".csv",
            ".xlsx",
            ".xls"
        ]
    ]

    if not files:
        print("No files found to compare.")
        return

    # Compare Files
    for file in files:

        print(f"\nChecking: {file.name}")

        try:

            user_header = get_header(
                file,
                rows=rows,
                sheet_name=sheet_name
            )

            user_flat = flatten(user_header)

            # Perfect Match
            if master_header == user_header:

                print(
                    f"\033[92m✓ {file.name} Header Match\033[0m"
                )

                continue

            print(
                f"\033[91m✗ {file.name} Header Mismatch\033[0m"
            )

            # Different Number of Columns
            if len(master_flat) != len(user_flat):

                print(
                    f"\nColumn Count Mismatch"
                )

                print(
                    f"Master Columns : {len(master_flat)}"
                )

                print(
                    f"User Columns   : {len(user_flat)}"
                )

            # Show Differences
            print()

            show_columns_difference(
                master_flat,
                user_flat
            )

        except Exception as error:

            print(
                f"\033[91mFailed to process "
                f"{file.name}\033[0m"
            )

            print(error)

if __name__ == "__main__":
    folder = get_folder()
    check_header(folder,"MOCK_DATA.xlsx")
