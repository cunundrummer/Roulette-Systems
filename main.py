import file_utils
import strat_doz_col
from config import *
from strat import strat_
from strat_doz_col import *


if __name__ == '__main__':
    games_max = GAMES
    games_count = 0
    results = list()

    if DESCRIBE_STRAT:
        strat_doz_col.describe()

    bankroll = ORIGINAL_BANKROLL

    while games_count < games_max:  # games loop !!! NOT the rounds per game!
        # results.append(strat_dozs_and_cols(games_count=games_count, bankroll=bankroll))  # strat1
        results.append(strat_(games_count=games_count, bankroll=bankroll))  # strat2

        if config.start_with_last_bankroll:
            print('Inspect', results)
            bankroll = results[games_count].get('amount')

        if bankroll < ORIGINAL_BANKROLL:
            games_count = games_max

        if bankroll > ORIGINAL_BANKROLL:
            games_count = games_count + 1

    print('After game completion, results: ', results)

    for r in results:
        print(r)

    if save_to_csv:
        file_utils.save_to_csv(results, 'roulette_results_cols_and_doz')

# print(bet_total([{"bet": 10, "where": 40}, {"bet": 10, "where": 40}]))
