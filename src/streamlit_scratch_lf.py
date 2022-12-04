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
import os


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
   new_job_duration = st.number_input('Job duration (h)', value=60, min_value=0, max_value=7*24)
   new_job_deadline = st.date_input('Job deadline', value=pd.to_datetime('2023-01-01'))
   new_job_submit = st.button('Schedule job')

   reset_jobs_button = st.button('Delete jobs')

data = load_data()
data = add_time_chunk_classification(data)
data = data.loc[(data.index > '2022-04-01') & (data.index < '2022-04-14')]

data.loc[data['Grey'], 'schedule_tag'] = 'grey'
data.loc[data['Overproduction'], 'schedule_tag'] = 'excess'
data.loc[data['Green'], 'schedule_tag'] = 'renewable'

with layout_col2:

   # Read jobs from CSV if file exists
   if os.path.isfile('jobs.csv') and not reset_jobs_button:
         jobs = pd.read_csv('jobs.csv')
   else:
         jobs = pd.DataFrame(columns=['id', 'deadline', 'length', 'priority'])
         jobs.to_csv('jobs.csv', index=False)

   # Plotly subplot with three rows
   fig = subplots.make_subplots(rows=3, cols=1, shared_xaxes=True, vertical_spacing=0.06, row_heights=[.8, 0.1, 0.08 * len(jobs) + 0.02])
   fig.add_trace(go.Scatter(x=data.index, y=data['Percentage Renewable'], fill='tozeroy', line_color='mediumseagreen', name='Renewable energy'), row=1, col=1)

   # Add points where data['green'] == True
   fig.add_trace(go.Scatter(x=data[data['Overproduction']].index, y=['Overproduction'] * len(data[data['Overproduction']].index), mode='markers', marker=dict(symbol='square'), name='Overproduction'), row=2, col=1)
   fig.add_trace(go.Scatter(x=data[data['Green']].index, y=['Green'] * len(data[data['Green']].index), mode='markers', marker=dict(symbol='square'), name='Green time'), row=2, col=1)

   # If job scheduled add line
   # Solve job scheduling problem if one is submitted

   if new_job_submit == True:

      job = {
         'id': [new_job_name],
         'length': [new_job_duration],
         'priority': [10],
         'deadline': [pd.Timestamp(new_job_deadline, tz='CET')],
      }

      jobs = pd.concat([jobs, pd.DataFrame(job)], ignore_index=True)
      jobs.to_csv('jobs.csv', index=False)

   if len(jobs) > 0:
      scheduled_time_slots = scheduling.solve(jobs, data['schedule_tag'])
      fig.add_trace(go.Scatter(x=scheduled_time_slots.dropna().index, y=scheduled_time_slots.dropna(), mode='markers', marker=dict(symbol='square'), name='Jobs'), row=3, col=1)

   st.plotly_chart(fig)

# Calculate CO2e savings
if new_job_submit:
   renewable_mean_general = data.loc[data['Green'], 'Percentage Renewable'].mean()
   renewable_mean_job = data.loc[scheduled_time_slots.dropna().index, 'Percentage Renewable'].mean()
   st.subheader(f"✅ You saved {(renewable_mean_job - renewable_mean_general) * 12000:.2f} CO2 kg")