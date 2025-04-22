from enum import Enum
import sys

from lotto.config import OWNERS, BASE_DIR, GAME_DATE

from lotto.utilities import (
    sync_file_read, 
    parse_read_file, 
    generate_absolute_filename,
    separator,
    combine_entries,
    FileWriter,
)

from lotto.entries import Entries

class Command(Enum):
    LIMITED = 1
    TULOG = 2
    WINNERS = 3
    WRONG_INPUT = 4

def run():
    clear_console()
    entries_tree = {}
    wrong_input_tree = {}
    game_bets_tree = {}
    
    for owner in OWNERS:
        filename = BASE_DIR / "input"
        filename = generate_absolute_filename(parent_dir=filename, owner=owner, date=GAME_DATE)
        parsed_entries = parse_read_file(sync_file_read(filename))
        wrong_input, valid_entries = separator(parsed_entries, owner, GAME_DATE)
        entries = Entries(valid_entries)
        entries_tree[owner] = entries
        wrong_input_tree[owner] = wrong_input
        game_bets_tree[owner] = entries.limited_entries(10).total_bet
        

    
    sys.stdout.write('Command me!\n')
    sys.stdout.write('Press 1 - Generate all entries list\n')
    sys.stdout.write('Press 2 - Generate tulog entries list\n')
    sys.stdout.write('Press 3 - Generate draw and winners entries list\n')
    sys.stdout.write('Press 4 - Report wrong input!\n\n')
    sys.stdout.flush()
    command = int(input("Press command number: "))
    
    clear_console()
    
    if command in [1,2,3]:
        file_writer = FileWriter(base_dir=BASE_DIR, game_date=GAME_DATE, game_bets=game_bets_tree)
        
        if command == Command.LIMITED.value:
            all_entries = []
            for owner, entries in entries_tree.items():
                all_entries.extend(entries.limited(limit=10))
            file_writer.write_limited(all_entries)
        elif command == Command.TULOG.value:
            sorted_entries = []
            for owner, entries in entries_tree.items():
                sorted_entries.append(entries.sort())
            combined_entries = combine_entries(sorted_entries)
            all_entries = Entries(combined_entries)
            tulog_entries = all_entries.tulog_items()
            file_writer.write_tulog(tulog_entries)    
        elif command == Command.WINNERS.value:
            winning_numbers = []
            for i in range(6):
                number = int(input(f"Winning Number {i+1}: "))
                winning_numbers.append(number)
            output = {}
            for owner, entries in entries_tree.items():
                draws, winners = entries.draws_and_winners_entries(winning_numbers)
                draws_total_bet = draws.limited_entries(limit=10).total_bet
                winners_total_bet = winners.limited_entries(limit=10).total_bet
                
                draws = draws.limited(10)
                winners = winners.limited(10)
                
                output[owner] = {
                    "draws": draws,
                    "winners": winners,
                    "draws_total_bet": draws_total_bet,
                    "winners_total_bet": winners_total_bet,
                }
                
            file_writer.write_draws_winners(output)
        
        file_writer.write()
        
    elif command == Command.WRONG_INPUT.value:
        wrong_input_reporter(wrong_input_tree)

        
def wrong_input_reporter(wrong_input_tree):
    sys.stdout.write(f'WRONG INPUT REPORT\n\n')
    for owner, wrong_entries in wrong_input_tree.items():
        sys.stdout.write(f'{owner}:\n')
        if len(wrong_entries) == 0:
            sys.stdout.write(f'No wrong input!\n')
        for line_number in sorted(wrong_entries):
            entry = wrong_entries[line_number]
            sys.stdout.write(f'Line number {line_number}: {entry}\n')
        sys.stdout.write(f"\n\n")
        
        
def clear_console():
    sys.stdout.write("\033[H\033[J")
    sys.stdout.flush()
    