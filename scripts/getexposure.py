import requests
import datetime
import numpy as np
import pandas as pd
import time
import plotly.graph_objects as go

max = 6000000
min = 4000
change = np.round(np.linspace(min, max, 121))
mins = pd.DataFrame({"time": pd.date_range("1/1/2021", "31/12/2021", freq="T"), "exposure": max})
url = "https://raw.githubusercontent.com/ekstremedia/raspberry-timelapse/master/scripts/solartimes.json"
data = requests.get(url).json()
sunset = None
neversets = False
for i in data:
    if not data[i]["data"]:
        if data[i]["sun"] == "never_sets":
            day = datetime.datetime.strptime(f'2021-{i}', "%Y-%d-%m")
            day_end = day + datetime.timedelta(hours=23, minutes=59)
            mins.loc[(mins["time"] >= day) & (mins["time"] <= day_end), "exposure"] = min
            if not neversets:
                new_max = int((((day-sunset).seconds/120)/120)*max)
                new_change = np.linspace(min, new_max, int(((day-sunset).seconds/120))+1)
                new_change_a = np.round(np.concatenate([new_change[:-1], new_change[::-1]]))
                try:
                    mins.loc[(mins["time"] >= sunset) & (mins["time"] <= day), "exposure"] = new_change_a
                except ValueError:
                    new_change_a = np.round(np.concatenate([new_change, new_change[::-1]]))
                    mins.loc[(mins["time"] >= sunset) & (mins["time"] <= day), "exposure"] = new_change_a
            neversets = True
    else:
        sunrise = datetime.datetime.strptime(f'2021-{i} {data[i]["sunrise"]}', "%Y-%d-%m %H:%M")
        pre_sunrise = sunrise - datetime.timedelta(hours=2)
        if neversets:
            day = datetime.datetime.strptime(f'2021-{i}', "%Y-%d-%m")
            sunrise = datetime.datetime.strptime(f'2021-{i} {data[i]["sunrise"]}', "%Y-%d-%m %H:%M")
            new_max = int((((sunrise-day).seconds/120)/120)*max)
            new_change = np.linspace(min, new_max, int(((sunrise-day).seconds/120))+1)
            new_change_a = np.round(np.concatenate([new_change[:-1], new_change[::-1]]))
            try:
                mins.loc[(mins["time"] >= day) & (mins["time"] <= sunrise), "exposure"] = new_change_a
            except ValueError:
                new_change_a = np.round(np.concatenate([new_change, new_change[::-1]]))
                mins.loc[(mins["time"] >= day) & (mins["time"] <= sunrise), "exposure"] = new_change_a
            sunset = datetime.datetime.strptime(f'2021-{i} {data[i]["sunset"]}', "%Y-%d-%m %H:%M")
            post_sunset = sunset + datetime.timedelta(hours=2)
            mins.loc[(mins["time"] >= sunrise) & (mins["time"] <= sunset), "exposure"] = min
            mins.loc[(mins["time"] >= sunset) & (mins["time"] <= post_sunset), "exposure"] = change
            neversets = False
            continue
        if sunset:
            yest_sunset = sunset
            if sunrise-yest_sunset < datetime.timedelta(hours=4):
                new_max = int((((sunrise-yest_sunset).seconds/120)/120)*max)
                new_change = np.linspace(min, new_max, int(((sunrise-yest_sunset).seconds/120))+1)
                new_change_a = np.round(np.concatenate([new_change[:-1], new_change[::-1]]))
                try:
                    mins.loc[(mins["time"] >= yest_sunset) & (mins["time"] <= sunrise), "exposure"] = new_change_a
                except ValueError:
                    new_change_a = np.round(np.concatenate([new_change, new_change[::-1]]))
                    mins.loc[(mins["time"] >= yest_sunset) & (mins["time"] <= sunrise), "exposure"] = new_change_a
                sunset = datetime.datetime.strptime(f'2021-{i} {data[i]["sunset"]}', "%Y-%d-%m %H:%M")
                post_sunset = sunset + datetime.timedelta(hours=2)
                mins.loc[(mins["time"] >= sunrise) & (mins["time"] <= sunset), "exposure"] = min
                mins.loc[(mins["time"] >= sunset) & (mins["time"] <= post_sunset), "exposure"] = change
                continue

        sunset = datetime.datetime.strptime(f'2021-{i} {data[i]["sunset"]}', "%Y-%d-%m %H:%M")
        post_sunset = sunset + datetime.timedelta(hours=2)
        mins.loc[(mins["time"] >= pre_sunrise) & (mins["time"] <= sunrise), "exposure"] = change[::-1]
        mins.loc[(mins["time"] >= sunrise) & (mins["time"] <= sunset), "exposure"] = min
        mins.loc[(mins["time"] >= sunset) & (mins["time"] <= post_sunset), "exposure"] = change

fig = go.Figure(data=go.Scattergl(x=mins["time"], y=mins["exposure"], mode='lines'))
fig.update_xaxes(rangeslider_visible=True)
fig.show()