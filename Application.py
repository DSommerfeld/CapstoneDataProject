"""Dorian Sommerfeld
Applied Computing Capstone Project
Identifying Trends in Seattle Traffic Accidents
Instructor: Laurie Anderson

File for importing other helper methods and running main application"""

# Importing Important Libraries + Other file methods
import pandas as pd
import streamlit as st
from data_cleaning import *
from filters import apply_filters
from visuals import *


# Streamlit Page Config
st.set_page_config(
    page_title="Uncovering Trends in Seattle Traffic Accidents",
    page_icon="🚗",
    layout="wide"
)

# App Title
st.title(" 🚗Uncovering Trends in Seattle Traffic Accidents (2020 - 2025)")
st.caption("Created by: Dorian Sommerfeld | Applied Computing Capstone | Instructor: Laurie Anderson")
# Stakeholder Form Link
st.markdown(
    """
    ### Stakeholder Feedback Form
    Please take a moment to provide feedback while exploring the application.
    [Click here to open the Google Form](https://docs.google.com/forms/d/e/1FAIpQLSeYdHGOOGePnhuYrW4pMvV53sLOMmi5wDPhRf8fgNwO6GQHrQ/viewform?usp=dialog)""",
    unsafe_allow_html=True
)

# Loading Dataset
file_path = "SDOT_Collisions_All_Years_Reworked20t25NoInattentionID.xlsx"
# Caching data
@st.cache_data(show_spinner=True)
def load_data(path):
    """Method for loading the dataset. Tries opening excel file, 
    stops everything if missing. """
    try:
        return pd.read_excel(path)
    except FileNotFoundError:
        st.error("Dataset not found.")
        st.stop()
# Creating variable for loading data
df = load_data(file_path)
# Caching data
@st.cache_data(show_spinner=True)
def clean_data(df):
    """Applying methods from data cleaning file."""
    df = clean_location(df)
    df = datetime_process(df)
    df = daylight_savings_marking(df)
    df = boolean_flags(df)
    df = parked_car_boolean(df)
    df = speeding_boolean(df)
    return df
# Applying clean data method to df variable
df = clean_data(df)

# Making copy of datafile for filtering
filtered_df = apply_filters(df)

st.markdown("---")
st.header("Visualizations")

# Appling the visuals from visuals file
plot_dangerous_streets(filtered_df)
# commented out collision type graph, will refine later
# plot_collision_type(filtered_df)
plot_time_distribution(filtered_df)
plot_day_of_week(filtered_df)
plot_monthly_trend(filtered_df)
plot_dst_trend(filtered_df)
plot_yoy_full_year(filtered_df)
plot_yoy_partial(filtered_df)

