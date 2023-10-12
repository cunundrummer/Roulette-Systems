import file_utils
import config
from system_names import strat_holy_grail_v1

system = strat_holy_grail_v1  # choose a system from system names to play out.

if __name__ == '__main__':
    games_max = config.GAMES  # max games to simulate
    games_count = 0
    results = list()
    IMMUTABLE_BANKROLL: int = 2000

    if config.DESCRIBE_STRAT:
        system.describe()

    bankroll: int = IMMUTABLE_BANKROLL

    while games_count < games_max:  # games loop !!! NOT the rounds per game!

        # play a single (subject to change possibly) strategy and get its results
        results.append(system.get('fn')(games_count=games_count, bankroll=bankroll))

        # if previous iteration is >= 2000 (2###), start with (2####)
        if config.start_with_last_bankroll and bankroll >= IMMUTABLE_BANKROLL:
            print('Inspect', results)
            bankroll = results[games_count].get('amount')
            games_count = games_count + 1

        # should always start new simulation with 'immutable' bankroll (ex. always start with 2000)
        if not config.start_with_last_bankroll and bankroll >= IMMUTABLE_BANKROLL:
            games_count = games_count + 1

        # should not be allowed to continue -> defend against players risk of ruin
        if bankroll < IMMUTABLE_BANKROLL:
            games_count = games_max

    print('After game completion, results: ', results)

    for r in results:
        print(r)

    if config.save_to_csv:
        file_utils.save_to_csv(results, system.get('name'))
