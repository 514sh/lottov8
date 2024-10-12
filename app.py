from datetime import datetime
from src.lotto.core.stake import Stake
from src.lotto.core.entry import Entry
from src.lotto.core.config import OWNERS, BASE_PATH
import csv


class CLI:
    def __init__(self, owners, limit, base_path):
        self.__owners = owners
        self.__limit = limit
        self.__base_path = base_path
        self.__all_lines = []
        self.__tulog_lines = []
        self.__all_stakes = []
        self.__today = datetime.today().strftime("%m_%d_%Y")
        self.__grand_total_bet = 0
        self.__grand_total_bet_w_limit = 0
        
    @property
    def base_path(self):
        return self.__base_path
    
    @property
    def owners(self):
        return self.__owners
        
    @property
    def limit(self):
        return self.__limit
        
    @property
    def today(self):
        return self.__today

    @property
    def game(self):
        for stake in self.__all_stakes:
            if stake.game:
                return stake.game
        return None
    
    @property
    def most_list(self):
        return max([len(output) for output in self.__all_lines])
    
    
    def filenames(self, report_key="", owner_name=""):
        file_names = {
            "input": f"{self.base_path}/input/{self.today}_{owner_name}.txt",
            "general": f"{self.base_path}/all/{self.today}_report.csv",
            "tulog": f"{self.base_path}/tulog/{self.today}_tulog_report.csv",
            "winners": f"{self.base_path}/winners/{self.today}_winners_report.csv",
        }
        return file_names.get(report_key.lower())
        
        
    def __reset(self):
        self.__all_lines.clear()
        self.__all_stakes.clear()
        self.__tulog_lines.clear()
        self.__grand_total_bet = 0
        self.__grand_total_bet_w_limit = 0
    
    def prepare_input(self):
        self.__reset()
        for owner in self.owners:
            lines = []
            with open(self.filenames("input",owner), encoding="utf-8") as file:
                for index, line in enumerate(file):
                    entry = Entry(entry=line, owner=owner, line_number=index+1, limit=limit)
                    lines.append(entry)
                    self.__tulog_lines.append(entry)
            stake = Stake(stake=lines, owner=owner, limit=self.__limit)
            self.__grand_total_bet += stake.total_bet
            self.__grand_total_bet_w_limit += stake.total_bet_w_limit
            self.__all_stakes.append(stake)
            self.__all_lines.append(stake.prepare_all)
            
    def general_report(self):
        with open(self.filenames("general"), "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([f"GENERAL REPORT: {self.today} {self.game if self.game else ""}"])
            writer.writerow([f"GRAND TOTAL: {self.__grand_total_bet}"])
            writer.writerow([f"GRAND TOTAL W/ LIMIT: {self.__grand_total_bet_w_limit}"])
            for line_number in range(self.most_list):
                row = []
                for index in range(len(self.owners)):
                    if len(self.__all_lines[index]) > line_number:
                        row.append(f"{self.__all_lines[index][line_number]}")
                    else:
                        row.append(",,,,,,")
                
                cols = "".join(row).split(",")

                writer.writerow(cols)
    
    def tulog_report(self):
        super_stake = Stake(stake=self.__tulog_lines, owner="super", limit=limit)
        with open(self.filenames("tulog"), "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([f"TULOG REPORT: {self.today} {self.game if self.game else ""}"])
            for lines in super_stake.prepare_tulog:
                writer.writerow(lines.split(","))
            
    def winners_report(self, winning_numbers):
        for stake in self.__all_stakes:
            stake.set_stake_winners(winning_numbers=winning_numbers)
        all_winners = [stake.prepare_winners for stake in self.__all_stakes]
        all_draws = [stake.prepare_draw for stake in self.__all_stakes]
        most_list_winners = max([len(output) for output in all_winners])
        most_list_draws = max([len(output) for output in all_draws])
        with open(self.filenames("winners"), "w", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow([f"WINNER AND DRAW ENTRIES REPORT: {self.today} {self.game if self.game else ""}"])
            for line_number in range(most_list_winners):
                row = []
                for index in range(len(self.owners)):
                    if len(all_winners[index]) > line_number:
                        row.append(f"{all_winners[index][line_number]}")
                    else:
                        row.append(",,,,,,")
                
                cols = "".join(row).split(",")

                writer.writerow(cols)
            writer.writerow([])
            writer.writerow([])    
            for line_number in range(most_list_draws):
                row = []
                for index in range(len(self.owners)):
                    if len(all_draws[index]) > line_number:
                        row.append(f"{all_draws[index][line_number]}")
                    else:
                        row.append(",,,,,,")
                
                cols = "".join(row).split(",")

                writer.writerow(cols)
                
    def wrong_input_report(self):
        for stake,owner in zip(self.__all_stakes,self.owners):
            print(f"Wrong input report on {owner.upper()}")
            print(stake)
            print() 


if __name__ == "__main__":
    limit = 10
    my_cli = CLI(owners=OWNERS,limit=limit,base_path=BASE_PATH)
    my_cli.prepare_input()
    prepare_again = False
    while True:
        if prepare_again:
            my_cli.prepare_input()
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
            my_cli.general_report()
            print(f"Done generating general report...")
        elif cmd == 2:
            print("Processing tulog report...")
            my_cli.tulog_report()
            print(f"Done generating tulog report...")
        elif cmd == 3:
            winning_numbers = []
            for i in range(6):
                number = int(input(f"Winning number {i+1}: "))
                winning_numbers.append(number)
            print("Processing winner entries report..")
            my_cli.winners_report(winning_numbers=winning_numbers)
            print(f"Done generating winner entries report...")
        elif cmd == 4:
            my_cli.wrong_input_report()
            prepare_again = True
        to_stop = input("Do you want to generate other report?(y/n)")
        if not ("y" == to_stop.lower() or "yes" == to_stop.lower()):
            print("Program terminated...")
            break


