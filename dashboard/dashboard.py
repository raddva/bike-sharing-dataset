import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

sns.set_theme(style='dark')

st.title('Analisis Bike Sharing Dataset')

main_data = pd.read_csv("dashboard/main_data.csv")

st.sidebar.header("Select Analysis")

st.caption('Nadya, 2024')