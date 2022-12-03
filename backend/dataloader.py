import os
import numpy as np
import pandas as pd


def select_lang(d, lang='en'):
    if pd.isna(d):
        return float('NaN')
    elif isinstance(d, list):
        return select_lang(d[0])
    elif isinstance(d, dict):
        return d[lang]
    return d


def load_data():
    week_dfs = []
    for week_file in os.listdir('data'):
        week_dfs.append(pd.read_json(os.path.join('data', week_file)))
    
    df = pd.concat(week_dfs, ignore_index=True)

    # Metadata
    meta = df.drop(
        [
            'date',
            'color',
            'data',
            'xAxisValues',
            'format',
            'yAxis',
            'type',
            'navigatorOptions',
            'hideInPercentView',
            'ignoreForTooltipSum',
            'visible',
            'showInLegend',
            'showInNavigator',
        ],
        axis=1,
    )
    for col in (
        'y0AxisLabelPercent',
        'y1AxisLabel',
        'y1AxisLabelPercent',
        'chartSubTitle',
        'chartTitle',
        'comment',
        'xAxisLabel',
        'y0AxisLabel',
    ):
        meta[col] = meta[col].apply(select_lang)
    meta = meta.loc[0]

    # Column info
    column_info = df[
        ['name', 'color', 'visible', 'showInLegend', 'showInNavigator', 'yAxis']
    ].reset_index().drop('index', axis=1)
    column_info['name'] = column_info['name'].apply(select_lang)

    # Time series data
    data = pd.DataFrame(np.vstack(df['data']).T)
    data.index = pd.DatetimeIndex(pd.to_datetime(df.loc[0, 'xAxisValues'], unit='ms')).strftime('%Y-%m-%d-%H-%M-%S')
    data.columns = df['name'].apply(select_lang).rename('Time')

    return meta, column_info, data
