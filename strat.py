import config
import game_utils
from custom_types import Bet_data

reset_at_profit_of = 150  # Found state machine library.  In the meantime, continue with simple states
bankroll_required = 2000  # buy in
cashout = game_utils.calc_percentage(bankroll_required, 15)
ORIG_UNIT_AMOUNT = 10


# holy grail (advantage play)
# bets on the 1st and 2nd dozen
# lose: +1 unit
# win: same unit on each bet
# everytime reach 150, reset to single 10 unit


def get_reset_levels(current_bankroll: int, old_reset_level_amount: int) -> int:
    """
    This function will determine the appropriate level to reset to.  Still undetermined if this will be needed, but
    I have to clarify what if possible will happen if I surpass another level. ex.
    reset @ 150 profit and starting from 2000
    reached 2170. reset new level to 2300.  But what happens if somehow I get 2470 coming out of a losing streak? The
    reset would have to be at 2450 (2150 - 2300 - 2450 -2600, etc...)
    :return:
    """
    if current_bankroll < old_reset_level_amount:
        return old_reset_level_amount

    while current_bankroll > old_reset_level_amount:
        old_reset_level_amount = old_reset_level_amount + reset_at_profit_of
    return old_reset_level_amount


def strat_(games_count: int = None, bankroll: int = None):
    gc = game_utils.readable_game_count(games_count)

    # Calculate the stop limit by adding the winning amount and bankroll
    stop_limit_by_amount = config.STOP_AFTER_WINNING_AMOUNT + bankroll  # +300
    print('\n-------- New Game Started -------- : ', gc)

    rounds = 0
    bankroll_per_session = bankroll  # the running total bankroll
    reset_at = bankroll + reset_at_profit_of
    bets_locations = list()
    units = 10
    prev_reset_at_lvl = reset_at

    nums_history = list()
    results: dict = {}  # prepare new results

    # strategy loop
    while rounds < config.ROUNDS_MAX and bankroll_per_session <= stop_limit_by_amount:
        # place bet; Some systems will require a specific trigger to place bets.  Keep this in mind!
        bets_locations.append(game_utils.place_bet(units, config.DOZENS1_ID))
        bets_locations.append(game_utils.place_bet(units, config.DOZENS2_ID))

        total_bets = game_utils.bets_total(bets_locations)
        bankroll_per_session = bankroll_per_session - total_bets  # bet_doz_1 - bet_doz_2
        print(f'After bet({total_bets}), bankroll: {bankroll_per_session}')

        # get number
        num = game_utils.generate_number(0, 36)
        nums_history.append(num)
        print(f'Number: {num}')

        # find winners/losers
        for bet_data in bets_locations:
            if game_utils.is_number_exist_in_location_by_id(num, bet_data.get('location')):
                print('Win')
                winnings = game_utils.calc_winnings(bet_data.get('bet'), config.DOZENS_MP)
                print('+', winnings)
                bankroll_per_session = bankroll_per_session + winnings
                print(f'New bankroll(session): {bankroll_per_session}')
                reset_at = get_reset_levels(bankroll_per_session, reset_at)
                if reset_at == prev_reset_at_lvl:  # condition for reset to new level met. Set new level & reset units.
                    prev_reset_at_lvl = reset_at
                    units = ORIG_UNIT_AMOUNT
                    print('New reset: ', reset_at)
                print('Unit amount:', units)
            else:
                print('Lose')
                units += ORIG_UNIT_AMOUNT  # on every loss increase a unit (per system)

        game_utils.generate_win_loss_report(0, rounds, num, bets_locations)
        rounds = config.ROUNDS_MAX
