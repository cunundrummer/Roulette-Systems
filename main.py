import file_utils
import strat_doz_col
from config import *
from strat_doz_col import *


def calculate_winnings(bet: int, mp: int, include_initial_bet: bool = True) -> int:
    """ Calculates the winnings.  Optionally include the original bet. Ex.  if winning on a 2:1 multiplier,
    you can return simply that.  But the real amount usually includes the initial bet, so it would more likely be a
    3:1 bet.
    """

    if include_initial_bet:
        return (bet * mp) + bet  # adjusted 3:1
    return bet * mp  # orig 2:1


if __name__ == '__main__':
    games_max = GAMES
    games_count = 0
    results = list()

    if DESCRIBE_STRAT:
        strat_doz_col.describe()

    bankroll = ORIGINAL_BANKROLL

    while games_count < games_max:
        results.append(strat_dozs_and_cols(games_count=games_count, bankroll=bankroll))

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
