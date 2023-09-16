import pandas as pd
import csv
from pathlib import Path
import subprocess




DATA_DIR = Path.cwd() / 'data'
RSCRIPT_PATH = '/usr/lib/R/bin/Rscript'


def run_rcicr(condition: int, subject_id: int):
    try:
        print("running rcicr...\n")
        subprocess.call([RSCRIPT_PATH, "--vanilla", "./src/rc.R", f"{subject_id}", f"{condition}"])
    except Exception as E:
        print(E, E.args) # TODO there should really be logging ...
        raise E
    finally:
        print("finished")
        return


def save_results(raw_data: dict, condition: int, subject_id: int):
    raw_df = pd.DataFrame.from_dict(raw_data['trials'])

    data_df = (raw_df
               .query("trial_type == 'image-button-response'")
            #    .drop('stimulus', axis=1)
               .assign(response=raw_df['response'].replace(0, -1)) # assign inverted choice -1
               )
    df = data_df.query(f"condition == {condition}").reset_index(drop=True)
    df.index = df.index + 1 # start index at 1 for R

    df.to_csv(DATA_DIR / f'sub-{subject_id}_{condition}.csv')


def increment_subject_id():
    get_sid_from_fname = lambda s: int(s[:-6].split('-')[1])
    try:
        sid_max = max(get_sid_from_fname(f.name) for f in DATA_DIR.glob('sub-*.csv'))
    except (ValueError, AttributeError):
        # no data files yet
        sid_max = -1

    return sid_max + 1
