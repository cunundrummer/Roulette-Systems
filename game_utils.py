import config


def readable_game_count(gc: int) -> int:
    return gc + 1


def get_stop_limit(br):
    return br + config.STOP_AFTER_WINNING_AMOUNT
