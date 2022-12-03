import pandas as pd

columns_renewable = [
    'Hydro water reservoir',
    'Hydro pumped storage',
    'Hydro Run-of-River',
    'Wind offshore',
    'Wind onshore',
    'Solar',
    'Geothermal',
]

columns_fossil = [    
    'Others',
    'Nuclear',
    'Fossil brown coal / lignite',
    'Fossil hard coal',
    'Fossil oil',
    'Fossil gas',
    'Waste',
    'Biomass',
]

def add_time_chunk_classification(data: pd.DataFrame):
    """Adds the classification of green, grey or over-capacity timespan classifications to time series Dataframe."""

    renewable_power = data[columns_renewable].sum(axis=1)
    fossil_power = data[columns_fossil].sum(axis=1)

    over_prodcution = (fossil_power + renewable_power) - data['Load']

    data['Overproduction'] =  over_prodcution > 5000 
    total = fossil_power + renewable_power
    percentage_renewable = renewable_power / total

    data['Percentage Renewable'] = percentage_renewable
    data['Percentage Fossil'] = fossil_power / total

    data['Green'] = (percentage_renewable > percentage_renewable.mean()) & (data['Overproduction'] == False)

    # If not green and not overproduction, it is grey
    data['Grey'] = (data['Green'] == False) & (data['Overproduction'] == False)
    return data

