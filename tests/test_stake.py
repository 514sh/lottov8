from src.lotto.core.stake import Stake

def test_stake_class_creation():
    stake = Stake(stake=["",])
    assert isinstance(stake, Stake)