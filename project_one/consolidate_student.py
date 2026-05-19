import csv
from pathlib import Path

folder = Path("/home/thetpainglin/consolidate/project_one")
csv_files = [
    file for file in folder.glob("*.csv")
    if file.name != "combine_student_file_v2.csv"
]

with open("combine_student_file_v2.csv","w", newline="") as outfile:
    writer = csv.writer(outfile)

    for file in csv_files:
        with open(file,"r") as infile:
            print(f"processing {file.name}")
            reader = csv.reader(infile)
            
            for row in reader:
                writer.writerow([file.name, *row])