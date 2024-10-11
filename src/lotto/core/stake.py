from src.lotto.core.entry import Entry

class Stake:
    def __init__(self, stake=None, owner="", limit=None):
        self.__stake = stake
        self.__owner = owner
        self.__limit = limit
        self.__game = None
        if len(self.__stake) > 0:
            self.__game = f"6/{self.__stake[0].game}"

    @property
    def game(self):
        return self.__game

    @property
    def total_bet(self):
        return sum([entry.original_bet for entry in self.all if not entry.ignore])
    
    @property
    def total_bet_w_limit(self):
        return sum([self.get_bet(self.all_dict[key]) for key in self.all_dict])
    
    @property
    def all(self):
        return sorted(tuple(self.__stake), key=lambda entry: entry.sorted_key)
    
    @property
    def all_dict(self):
        entries = {}
        for entry in self.__stake:
            if not entry.ignore:
                key = entry.sorted_key
                if key not in entries:
                    entries[key] = 0
                entries[key] += entry.original_bet
        return {key: entries[key] for key in sorted(entries)}
    
    @property
    def winners_dict(self):
        entries = {}
        for entry in self.__stake:
            if not entry.ignore and entry.iswinner:
                key = entry.sorted_key
                if key not in entries:
                    entries[key] = 0
                entries[key] += entry.original_bet
        return {key: entries[key] for key in sorted(entries)}
    
    @property
    def draw_dict(self):
        entries = {}
        for entry in self.__stake:
            if not entry.ignore and entry.isdraw:
                key = entry.sorted_key
                if key not in entries:
                    entries[key] = 0
                entries[key] += entry.original_bet
        return {key: entries[key] for key in sorted(entries)}
    
    @property
    def tulog_dict(self):
        entries = {}
        for entry in self.__stake:
            if not entry.ignore:
                key = entry.sorted_key
                if key not in entries:
                    entries[key] = {}
                if entry.owner not in entries[key]:
                    entries[key][entry.owner] = []
                entries[key][entry.owner].append(entry.original_bet)
        return {key: entries[key] for key in sorted(entries) if sum(len(entries[key][owner]) for owner in entries[key]) > 1}

        
            
    def get_bet(self, value):
        if self.limit and value and value < self.limit:
            return value
        return self.limit
            
    def __str__(self):
        return f"{'\n'.join([str(entry) for entry in self.all if not entry.status and not entry.ignore])}"
    
    @property
    def owner(self):
        return self.__owner
    
    @property
    def limit(self):
        return self.__limit
    
    @property
    def prepare_all(self):
        prepared = []
        header = f"\n{self.owner.upper()},COMBINATION,BET,BET W/ LIMIT,,,"
        prepared.append(header)
        all_keys = list(self.all_dict.keys())
        same_with_prev = False
        for index in range(len(self.all_dict)):
            entry = all_keys[index]
            next_entry = None
            line = ""
            if same_with_prev:
                line += "**"
                same_with_prev = False
            if index + 1 < len(self.all_dict):
                next_entry = all_keys[index + 1]
                same_entries = sum([1 for number in entry if number in next_entry])
                if same_entries == 2 and line == "":
                    line += "**"
                    same_with_prev = True
                else:
                    same_with_prev = False
            line += f",{'-'.join([str(combination) for combination in entry])},{self.all_dict[entry]},{self.get_bet(self.all_dict[entry])},,,"
            prepared.append(line)
        second_line = f"TOTAL BET,,{self.total_bet},{self.total_bet_w_limit},,,"
        prepared.append(second_line)
        return prepared
    
    @property
    def prepare_tulog(self):
        prepared = []
        header = f"OWNER,COMBINATION,BET,BET W/ LIMIT,,,"
        prepared.append(header)
        total_bet = 0
        total_bet_w_limit = 0
        for entry in self.tulog_dict:
            for owner in self.tulog_dict[entry]:
                for bet in self.tulog_dict[entry][owner]:
                    bet_w_limit = self.get_bet(bet)
                    total_bet += bet
                    total_bet_w_limit += bet_w_limit
                    line = f"{owner.upper()},{'-'.join([str(combination) for combination in entry])},{bet},{bet_w_limit},,,"
                    prepared.append(line)
            prepared.append("")
        second_line = f"TOTAL BET,,{total_bet},{total_bet_w_limit},,,"
        prepared.append(second_line)
        
        return prepared
    
    def set_stake_winners(self, winning_numbers=None):
        for entry in self.__stake:
            entry.set_winner(winning_numbers)
    
    @property
    def prepare_winners(self):
        prepared = []
        prepared_dict = self.winners_dict
        header = f"{self.owner.upper()},COMBINATION,BET,BET W/ LIMIT,,,"
        prepared.append(header)
        total_bet = 0
        total_bet_w_limit = 0
        for entry in prepared_dict:
            total_bet += prepared_dict[entry]
            total_bet_w_limit += self.get_bet(prepared_dict[entry])
            line = f",{'-'.join([str(combination) for combination in entry])},{prepared_dict[entry]},{self.get_bet(prepared_dict[entry])},,,"
            prepared.append(line)
        second_line = f"TOTAL BET,,{total_bet},{total_bet_w_limit},,,"
        prepared.append(second_line)
        return prepared
    
    @property
    def prepare_draw(self):
        
        prepared = []
        prepared_dict = self.draw_dict
        header = f"{self.owner.upper()},COMBINATION,BET,BET W/ LIMIT,,,"
        prepared.append(header)
        total_bet = 0
        total_bet_w_limit = 0
        for entry in prepared_dict:
            total_bet += prepared_dict[entry]
            total_bet_w_limit += self.get_bet(prepared_dict[entry])
            line = f",{'-'.join([str(combination) for combination in entry])},{prepared_dict[entry]},{self.get_bet(prepared_dict[entry])},,,"
            prepared.append(line)
        second_line = f"TOTAL BET,,{total_bet},{total_bet_w_limit},,,"
        total_remit = (self.total_bet  * 0.55) - total_bet
        total_remit_w_limit = (self.total_bet_w_limit * 0.55) - total_bet
        remit_line = f"REMIT,,{total_remit},{total_remit_w_limit},,,"
        prepared.append(second_line)
        prepared.append(remit_line)
        return prepared