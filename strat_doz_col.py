import config
import game_utils
from config import set_max_bet, COLUMN2, DOZENS2, COLUMNS_MP
from file_utils import record_result_to_dict
import random

STRAT_NAME = 'Dozen and column'
ROUNDS_MAX = 500
MAX_BET = set_max_bet(2000)  # Max bet for outsides is usually different from inside max bets
UNIT = 10
ORIGINAL_BANKROLL = 2000


def describe() -> None:
    """
    A detailed step by step description of the system.
    :return:
    """
    print(f'Strategy name: \n  {STRAT_NAME}')
    print(f'Start with original bankroll: \n  {ORIGINAL_BANKROLL}')
    print(f'Will always continue with orig. bankroll or start with cumulative bankroll? \n ',
          'Original' if not config.start_with_last_bankroll else 'Cumulative (continuous)')
    print('Always keeps track of session high(S.H.) | (all time high (A.T.H.).  The S.H. '
          f'starts with the beginning bankroll (ex. 2000).')
    print(f'Always start with 1 unit({UNIT}) on a dozen, and 1 unit({UNIT}) on a column.')
    print(f'On loss: \n  increment a unit({UNIT}) or until broke.')
    print('On win:')
    print(f'  if winning and amount is >= A.T.H., reset bet back to 1 unit({UNIT}) on the respective dozen, column')
    print(f'  if the bankroll < S.H, the bet remains unchanged. '
          f'Ex. S.H = $2000, current bankroll = $1990, current bet = $30/area; the bet will remain $30/area.')
    print(f'The game will continue until either:')
    print(f'  {game_utils.get_stop_limit(ORIGINAL_BANKROLL)}(the bankroll + {config.STOP_AFTER_WINNING_AMOUNT}) '
          f'is reached (stop limit)...')
    print(f'  the max number of rounds ({config.ROUNDS_MAX} have been iterated through...')
    print(f'  cannot make a bet because of lack of bankroll funds.')
    print('\n ----------------------------------------------------------------------------------------------------- \n')


def record_total_loss(gc, bps: int, bankroll: int, last_round: int, wl: str) -> dict:
    """
    at the moment, this function is called 'handle'_total_loss.  It may be changed to record_total_loss
    :param gc: game count
    :param bps: bankroll per session
    :param bankroll: starting bankroll
    :param last_round: the last round played at end
    :param wl: win ('w') or loss ('l)
    :return: dict
    """
    print(f'TOTAL LOSS on round {last_round}')
    print('-- recording result for loss...')
    return record_result_to_dict(game_id=gc, bankroll_start=bankroll, round_ended_at=last_round,
                                 result_wl=wl, amount=bps)


def strat_dozs_and_cols(games_count: int, bankroll: int) -> dict:
    """

    :param games_count:
    :param bankroll:
    :return:
    """
    gc = game_utils.readable_game_count(games_count)
    stop_limit_by_amount = config.STOP_AFTER_WINNING_AMOUNT + bankroll  # +300
    print('\n-------- New Game Started -------- : ', gc)

    nums = list()  # will keep for history
    rounds = 0
    bankroll_per_session = bankroll  # the running total bankroll
    bet_col = 10
    bet_doz = 10
    ath = 2000

    results: dict = {}  # prepare new results

    while rounds < ROUNDS_MAX and bankroll_per_session <= stop_limit_by_amount:
        print(f'GAME: {gc} :: Round: {rounds + 1}')

        # make the bet before getting the 'number'
        print('Making bet before spinning for number...')
        print(f'Betting {bet_doz} on doz2, {bet_col} on col2')
        print(f'Bankroll: {bankroll_per_session} - {bet_col} - {bet_doz}: ')

        bankroll_per_session = bankroll_per_session - bet_col - bet_doz

        print(f'        = {bankroll_per_session}')

        num = random.randint(0, 36)
        nums.append(num)
        print(f'Number: {num}')

        winnings = 0
        losses = 0

        if num in COLUMN2:
            print('winner col2')
            winnings = winnings + (bet_col * COLUMNS_MP) + bet_col
            print(f'+{winnings}: {bet_col} * {COLUMNS_MP} [+ {bet_col}]')
        else:
            losses = losses + 1
            print(f'Lost {bet_col} on columns2')

        if num in DOZENS2:
            print('winner doz2')
            winnings = winnings + (bet_doz * COLUMNS_MP) + bet_doz
            print(f'+{winnings}: {bet_doz} * {COLUMNS_MP} [+ {bet_doz}]')
        else:
            losses = losses + 1
            print(f'Lost {bet_doz} on dozens2')

        bankroll_per_session = bankroll_per_session + winnings

        print(f'Losses total: {losses}')
        print(f'Bankroll: {bankroll_per_session}')

        if bankroll_per_session > ath:
            ath = bankroll_per_session
            print(f'New ATH: {ath}')

        # determine bet reset
        if winnings > 0:
            losses = 0  # no need to increment bets unit
            if bankroll_per_session >= ath:
                print(f'RESETTING BETS to {UNIT}')
                bet_doz = UNIT
                bet_col = UNIT

        if losses > 0:
            bet_col = bet_col + UNIT
            bet_doz = bet_doz + UNIT

        # on lose session:
        if game_utils.is_total_loss(bankroll_per_session, MAX_BET, bet_col, bet_doz).get('result'):
            print(f'TOTAL LOSS on round {rounds}')
            print('-- recording result for loss...')
            results.update(
                record_result_to_dict(game_id=gc, bankroll_start=bankroll, round_ended_at=rounds,
                                      result_wl="l", amount=bankroll_per_session)
            )
            rounds = ROUNDS_MAX  # end session because of loss limit reach
            continue

        # on win session:
        if (rounds == ROUNDS_MAX and bankroll_per_session >= 0) or bankroll_per_session >= stop_limit_by_amount:
            print('-- recording result for win...')
            results.update(
                record_result_to_dict(game_id=gc, bankroll_start=bankroll, round_ended_at=rounds,
                                      result_wl="w", amount=bankroll_per_session)
            )
            rounds = ROUNDS_MAX  # end session because of win limit reached

        rounds = rounds + 1
        print()
    print('Results from strat_doz_col.py', results)
    return results
