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
        self.__iswinner = False
        self.__isdraw = False
    
    @property
    def iswinner(self):
        return self.__iswinner
    
    @property
    def isdraw(self):
        return self.__isdraw
    
    @property
    def original(self):
        return self.__original
    
    @property
    def sorted_key(self):
        return tuple(sorted(self.clean_entry[:3]))
    
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
    

    def __duplicated_entry(self):
        return len(self.sorted_key) != 3
    
    def __wrong_bet(self):
        return self.original_bet % 5 != 0
    
    def __highest_combination_today(self):
        weekday = datetime.today().weekday()
        highest_per_weekday = [45,49,45,49,45,42,49]
        return highest_per_weekday[weekday]

    
    def __exceeded_highest_possible(self):
        for entry in self.sorted_key:
            if entry > self.__highest_combination_today():
                return True
        return False
    
    def __set_status(self):
        self.__status = not (self.__duplicated_entry() or self.__wrong_bet() or self.__exceeded_highest_possible())
    
    def set_winner(self, winning_numbers=None):
        if not self.ignore:
            guesses = 0
            if winning_numbers:
                for number in self.sorted_key:
                    if number in winning_numbers:
                        guesses +=1
            if guesses >= 3:
                self.__iswinner = True
            elif guesses == 2:
                self.__isdraw = True
    
    def __eq__(self, value: object) -> bool:
        if self.sorted_key == value.sorted_key:
            return True
        return False
    
    def __str__(self):
        return f"{self.owner.upper()} - Line number {self.line_number}: {self.original}"