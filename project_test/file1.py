import re

formated_number = []

with open("sample.txt","r") as file:
    for line in file:
        ["start","end","step"]
        line = f'{line[:2]}-{line[2:5]}-{line[5:8]}-{line[8:]}'
        formated_number.append(line)
        

with open("formatted_number.txt","w") as file:
    for line in formated_number:
        file.write(line)