from enum import Enum
import sys

from lotto.config import OWNERS, BASE_DIR, GAME_DATE, LIMIT, HEADER_FONT, BODY_FONT

from lotto.utilities import (
    sync_file_read, 
    parse_read_file, 
    generate_absolute_filename,
    separator,
    combine_entries,
    FileWriter,
)

from lotto.entries import Entries, Entry

class Command(Enum):
    LIMITED = 1
    TULOG = 2
    WINNERS = 3
    WRONG_INPUT = 4


def run(
    limit=LIMIT,
    base_dir=BASE_DIR,
    owners=OWNERS,
    game_date=GAME_DATE,
    header_font=HEADER_FONT,
    body_font=BODY_FONT,
    ):
    
    clear_console()
    entries_tree, wrong_input_tree, game_bets_tree = load_entries(base_dir, owners, game_date, limit)
    command = get_user_command()
    clear_console()
    handle_command(
        command=command,
        entries_tree=entries_tree,
        wrong_input_tree=wrong_input_tree,
        game_bets_tree=game_bets_tree,
        base_dir=base_dir,
        limit=limit,
        game_date=game_date,
        header_font=header_font,
        body_font=body_font,
    )
    
            
def handle_command(command, entries_tree, wrong_input_tree, game_bets_tree, base_dir, limit, game_date, header_font, body_font):
    if command != Command.WRONG_INPUT.value:
        file_writer = FileWriter(base_dir=base_dir, game_date=game_date, game_bets=game_bets_tree, header_font=header_font, body_font=body_font)
        
        if command == Command.LIMITED.value:
            process_limited_entries(file_writer, entries_tree, limit)
        elif command == Command.TULOG.value:
            process_tulog_entries(file_writer, entries_tree)  
        elif command == Command.WINNERS.value:
            process_draws_and_winners_entries(file_writer, entries_tree, limit)
            
        file_writer.write() 
    else:
        cli_reporter(input_tree=wrong_input_tree, title="WRONG INPUT REPORT")
        

def process_limited_entries(file_writer, entries_tree, limit):
    all_entries = []
    for owner, entries in entries_tree.items():
        all_entries.extend(entries.limited(limit=limit))
    file_writer.write_limited(all_entries)

def process_tulog_entries(file_writer, entries_tree):
    sorted_entries = []
    for owner, entries in entries_tree.items():
        sorted_entries.append(entries.sort())
    combined_entries = combine_entries(sorted_entries)
    all_entries = Entries(combined_entries)
    tulog_entries = all_entries.tulog_items()
    file_writer.write_tulog(tulog_entries)   

def process_draws_and_winners_entries(file_writer, entries_tree, limit):
    winning_numbers = collect_winning_numbers()
    winners_tree, output = get_draws_winners_data(entries_tree, winning_numbers, limit)
    file_writer.write_draws_winners(output, winning_numbers)
    cli_reporter(input_tree=winners_tree, title="WINNERS REPORT")    
        
def load_entries(base_dir, owners, game_date, limit):
    entries_tree = {}
    wrong_input_tree = {}
    game_bets_tree = {}
    
    for owner in owners:
        filename = base_dir / "input"
        filename = generate_absolute_filename(parent_dir=filename, owner=owner, date=game_date)
        parsed_entries = parse_read_file(sync_file_read(filename))
        wrong_input, valid_entries = separator(parsed_entries, owner, game_date)
        entries = Entries(valid_entries)
        entries_tree[owner] = entries
        wrong_input_tree[owner] = wrong_input

        game_bets_tree[owner] = entries.limited_entries(limit).total_bet
    
    return entries_tree, wrong_input_tree, game_bets_tree

def get_user_command():
    sys.stdout.write('Command me!\n')
    sys.stdout.write('Press 1 - Generate all entries list\n')
    sys.stdout.write('Press 2 - Generate tulog entries list\n')
    sys.stdout.write('Press 3 - Generate draw and winners entries list\n')
    sys.stdout.write('Press 4 - Report wrong input!\n\n')
    sys.stdout.flush()
    
    command = input("Press command number: ")
    if command not in [str(c.value) for c in Command]:
        raise ValueError("Error from user: Invalid command. Please enter a number between 1 and 4.")

    return int(command)

        
def cli_reporter(input_tree, title=""):
    sys.stdout.write(f'{title}\n\n')
    for owner, entries in input_tree.items():
        sys.stdout.write(f'{owner}:\n')
        if len(entries) == 0:
            no_report = "No wrong input!" if title == "WRONG INPUT REPORT" else "No winners!"
            sys.stdout.write(f'{no_report}\n')
        for line_number in sorted(entries):
            raw_entry = ""
            if isinstance(entries[line_number], Entry):
                entry = entries[line_number]
                raw_entry = entry.raw_entry
            else:
                raw_entry = entries[line_number]
            sys.stdout.write(f'Line number {line_number}: {raw_entry}\n')
        sys.stdout.write(f"\n\n")
        
        
def clear_console():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()


def get_draws_winners_data(entries_tree, winning_numbers, limit):
    winners_tree = {}  # used in CLI reporting
    output = {}  # used in CSV reporting
    for owner, entries in entries_tree.items():
        draws, winners = entries.draws_and_winners_entries(winning_numbers)

        draws_total_bet = draws.limited_entries(limit=limit).total_bet
        winners_total_bet = winners.limited_entries(limit=limit).total_bet
        
        draws = draws.limited(limit=limit)
        winners = winners.limited(limit=limit)

        winners_tree[owner] = {entry.line_number: entry.raw_entry for entry in winners}
        
        output[owner] = {
            "draws": draws,
            "winners": winners,
            "draws_total_bet": draws_total_bet,
            "winners_total_bet": winners_total_bet,
        }
    return winners_tree, output    
    
def collect_winning_numbers():
    winning_numbers = []
    for i in range(6):
        try:
            number = int(input(f"Winning Number {i+1}: "))
        except ValueError:
            raise ValueError("Error from user: Invalid input for winning number.")
        winning_numbers.append(number)
    return winning_numbers
