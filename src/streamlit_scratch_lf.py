import streamlit as st
import pandas as pd
from PIL import Image

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


layout_col1, layout_col2 = st.columns([1, 4])

with layout_col1:
   st.image(image_logo)

with layout_col2:
   st.line_chart(sample_data)