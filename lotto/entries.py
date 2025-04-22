import re

from typing import List

class Entry:
    def __init__(self, line_number: int, entry: str, owner: str):
        self._line_number = line_number
        self._raw_entry = entry
        self._owner = owner
        split_entry = re.split(r"[^0-9]", entry)
        self._entry = [int(i) for i in split_entry if i != ""]
        self._combination = self._entry[:3]
        self._bet = self._entry[3]
    
    @property
    def line_number(self):
        return self._line_number
    
    @property
    def owner(self):
        return self._owner
    
    @property
    def raw_entry(self):
        return self._raw_entry
    
    @property
    def combination(self):
        return tuple(sorted(self._combination))
    
    def new_entry(self, bet: int):
        new_entry = "-".join(map(str,[*self.combination, bet]))
        return Entry(self.line_number, new_entry, self.owner)
    
    @property
    def bet(self):
        return self._bet
    
    def __eq__(self, other):
        return self.combination == other.combination
    
    def __hash__(self):
        return hash((*self.combination,self.owner,self.bet,self.line_number))
    
    def __lt__(self, other):
        return (*self.combination, self.owner, self.bet, self.line_number) < (*other.combination, other.owner, other.bet, other.line_number)
    
    def __repr__(self):
        return f"Entry(line={self.line_number}, owner={self.owner}, combination={self.combination}, bet={self.bet})"
    
    
class Entries:
    def __init__(self, entries: list):
        self._entries:List[Entry] = []
        total_bet = 0
        for entry in entries:
            new_entry = None
            if isinstance(entry, tuple):
                new_entry = Entry(*entry)
            else:
                new_entry = entry
            total_bet += new_entry.bet    
            self._entries.append(new_entry)
            
        self._total_bet = total_bet
        self._entries = sorted(self._entries)
        
    def sort(self):
        return self._entries
    
    @property
    def total_bet(self):
        return self._total_bet
    
    def limited_entries(self, limit):
        entries = self.limited(limit)
        return Entries(entries)
    
    def limited(self, limit):
        limited_entries = []
        prev_entry = None
        entry_total_bet = 0
        for entry_obj in self._entries:
            if prev_entry is not None and prev_entry != entry_obj:
                entry_total_bet = min(entry_total_bet, limit)
                new_entry = prev_entry.new_entry(bet=entry_total_bet)
                limited_entries.append(new_entry)
                entry_total_bet = 0
            entry_total_bet += entry_obj.bet
            prev_entry = entry_obj
            
        if prev_entry:
            entry_total_bet = min(entry_total_bet, limit)
            new_entry = prev_entry.new_entry(bet=entry_total_bet)
            limited_entries.append(new_entry)
        
        return limited_entries
    
    def tulog_items(self):
        tulog_entries = {}
        prev_entry = None
        tulog_lines = []
        for entry_obj in self._entries:
            if prev_entry is not None and prev_entry != entry_obj:
                if len(tulog_lines) >= 2:
                    tulog_entries[prev_entry.combination] = tulog_lines
                tulog_lines = []
            tulog_lines.append(entry_obj)
            prev_entry = entry_obj
        if len(tulog_lines) >= 2:
            tulog_entries[prev_entry.combination] = tulog_lines
            
        return tulog_entries
    
    def draws_and_winners_entries(self, winning_numbers):
        draw_entries = []
        winners_entries = []
        for entry_obj in self._entries:
            score = self._get_score(entry_obj, winning_numbers)
            if score == 3:
                winners_entries.append(entry_obj)
            elif score == 2:
                draw_entries.append(entry_obj)
        return Entries(draw_entries), Entries(winners_entries)
        
    @staticmethod
    def _get_score(entry, winning_numbers: list):
        score = 0
        for number in entry.combination:
            if number in winning_numbers:
                score+= 1
        return score
    
    def __getitem__(self, index):
        return self._entries[index]
    
    def __len__(self):
        return len(self._entries)