import pandas as pd
import datetime
mins = pd.read_csv("mins.csv") 
current = datetime.datetime.now().replace(second=0, microsecond=0)
print(current)

print(mins.loc[mins["time"] == current, "exposure"])