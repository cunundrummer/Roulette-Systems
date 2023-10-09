import random
import config
from custom_types import Bet_data


def readable_game_count(gc: int) -> int:
    return gc + 1


def get_stop_limit(br) -> int:
    """

    :param br: bankroll
    :return:
    """
    return br + config.STOP_AFTER_WINNING_AMOUNT


def generate_number(start_at, range_end):
    return random.randint(start_at, range_end)


def place_bet(how_much: int, where: int) -> Bet_data:
    return {'bet': how_much, 'location': where}


def bets_total(bets: list[Bet_data]) -> int:
    """
    calculate specifically the total of bets for the list of bets(bet_data)
    :param bets:
    :return:
    """
    return sum([d.get('bet') for d in bets])


def calc_winnings(bet: int, mp: int, include_initial_bet: bool = True) -> int:
    """ Calculates the winnings.  Optionally include the original bet. Ex.  if winning on a 2:1 multiplier,
    you can return simply that.  But the real amount usually includes the initial bet, so it would more likely be a
    3:1 bet.
    """

    if include_initial_bet:
        return (bet * mp) + bet  # adjusted 3:1
    return bet * mp  # orig 2:1


def set_max_bet(m_bet=config.DEFAULT_MAX_BET_OUTSIDES) -> int:
    return m_bet


def is_total_loss(bps: int, max_bet: int,  *argv) -> dict[str, bool | str]:
    """
    Determines the conditions of a total loss

    :rtype: object
    :param bps: bankroll per session
    :param max_bet: maximum allowable bet
    :param argv: bets values
    :return: dict["result": bool, "reason": str | None]
    """

    total = sum(argv, 0)

    # condition1: if session bankroll <= 0
    if (bps - total) <= 0:
        return {"result": True, "reason": 'Not enough funds to continue'}

    # condition2: if total > MAX_BET
    if total > max_bet:
        return {"result": True, "reason": 'Bet exceeds the maximum allowable bet'}

    return {"result": False, "reason": ''}


def calc_percentage(br, percentage_required) -> int:
    return (percentage_required / 100) * br


def get_readable_location(where: int) -> str | None:
    for el in config.LOCATIONS_OBJ:
        if el.get('id') == where:
            return el.get('readable')
    return None


def is_number_exist_in_location_by_id(num: int, location: int) -> bool:
    """
    :param num: Spun num.
    :param location: int -> the location id of the table area.
    :return: bool
    """
    for el in config.LOCATIONS_OBJ:
        if num in el.get('numbers') and location == el.get('id'):
            return True
    return False


def generate_win_loss_report(game_num: int, round_num: int, spun_num: int, bet_locations_w_bets: list[Bet_data]):
    """

    :param game_num:
    :param round_num:
    :param spun_num:
    :param bet_locations_w_bets: list[dict[int, int]]
    :deprecated bets: All the bets. Can be different amounts depending on the strategy being used.
    :return:
    """
    print('*************************************************')
    print(f'Game: {game_num} :: Round: {round_num} :: Number: {spun_num}')

    print('Bets:')
    for bet in bet_locations_w_bets:
        bet_amount = bet.get("bet")
        readable_location = get_readable_location(bet.get("location"))
        win_loss_result = 'W' if is_number_exist_in_location_by_id(spun_num, bet.get("location")) else 'L'
        print(f'  ${str(bet_amount)} @ {readable_location}: {win_loss_result}')
    print('*************************************************')