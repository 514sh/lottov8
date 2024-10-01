import re
from datetime import datetime

class Entry:
    def __init__(self, entry="", owner="", line_number=None, limit=None):
        self.__original = entry.strip()
        self.__owner = owner
        self.__line_number=line_number
        self.__status = None
        self.__limit = limit
        self.__set_status()
    
    @property
    def original(self):
        return self.__original
    
    @property
    def sorted_key(self):
        return tuple(sorted(self.entry_set))
    
    @property
    def owner(self):
        return self.__owner
    
    @property
    def line_number(self):
        return self.__line_number
    
    @property
    def limit(self):
        return self.__limit
    
    @property
    def ignore(self):
        return len(self.clean_entry) <= 1
    
    @property
    def used_bet(self):
        if self.__limit:
            return self.original_bet if self.__limit >= self.original_bet else self.__limit
        return self.original_bet
    
    @property
    def status(self):
        return self.__status
    
    @property
    def clean_entry(self):
        split_entry = re.split("[^0-9]", self.original)
        return [int(i) for i in split_entry if i != ""]
    
    @property
    def semi_orig(self):
        if not self.ignore:
            return "-".join([str(c) for c in self.clean_entry])
    
    @property
    def original_bet(self):
        if not self.ignore:
            return self.clean_entry[-1]
        return 0
    
    @property
    def entry_set(self):
        my_set = set()
        for entry in self.clean_entry[:3]:
            my_set.add(entry)
        return frozenset(my_set)

    def __duplicated_entry(self):
        return len(self.entry_set) != 3
    
    def __wrong_bet(self):
        return self.original_bet % 5 != 0
    
    def __highest_combination_today(self):
        weekday = datetime.today().weekday()
        highest_per_weekday = [45,45,45,45,45,45,45]
        return highest_per_weekday[weekday]
    
    def __exceeded_highest_possible(self):
        for entry in self.entry_set:
            if entry > self.__highest_combination_today():
                return True
        return False
    
    def __set_status(self):
        self.__status = not (self.__duplicated_entry() or self.__wrong_bet() or self.__exceeded_highest_possible())
    
    def __eq__(self, value: object) -> bool:
        if self.entry_set == value.entry_set:
            return True
        return False
    
    def __str__(self):
        return f"{self.owner.upper()} - Line number {self.line_number}: {self.original}"