import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import weather
from dataloader import load_data
from scheduler import add_time_chunk_classification
import seaborn as sns
import matplotlib.pyplot as plt

# Streamlit page config
st.set_page_config(
    page_title="ECOmpute",
    layout="wide"
)
clouds = Image.open('img/clouds.png')
leaves = Image.open('img/leaves.png')

weather_data = weather.get_weather('New York')

col1, col2, col3, col4, col5 = st.columns([1,1,1,1,1])

with col1:
    st.metric(label="Temperature", value=round(weather_data['temp'], 2), delta="1.2 °C")
with col2:
    st.metric(label="Clouds", value=weather_data['clouds'], delta="1.2 %")
with col3:
    st.metric(label="Wind", value=weather_data['wind'], delta="-1.2 m/s")
with col4:
   st.metric(label="Humidity", value=weather_data['humidity'], delta="1.2 %")
with col5:
      st.metric(label="Pressure", value=weather_data['pressure'], delta="1.2 hPa")

# with layout_col1:
#    # create a streamlit container that contains the weather data
#    with st.container():
#       st.image(clouds)
#       st.markdown('**Weather in New York**')
#       st.write('Temperature: ', str(round(weather_data['temp'], 2)) + '°C')
#       st.write('Clouds: ', str(weather_data['clouds']) + '%')
#       st.write('Wind: ', str(weather_data['wind']) + 'm/s')


data = load_data()
data = add_time_chunk_classification(data)
data = data.loc[(data.index > '2022-04-01') & (data.index < '2022-05-01')]




sns.set_theme(style="darkgrid")
fig, (ax1, ax2) = plt.subplots(nrows=2, sharex=True, figsize=(10,5))
# plt.stackplot(
#    ax=ax1,
#    x=data.index,
#    y=data['Percentage Renewable'],
# )
# ax=axes[0]
# sns.lineplot(
#    ax = ax1,
#    data = data,
#    y = 'Percentage Renewable',
#    x = data.index,
# )
# fig.suptitle('Bigger 1 row x 2 columns axes with no data')
# axes[0].set_title('Title of the first chart')
# sns.lineplot(ax=axes[0], data=data, x=data.index, y='Load')
# sns.lineplot(ax=axes[1], data=data, x=data.index, y='Nuclear')
data = data.sort_index()
ax1.fill_between(data.index, data['Percentage Fossil'], alpha=0.7)
ax1.fill_between(data.index, 1, data['Percentage Fossil'], alpha=0.7)
ax1.set_ylim(0,1)
ax1.set_xlim(data.index[0], data.index[-1])

st.pyplot(plt.gcf())

with st.container():
   st.markdown('**Your CO2 savings**')
   st.success('You have saved 375kWh of energy! ✅')
