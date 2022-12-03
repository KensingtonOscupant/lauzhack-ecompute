import streamlit as st
import pandas as pd
from PIL import Image
import plotly.express as px
from plotly import subplots
import plotly.graph_objects as go

# Load data
sample_data = pd.read_json('data/sample_time_series.json')
sample_data['xAxisValues'] = pd.to_datetime(sample_data['xAxisValues'], unit='ms')
sample_data = sample_data.set_index('xAxisValues')

# Streamlit page config
st.set_page_config(
    page_title="ECOmpute",
    layout="wide"
)
image_logo = Image.open('img/logo.png')


figure = subplots.make_subplots(rows=2, cols=1, shared_yaxes=False, shared_xaxes=True, row_heights=[1, 0.3])

graph = px.line(sample_data)
for component in graph['data']:
   figure.append_trace(component, row=1, col=1)

over_capacities = [
   (pd.Timestamp('2022-11-28'), pd.Timestamp('2022-11-29')),
   (pd.Timestamp('2022-11-30'), pd.Timestamp('2022-11-30')),
   (pd.Timestamp('2022-11-23'), pd.Timestamp('2022-11-24'))
]

for oc in over_capacities:
   figure.add_trace(
      go.Scatter(x=[oc[0], oc[1]], y=['Over-capacity', 'Over-capacity']), row=2, col=1
   )

layout_col1, layout_col2 = st.columns([1, 4], gap='large')

with layout_col1:
   st.image(image_logo)
   st.success('You saved 938.5 CO2e over the last 7 days. ✅')

with layout_col2:
   st.plotly_chart(figure)