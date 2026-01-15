import datetime

import numpy as np
import pandas as pd
from deltalake import DeltaTable
from deltalake.writer import write_deltalake
from helpers import load_cfg

CFG_FILE = "./utils/config.yaml"


def main():
    cfg = load_cfg(CFG_FILE)
    fake_data_cfg = cfg["fake_data"]

    # Load Delta Lake table
    print("*" * 80)
    delta_table_fp = f"{fake_data_cfg['folder_path']}"
    df = pd.DataFrame(
        {
            # Randomize a datetime
            "event_timestamp": [
                np.random.choice(
                    pd.date_range(
                        datetime.datetime(2023, 9, 26), datetime.datetime(2023, 9, 27)
                    )
                ),
                np.random.choice(
                    pd.date_range(
                        datetime.datetime(2023, 9, 26), datetime.datetime(2023, 9, 27)
                    )
                )
            ],
            "pressure": [np.random.rand(), np.random.rand()],
            "velocity": [np.random.rand(), np.random.rand()],
            "speed": [np.random.rand(), np.random.rand()],
        }
    )
    print(df)
    # Append to create new versions
    # Take a look at this for more details: https://delta.io/blog/2022-10-15-version-pandas-dataset/
    write_deltalake(delta_table_fp, df, mode="append")
    print("Final Delta table:")
    dt2 = DeltaTable(delta_table_fp)
    print(dt2.to_pandas())


if __name__ == "__main__":
    main()
