from datetime import datetime
from src.lotto.core.stake import Stake
import csv
owners = ["agustin", "atlas", "bryan", "laiza"]

outputs = []
today = datetime.today().strftime("%m_%d_%Y_")

for owner in owners:
    lines = []
    with open(f"input/{today}{owner}.txt", encoding="utf-8") as file:
        for line in file:
            lines.append(line)
    
    stake = Stake(stake=lines, owner=owner)
    outputs.append(stake.prepare_all)

most_list = max([len(output) for output in outputs])

with open(f'all/{today}report.csv', "w", encoding="utf-8") as file:
    writer = csv.writer(file)
    for line_number in range(most_list):
        row = ""
        for index in range(len(owners)):
            if len(outputs[index]) > line_number:
                row += f"{outputs[index][line_number]}"
            else:
                row += ",,,,,,,,"
        
        cols = row.split(",")
        print(cols)
    # Write each row to the CSV
        writer.writerow(cols)
        # file.write(f"{row}\n")
