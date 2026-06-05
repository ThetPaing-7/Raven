import csv
from pathlib import Path
import pandas as pd
from file_helper import read_file, get_folder, get_file_name
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
        raise FileNotFoundError(f"No .{extension} files found")

    all_dataframes = []

    for file in files:

        print(f"Processing {file.name}")

        data = read_file(file, sheet_name=sheets, header_include=header_include)

        # CSV or single-sheet Excel
        if isinstance(data, pd.DataFrame):

            df = data.copy()

            df.insert(0, "source_file", file.name)

            all_dataframes.append(df)

        # Multi-sheet Excel
        elif isinstance(data, dict):

            for sheet_name, df in data.items():

                print(f"  Combining sheet: {sheet_name}")

                sheet_df = df.copy()

                sheet_df.insert(0, "sheet_name", sheet_name)

                sheet_df.insert(0, "source_file", file.name)

                all_dataframes.append(sheet_df)

    if not all_dataframes:
        raise ValueError("No data found to combine")

    combined_df = pd.concat(all_dataframes, ignore_index=True)

    output_path = folder / f"{output_file}.csv"

    combined_df.to_csv(output_path, index=False)

    print(f"Successfully combined " f"{len(all_dataframes)} datasets")

    print(f"Output saved to: {output_path}")

    return combined_df
