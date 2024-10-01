from src.lotto.core.entry import Entry

class Stake:
    def __init__(self, stake=None, owner="", limit=None):
        self.__stake = stake
        self.__owner = owner
        self.__limit = limit
    
    @property
    def total_bet(self):
        return sum([entry.original_bet for entry in self.all if not entry.ignore])
    
    @property
    def all(self):
        return sorted(
            [
                Entry(entry=entry, owner=self.__owner, line_number=index+1, limit=self.__limit) 
                for index,entry in enumerate(self.__stake)
            ], 
            key=lambda entry: entry.sorted_key)
            
    def __str__(self):
        return f"{'\n'.join([str(entry.sorted_key) for entry in self.all])}"
    
    @property
    def owner(self):
        return self.__owner
    
    @property
    def prepare_all(self):
        prepared = []
        header = f"{self.owner.upper()},C1,C2,C3,BET,ORIGINAL,,,"
        second_line = f"TOTAL BET: {self.total_bet},,,,,,,,"
        prepared.append(header)
        prepared.append(second_line)
        for entry in self.all:
            if entry.ignore:
                continue
            line = f",{','.join([str(combination) for combination in entry.sorted_key])},{entry.original_bet},{entry.semi_orig},,,"
            prepared.append(line)
        
        return prepared