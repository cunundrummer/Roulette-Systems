from holy_grail_v1 import holy_grail_v1 as holy_grail_1
from strat_doz_col import strat_dozs_and_cols

# precede all strategies with strat_

strat_dozens_and_columns = {"name": 'roulette_results_cols_and_doz',
                            "fn": strat_dozs_and_cols,
                            'filename': 'dozs_and_cols',
                            'description': ''
                            }
strat_holy_grail_v1 = {"name": 'Holy_Grail_v1',
                       "fn": holy_grail_1,
                       'filename': 'holy_grail_v1',
                       'description': ''
                       }
