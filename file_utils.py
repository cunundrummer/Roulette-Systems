import pandas as pd
import os.path
from datetime import datetime


def create_filename(filename, f_extension='.csv'):
    """
    Creates the file with the filename provided.  To ensure uniqueness, it will append the date and time at the end.
    The default extension will be csv for easy integration with spreadsheets/dbases/etc...
    :param filename:
    :param f_extension:
    :return:
    """
    file = f'{filename + (str(datetime.now()).strip())}{f_extension}'
    print(f'Creating file: , {file}')
    return fr'{file}'


def save_to_csv(summary: list[dict], filename: str) -> None:
    print('Saving to .csv...')
    df = pd.DataFrame.from_records(summary)
    file = create_filename(filename)
    df.to_csv(file, index=False, header=True)


def record_result_to_dict(game_id: int, bankroll_start: int, round_ended_at: int, result_wl: str, amount: int) -> dict:
    return dict({'game': game_id,
                 'bankroll_at_start': bankroll_start,
                 'num_rounds': round_ended_at,
                 "win_lose": result_wl,
                 "amount": amount
                 })
