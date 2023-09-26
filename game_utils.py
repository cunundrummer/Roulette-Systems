import config


def readable_game_count(gc: int) -> int:
    return gc + 1


def get_stop_limit(br) -> int:
    """

    :param br: bankroll
    :return:
    """
    return br + config.STOP_AFTER_WINNING_AMOUNT


def calculate_winnings(bet: int, mp: int, include_initial_bet: bool = True) -> int:
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

    bets_total = sum(argv, 0)

    # condition1: if session bankroll <= 0
    if (bps - bets_total) <= 0:
        return {"result": True, "reason": 'Not enough funds to continue'}

    # condition2: if bets_total > MAX_BET
    if bets_total > max_bet:
        return {"result": True, "reason": 'Bet exceeds the maximum allowable bet'}

    return {"result": False, "reason": ''}
