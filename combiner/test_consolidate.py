import csv
from pathlib import Path
from consolidate import main,get_folder,get_file_name,check_header


def test_get_file_name(tmp_path):
    file = tmp_path / "test.csv"

    file.write_text("name, age")
    with open(file, "r") as reader:

        file_name = get_file_name(reader)
    
    assert file_name == "test.csv"


def test_main(tmp_path):

    # sample file
    file_one = tmp_path/"a.csv"
    file_two = tmp_path/"b.csv"

    file_one.write_text("name,age\nJohn,20\n")
    file_two.write_text("name,age\nMike,21\n")

    main(tmp_path, "csv", tmp_path / "output")

    output_file = tmp_path / "output.csv"

    assert output_file.exists()

    with open(output_file, "r") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["a.csv", "name", "age"]
    assert rows[1] == ["a.csv", "John", "20"]
    assert rows[3] == ["b.csv", "Mike", "21"]
    assert rows[2] == ["b.csv", "name", "age"]


def test_check_header(tmp_path):
    
     # sample file
    file_one = tmp_path/"a.csv"
    file_two = tmp_path/"b.csv"

    file_one.write_text(
    "name,age\n"
    "John,20\n"
    "David,35\n"
    )

    file_two.write_text(
    "full_name,age\n"
    "Mike,21\n"
    "Zelen,22\n"
    )

    result = check_header(tmp_path)

    assert result == ['b.csv >> Need to check']

