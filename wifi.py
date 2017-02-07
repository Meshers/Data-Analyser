import pandas as pd
import plotly.offline as pl
import plotly.graph_objs as go


import datetime

KEY_START_TIME = "StartTime"
KEY_END_TIME = "EndTime"
KEY_SSID = "SSID"
KEY_BSSID = "BSSID"


def draw_discovery_graph(df: pd.DataFrame):
    series = df.groupby(by=KEY_START_TIME)[KEY_SSID].unique()
    series.sort_index(inplace=True)
    min_time = int(series.index[0])
    max_time = int(series.index[-1])
    print(series)
    scatter = go.Scatter(
        x=list(map(lambda x: (int(x) - min_time)//1000, series.index)),
        y=list(map(lambda x: len(x), series)),
        mode='lines+markers',
        name='lines+markers'
    )
    data = [scatter]
    pl.plot(data)
    pass


def main():
    new_df = pd.read_csv("WIFI_1485837592674.csv")
    old_df = pd.read_csv("WIFI_1485836931804.csv")
    filtered_df = new_df[~new_df[KEY_SSID].isin(old_df[KEY_SSID])]
    print(len(filtered_df[KEY_START_TIME].unique()))
    print(len(filtered_df[KEY_SSID].unique()))
    series = filtered_df.groupby(by=KEY_START_TIME)[KEY_SSID].unique()
    max_element, index = max(zip(series, series.index), key=lambda x: len(x[0]))
    print(len(max_element))
    print(index)
    draw_discovery_graph(filtered_df)


if __name__ == '__main__':
    main()
