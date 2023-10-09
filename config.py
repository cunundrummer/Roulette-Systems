start_with_last_bankroll: bool = True
save_to_csv: bool = False

DEFAULT_MAX_BET_OUTSIDES = 2000
ROUNDS_MAX = 500
GAMES = 100
STOP_AFTER_WINNING_AMOUNT = 500
WIN = 'w'
LOSS = 'l'

DESCRIBE_STRAT = False  # intention: before running the strategy, describe it?

BLACKS = [15, 4, 2, 17, 6, 13, 11, 8, 10, 24, 33, 20, 31, 22, 29, 28, 35, 26]
REDS = [32, 19, 21, 25, 34, 27, 36, 30, 23, 5, 16, 1, 14, 9, 18, 7, 12, 3]
COLUMN1 = [1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 31, 34]
COLUMN2 = [2, 5, 8, 11, 14, 17, 20, 23, 26, 29, 32, 35]
COLUMN3 = [3, 6, 9, 12, 15, 18, 21, 24, 27, 30, 33, 36]
DOZENS1 = list(range(1, 13))
DOZENS2 = list(range(13, 25))
DOZENS3 = list(range(25, 37))

DOZENS_MP = 2
COLUMNS_MP = 2

DOZENS1_ID = 40
DOZENS2_ID = 41
DOZENS3_ID = 42

DOZENS1_dict = {'id': DOZENS1_ID, 'numbers': DOZENS1, 'readable': '1st 12'}
DOZENS2_dict = {'id': DOZENS2_ID, 'numbers': DOZENS2, 'readable': '2nd 12'}
DOZENS3_dict = {'id': DOZENS3_ID, 'numbers': DOZENS3, 'readable': '3rd 12'}

LOCATIONS_OBJ = [DOZENS1_dict, DOZENS2_dict, DOZENS3_dict]