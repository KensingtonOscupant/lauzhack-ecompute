import os
import numpy as np
import pandas as pd


def select_lang(d, lang="en"):
    if pd.isna(d):
        return float("NaN")
    elif isinstance(d, list):
        return select_lang(d[0])
    elif isinstance(d, dict):
        return d[lang]
    return d


def load_meta():
    # Metadata
    df = pd.read_json(os.path.join("data", os.listdir("data")[0]))

    meta = df.drop(
        [
            "date",
            "color",
            "data",
            "xAxisValues",
            "format",
            "yAxis",
            "type",
            "navigatorOptions",
            "hideInPercentView",
            "ignoreForTooltipSum",
            "visible",
            "showInLegend",
            "showInNavigator",
        ],
        axis=1,
    )
    for col in (
        "y0AxisLabelPercent",
        "y1AxisLabel",
        "y1AxisLabelPercent",
        "chartSubTitle",
        "chartTitle",
        "comment",
        "xAxisLabel",
        "y0AxisLabel",
    ):
        meta[col] = meta[col].apply(select_lang)
    meta = meta.loc[0]

    # Column info
    column_info = (
        df[["name", "color", "visible", "showInLegend", "showInNavigator", "yAxis"]]
        .reset_index()
        .drop("index", axis=1)
    )
    column_info["name"] = column_info["name"].apply(select_lang)

    return meta, column_info


def load_data():
    week_data = []
    for week_file in os.listdir("data"):
        if not week_file.startswith('week'):
            continue
        week_df = pd.read_json(os.path.join("data", week_file))

        data = pd.DataFrame(np.vstack(week_df["data"]).T)
        data.index = pd.DatetimeIndex(
            pd.to_datetime(week_df.loc[0, "xAxisValues"], unit="ms")
            + pd.Timedelta(-1, unit='hours')
        ).tz_localize('UTC').tz_convert('CET')
        data.columns = week_df["name"].apply(select_lang).rename("Time")

        week_data.append(data)

    data = pd.concat(week_data)
    return data
