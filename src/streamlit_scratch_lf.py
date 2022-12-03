import streamlit as st
import pandas as pd
from PIL import Image
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import plotly.subplots as sp
import dash_core_components as dcc
import weather

# Load data
sample_data = pd.read_json('data/sample_time_series.json')
sample_data['xAxisValues'] = pd.to_datetime(sample_data['xAxisValues'], unit='ms')
sample_data = sample_data.set_index('xAxisValues')

# Streamlit page config
st.set_page_config(
    page_title="ECOmpute",
    layout="wide"
)
clouds = Image.open('img/clouds.png')
leaves = Image.open('img/leaves.png')

layout_col1, layout_col2 = st.columns([1, 3])

weather_data = weather.get_weather('New York')

with layout_col1:
   # create a streamlit container that contains the weather data
   with st.container():
      st.image(clouds)
      st.markdown('**Weather in New York**')
      st.write('Temperature: ', str(round(weather_data['temp'], 2)) + '°C')
      st.write('Clouds: ', str(weather_data['clouds']) + '%')
      st.write('Wind: ', str(weather_data['wind']) + 'm/s')
   with st.container():
      st.image(leaves)
      st.markdown('**Your CO2 savings**')
      st.success('You have saved 375kWh of energy! ✅')

image = Image.open('img/logo.png')

with layout_col2:
   st.line_chart(sample_data)
   df = pd.DataFrame([
      dict(Task="Job A", Start='2009-01-01', Finish='2009-02-28'),
      dict(Task="Job B", Start='2009-03-05', Finish='2009-04-15'),
      dict(Task="Job C", Start='2009-02-20', Finish='2009-05-30')
   ])

   fig = px.timeline(df, x_start="Start", x_end="Finish", y="Task")
   fig.update_yaxes(autorange="reversed") # otherwise tasks are listed from the bottom up
   # fig.show()

   fig.update_xaxes(
      side="top",
      dtick="D1",
      tickformat="%e\n%b\n%Y",
      ticklabelmode="period",
      tickangle=0,
      fixedrange=True,
   )
   fig.update_yaxes(
      title="",
      tickson="boundaries",
      fixedrange=True,
   )
   BARHEIGHT = .1
   fig.update_layout(
      yaxis={"domain": [max(1 - (BARHEIGHT * len(fig.data)), 0), 1]}, margin={"t": 0, "b": 0}
   )

   #st.plotly_chart(fig, use_container_width=True)



   # how do i set bar thickness in plotly timeline charts? https://stackoverflow.com/questions/64888876/how-do-i-set-bar-thickness-in-plotly-timeline-charts

# # Add histogram data
# x1 = np.random.randn(200) - 2
# x2 = np.random.randn(200)
# x3 = np.random.randn(200) + 2

# # Group data together
# hist_data = [x1, x2, x3]

# group_labels = ['Group 1', 'Group 2', 'Group 3']

# # Create distplot with custom bin_size
# fig = ff.create_distplot(
#         hist_data, group_labels, bin_size=[.1, .25, .5])

# # Plot!
# st.plotly_chart(fig, use_container_width=True)

text = "New York"

# display text and image next to each other
#st.image(image, caption=text, width=300)