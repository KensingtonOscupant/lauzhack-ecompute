import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import weather
from dataloader import load_data
from scheduler import add_time_chunk_classification
import seaborn as sns
import matplotlib.pyplot as plt
import scheduling
from plotly import graph_objects as go
from plotly import subplots


# Streamlit page config
st.set_page_config(
    page_title="ECOmpute",
    layout="wide"
)
clouds = Image.open('img/clouds.png')
leaves = Image.open('img/leaves.png')
logo = Image.open('img/logo.png')

# Weather bar
weather_data = weather.get_weather('New York')

# Add weather bar
logo_col, col1, col2, col3, col4, col5 = st.columns([1.5, 1,1,1,1,1])

with col1:
   st.metric(label="Temperature", value=round(weather_data['temp'], 2), delta="1.2 °C")
with col2:
   st.metric(label="Clouds", value=weather_data['clouds'], delta="1.2 %")
with col3:
   st.metric(label="Wind", value=weather_data['wind'], delta="-1.2 m/s")
with col4:
   st.metric(label="Humidity", value=20, delta="1.2 %")
with col5:
   st.metric(label="Pressure", value=20, delta="1.2 hPa") 
with logo_col:
   # Add logo
   st.image(logo)

layout_col1, layout_col2 = st.columns([1, 3])

with layout_col1:
   # Add job functionality

   st.subheader('Schedule job')

   new_job_name = st.text_input('Job name', value='Job 1')
   new_job_duration = st.number_input('Job duration (h)', value=60, min_value=0, max_value=150)
   new_job_deadline = st.date_input('Job deadline', value=pd.to_datetime('2023-01-01'))
   new_job_submit = st.button('Schedule job')

data = load_data()
data = add_time_chunk_classification(data)
data = data.loc[(data.index > '2022-04-01') & (data.index < '2022-04-14')]

data.loc[data['Grey'], 'schedule_tag'] = 'grey'
data.loc[data['Overproduction'], 'schedule_tag'] = 'excess'
data.loc[data['Green'], 'schedule_tag'] = 'renewable'

with layout_col2:

   # Plotly subplot with three rows
   fig = subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.001, row_heights=[0.6, 0.2, 0.2])
   fig.add_trace(go.Scatter(x=data.index, y=data['Percentage Renewable']), row=1, col=1)

   # Add points where data['green'] == True
   fig.add_trace(go.Scatter(x=data[data['Overproduction']].index, y=['Overproduction'] * len(data[data['Overproduction']].index), mode='markers', marker=dict(symbol='square')), row=2, col=1)
   fig.add_trace(go.Scatter(x=data[data['Green']].index, y=['Green'] * len(data[data['Green']].index), mode='markers', marker=dict(symbol='square')), row=2, col=1)

   # If job scheduled add line
   # Solve job scheduling problem if one is submitted
   if new_job_submit == True:
      job = {
         'id': [new_job_name],
         'length': [new_job_duration],
         'priority': [10],
         'deadline': [pd.Timestamp(new_job_deadline, tz='CET')],
      }
      scheduled_time_slots = scheduling.solve(pd.DataFrame(job), data['schedule_tag'])

      fig.add_trace(go.Scatter(x=scheduled_time_slots.dropna().index, y=['Job scheduled'] * len(scheduled_time_slots.dropna().index), mode='markers', marker=dict(symbol='square')), row=3, col=1)

   st.plotly_chart(fig)

