import file_utils
import strat_doz_col
from config import *
from strat import strat_
from strat_doz_col import *
from system_names import sys2

system = sys2

if __name__ == '__main__':
    games_max = GAMES
    games_count = 0
    results = list()
    IMMUTABLE_BANKROLL: int = 2000

    if DESCRIBE_STRAT:
        strat_doz_col.describe()

    bankroll: int = IMMUTABLE_BANKROLL

    while games_count < games_max:  # games loop !!! NOT the rounds per game!
        # results.append(strat_dozs_and_cols(games_count=games_count, bankroll=bankroll))  # strat1
        results.append(strat_(games_count=games_count, bankroll=bankroll))  # strat2

        if config.start_with_last_bankroll:
            print('Inspect', results)
            bankroll = results[games_count].get('amount')

        if bankroll < IMMUTABLE_BANKROLL:
            games_count = games_max

        if bankroll > IMMUTABLE_BANKROLL:
            games_count = games_count + 1

    print('After game completion, results: ', results)

    for r in results:
        print(r)

    if save_to_csv:
        file_utils.save_to_csv(results, sys2.get('holy_grail_v1'))
