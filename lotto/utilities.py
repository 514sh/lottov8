import re
import heapq
from datetime import datetime
from pathlib import Path
import pandas as pd
import csv2pdf

def sync_file_read(filename: str) -> str:
    with open(filename, encoding="utf-8") as file:
        return file.read()
    
def parse_read_file(input: str) -> list[str]:
    if not isinstance(input, str):
        raise TypeError(f"Expected str, got {type(input).__name__}")
    return input.split("\n")

def parse_date(date: datetime) -> tuple[str, str, str]:
    if not isinstance(date, datetime):
        raise TypeError(f"Expected datetime, got {type(input).__name__}")
    
    return str(date.year), str(date.month).zfill(2), str(date.day).zfill(2)
    
def generate_filename(owner: str, date: datetime,filetype: str="txt") -> str:
    if not isinstance(owner, str):
        raise TypeError(f"Expected str, got {type(owner).__name__}")
    elif not isinstance(date, datetime):
        raise TypeError(f"Expected datetime, got {type(input).__name__}")
    if not isinstance(filetype, str):
        raise TypeError(f"Expected str, got {type(filetype).__name__}")
    
    year, month, day = parse_date(date)
    filename = "_".join([year, month, day, owner])
    return f"{filename}.{filetype}"


def generate_absolute_filename(parent_dir: Path,owner: str, date: datetime, filetype: str="txt"):
    filename = generate_filename(owner, date, filetype)
    return f"{parent_dir}/{filename}"

def separator(entries: list, owner:str, game_date: datetime):
    wrong_input = {}
    valid_entries = []
    for index, entry in enumerate(entries):
        split_entry = re.split("[^0-9]", entry)
        prepared_entry = [int(i) for i in split_entry if i != ""]
        if len(prepared_entry) == 0:
            continue
        elif _is_valid_entry(prepared_entry, game_date):
            valid_entry = (index+1, entry, owner)
            valid_entries.append(valid_entry)
        else:
            wrong_input[index + 1] = entry
    return wrong_input, valid_entries
    
def _is_valid_entry(prepared_entry: str, game_date: datetime):
    if len(prepared_entry) != 4:
        return False
    elif prepared_entry[3] % 5 != 0:
        return False
    elif len(set(prepared_entry[:3])) != 3:
        return False
    
    for entry in prepared_entry[:3]:
        if entry > get_max_possible_combination(game_date):
            return False
        
    return True

def get_max_possible_combination(game_date: datetime):
    games = [45,49,45,49,45,42,49]
    day_of_the_week = game_date.weekday()
    return games[day_of_the_week]


def combine_entries(list_of_sorted_entries):
    return list(heapq.merge(*list_of_sorted_entries))

class FileWriter:
    def __init__(self, base_dir:Path, game_date: datetime, game_bets, header_font=None, body_font=None):
        self._base_dir = base_dir
        self._game_date = game_date
        self._game_bets = game_bets
        self._filename = ""
        self._body = ""
        self._title = ""
        self._header_font = header_font
        self._body_font = body_font
    
    def write(self):
        with open(self._filename, "w", encoding="utf-8") as file:
            file.write(f"{self._headers}\n{self._body}")
            
        if self._filename[len(self._filename)-3:] == "csv":
            pdf_filename = f"{self._filename[:-3]}pdf"
            font = self._body_font if self._body_font else None
            headerfont = self._header_font if self._header_font else None
            csv2pdf.convert(self._filename, pdf_filename, align="L", font=font, headerfont=headerfont, headersize=14)
            
            
    @property
    def body(self):
        return self._body
    
    @property
    def get_date(self):
        return parse_date(self._game_date)
    
    @property
    def game_of_the_day(self):
        return get_max_possible_combination(self._game_date)
    
    def write_limited(self, output):
        # side effects
        self._filename = generate_absolute_filename(parent_dir=self._base_dir / "all", owner="all", date=self._game_date, filetype="csv")
        self._body = self._write_table_style(output)
        self._title = "ALL ENTRIES REPORT"

    def write_tulog(self, output):
        data = []
        for key in output:
            for entry_obj in output[key]:
                line = "-".join(map(str,[*entry_obj.combination, entry_obj.bet, entry_obj.owner]))
                data.append(line)
            data.append("")
        # side effects    
        self._filename = generate_absolute_filename(parent_dir=self._base_dir / "tulog", owner="tulog", date=self._game_date, filetype="txt")
        self._body = "\n".join(data)
        self._title = "TULOG REPORT"
    
    def write_draws_winners(self, output, winning_numbers):
        draws_list = []
        winners_list = []
        draws_total_bet = []
        winners_total_bet = []
        remits = []
        grand_total_remit = 0
        for owner, value in output.items():
            draws_list.extend(value["draws"])
            winners_list.extend(value["winners"])
            draws_total_bet.append(value["draws_total_bet"])
            winners_total_bet.append(value["winners_total_bet"])
            total_remit = self._game_bets[owner] * 0.55 - value["draws_total_bet"]
            grand_total_remit += total_remit
            remits.append(f"{owner.upper()} REMIT: ,{total_remit:.2f}")
        remits.append(f"GRAND TOTAL REMIT: ,{grand_total_remit:.2f}")    
        winners_str = self._write_table_style(winners_list)
        draws_str = self._write_table_style(draws_list)
        
        winners_total_bet_str = self._write_totals(category="WINNERS TOTAL BET: ", output=winners_total_bet)
        draws_total_bet_str = self._write_totals(category="DRAWS TOTAL BET: ", output=draws_total_bet)
        remit_total_str = "\n".join(remits)
        result = "-".join([str(number).zfill(2) for number in winning_numbers])
        
        # side effects
        self._filename = generate_absolute_filename(parent_dir=self._base_dir / "result", owner="result", date=self._game_date, filetype=".csv")
        self._body = f"WINNING NUMBERS:\n{result}\n\n{remit_total_str}\n\nWINNERS LIST\n{winners_str}\n{winners_total_bet_str}\nDRAWS LIST\n{draws_str}\n{draws_total_bet_str}\n"
        self._title = "WINNERS AND DRAWS REPORT"
        
    @property    
    def _headers(self):
        game_total_bet = 0
        metadata = [
            f"{self._title}",
            f"LOTTO 6/{self.game_of_the_day}: {'-'.join(self.get_date)}",
            ""
        ]
        if self._title != "TULOG REPORT":
            for owner, total_bet in self._game_bets.items():
                metadata.append(f"{owner.upper()} TOTAL: ,{total_bet}")
                game_total_bet += total_bet
            metadata.append(f"GRAND TOTAL: ,{game_total_bet}")
        metadata.append("")
        return "\n".join(metadata)
    
    
    ##################
    # HELPER METHODS #
    ##################
            
    def _write_table_style(self, output):
        data = {}
        for entry_obj in output:
            if entry_obj.owner not in data:
                data[entry_obj.owner] = []
            line = "-".join(map(str,[*entry_obj.combination, entry_obj.bet]))
            data[entry_obj.owner].append(line)
        entries_data_frame = pd.DataFrame(dict([(k, pd.Series(v)) for k, v in data.items()]))
        return entries_data_frame.to_csv(index=False, lineterminator="\n")
    
    def _write_totals(self, category, output):
        output_str = ",".join([str(out) for out in output])
        return f"{category}\n{output_str}\n"
    
    
    