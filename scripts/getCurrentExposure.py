import pandas as pd
import datetime
col_list = ["time", "exposure"]
usecols = col_list

mins = pd.read_csv("mins.csv", usecols=col_list)
current = str(datetime.datetime(2021,4,4,20,21,00).replace(second=0, microsecond=0))
out = int(mins.loc[mins["time"] == current, "exposure"])
print(out)
