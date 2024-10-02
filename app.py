from datetime import datetime
from src.lotto.core.stake import Stake
from src.lotto.core.entry import Entry
from src.lotto.core.styler import csv_to_html
import csv
owners = ["agustin", "jun", "pards"]

all_lines = []
tulog_lines = []
all_stakes = []
today = datetime.today().strftime("%m_%d_%Y_")
limit = 10
grand_total_bet = 0
grand_total_bet_w_limit = 0

def prepare_input(owners=owners, all_lines=all_lines, all_stakes=all_stakes,):
    global grand_total_bet
    global grand_total_bet_w_limit
    grand_total_bet = 0
    grand_total_bet_w_limit = 0
    for owner in owners:
        lines = []
        with open(f"input/{today}{owner}.txt", encoding="utf-8") as file:
            for index, line in enumerate(file):
                entry = Entry(entry=line, owner=owner, line_number=index+1, limit=limit)
                lines.append(entry)
                tulog_lines.append(entry)
        stake = Stake(stake=lines, owner=owner, limit=limit)
        grand_total_bet += stake.total_bet
        grand_total_bet_w_limit += stake.total_bet_w_limit
        all_stakes.append(stake)
        all_lines.append(stake.prepare_all)

def general_report(all_lines, owners, grand_total_bet, grand_total_bet_w_limit, base_path=""):
    most_list = max([len(output) for output in all_lines])
    filename = f"{base_path}all/{today}report"
    with open(f'{filename}.csv', "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([f"GENERAL REPORT: {today[:-1]}"])
        writer.writerow([f"GRAND TOTAL: {grand_total_bet}"])
        writer.writerow([f"GRAND TOTAL W/ LIMIT: {grand_total_bet_w_limit}"])
        for line_number in range(most_list):
            row = []
            for index in range(len(owners)):
                if len(all_lines[index]) > line_number:
                    row.append(f"{all_lines[index][line_number]}")
                else:
                    row.append(",,,,,,,,")
            
            cols = "".join(row).split(",")

            writer.writerow(cols)
            

def tulog_report(tulog_lines, limit, base_path=""):
    super_stake = Stake(stake=tulog_lines, owner="super", limit=limit)
    filename = f"{base_path}tulog/{today}tulog_report"
    with open(f'{filename}.csv', "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([f"TULOG REPORT: {today[:-1]}"])
        for lines in super_stake.prepare_tulog:
            writer.writerow(lines.split(","))
            
    csv_to_html(csv_file=filename, header_title="DUPLICATE ENTRIES REPORT")

def winners_report(all_winners, all_draws,owners, base_path=""):
    most_list_winners = max([len(output) for output in all_winners])
    most_list_draws = max([len(output) for output in all_draws])
    filename = f"{base_path}winners/{today}winners_report"
    with open(f'{filename}.csv', "w", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([f"WINNER AND DRAW ENTRIES REPORT: {today[:-1]}"])
        for line_number in range(most_list_winners):
            row = []
            for index in range(len(owners)):
                if len(all_winners[index]) > line_number:
                    row.append(f"{all_winners[index][line_number]}")
                else:
                    row.append(",,,,,,,,")
            
            cols = "".join(row).split(",")

            writer.writerow(cols)
        writer.writerow([])
        writer.writerow([])    
        for line_number in range(most_list_draws):
            row = []
            for index in range(len(owners)):
                if len(all_draws[index]) > line_number:
                    row.append(f"{all_draws[index][line_number]}")
                else:
                    row.append(",,,,,,,,")
            
            cols = "".join(row).split(",")

            writer.writerow(cols)
    
prepare_input()
prepare_again = False
while True:
    if prepare_again:
        prepare_input()
        prepare_again = False
    try:
        cmd = int(input(
        """
        WHAT REPORT TO GENERATE CHOOSE COMMAND #:
        1 : Generate General report
        2 : Generate Tulog report
        3 : Generate Winner entries report
        4 : Show wrong input
        """
        ))
    except ValueError:
        print("Wrong command...\nProgram terminated...")
        break
    if cmd == 1:
        print("Processing general report...")
        general_report(
            all_lines = all_lines,
            owners = owners,
            grand_total_bet = grand_total_bet,
            grand_total_bet_w_limit = grand_total_bet_w_limit,
            base_path="",
        )
        print(f"Done generating general report...")
    elif cmd == 2:
        print("Processing tulog report...")
        tulog_report(
            tulog_lines= tulog_lines,
            limit = limit,
            base_path="",
        )
        print(f"Done generating tulog report...")
    elif cmd == 3:
        winning_numbers = []
        for i in range(6):
            number = int(input(f"Winning number {i+1}: "))
            winning_numbers.append(number)
        print("Processing winner entries report..")
        for stake in all_stakes:
            stake.set_stake_winners(winning_numbers=winning_numbers)
        winners_report(
            all_winners = [stake.prepare_winners for stake in all_stakes], 
            all_draws = [stake.prepare_draw for stake in all_stakes],
            owners=owners, 
            base_path=""
        )
        print(f"Done generating winner entries report...")
    elif cmd == 4:
        for stake,owner in zip(all_stakes,owners):
            print(f"Wrong input report on {owner.upper()}")
            print(stake)
            print("\n\n")
        prepare_again = True
    to_stop = input("Do you want to generate other report?(y/n)")
    if not ("y" == to_stop.lower() or "yes" == to_stop.lower()):
        print("Program terminated...")
        break


