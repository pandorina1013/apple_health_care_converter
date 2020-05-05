import pandas as pd
import os

from splitter import Splitter


def merge_all():
    i = 0
    for fname in os.listdir('output'):
        if '.csv' in fname:
            if i == 0:
                df = pd.read_csv('output/' + fname)
            else:
                df = pd.merge(df, pd.read_csv('output/' + fname),
                            how='outer', on='datetime')
            i+=1
    df.to_csv('health_care.csv')


if __name__ == "__main__":

    print("Convert apple health care xml to csv.")

    s = Splitter()

    s.get_body_mass()
    s.get_burned_energy()
    s.get_heart_rate()
    s.get_stand_time()
    s.get_step_count()
    s.get_walking_distance()

    print("Merge all csv.")
    merge_all()

    print("Done.")
