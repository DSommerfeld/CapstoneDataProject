"""Dorian Sommerfeld
Applied Computing Capstone Project
Identifying Trends in Seattle Traffic Accidents
Instructor: Laurie Anderson

File for creating sidebar filters"""
import pandas as pd
import streamlit as st

def apply_filters(df):
    """Function for creating fitlers stakeholders can use in the applications."""
# Title for sidebar header    
    st.sidebar.header("Filter Data")

# Checkboxes for boolean filters
# Pedestrian Count column
    pedestrianflag = st.sidebar.checkbox("Pedestrian(s) involved?", key = "pedflag")
# Cyclist Count column
    cyclistflag = st.sidebar.checkbox("Cyclist(s) involved?", key = "cyclflag")
# Injury Count column
    injuryflag = st.sidebar.checkbox("Anyone injured?", key = "injuryflag")
# Serious Injury Count column
    seriousinjuryflag = st.sidebar.checkbox("Anyone seriously injured?", key = "serinjuryflag")
# Fatality Count column
    fatalityflag = st.sidebar.checkbox("Anyone killed?", key =  "fatalityflag")
# Speeding column
    speedingflag = st.sidebar.checkbox("Anyone speeding?", key = "speedingflag")
# Hit Parked Car column
    parkedcarflag = st.sidebar.checkbox("Anyone hit a parked car?", key = "parkedflag")
# Month column made in data cleaning file
    available_months = [
        "January", "February", "March", "April", "May", "June",
        "July", "August", "September", "October", "November", "December"
    ]
    months = df['MONTHNAME'].dropna().unique()
    filtered_months = [m for m in available_months if m in months]
    selected_months = st.sidebar.multiselect(
        "select month(s):",
        options = filtered_months,
        default = [],
        key = "selmonths"
    )
# Year column made in data cleaning file
    available_years = sorted(df['YEAR'].dropna().unique())
    selected_years = st.sidebar.multiselect(
        "select year(s):",
        options = available_years,
        default = [],
        key = "selyears"
    )
# Road Condition column
    road_condition = sorted(df['ROADCOND'].dropna().unique())
    selected_road = st.sidebar.multiselect(
        "select road condition(s):",
        options=road_condition,
        default=[],
        key = "selroad"
    )
# Light Condition column
    light_condition = sorted(df['LIGHTCOND'].dropna().unique())
    selected_light = st.sidebar.multiselect(
        "select light condition(s):",
        options=light_condition,
        default=[],
        key = "sellight"
    )
# Collision type column
    collision_type = sorted(df['COLLISIONTYPE'].dropna().unique())
    selected_collision = st.sidebar.multiselect(
        "select Collision Type(s):",
        options =collision_type,
        default=[],
        key = "selcollision"
    )
# Severity column
    severity_description = sorted(df['SEVERITYDESC'].dropna().unique())
    selected_severity = st.sidebar.multiselect(
        "Select Severity Level(s):",
        options=severity_description,
        default=[],
        key = "selseverity"
    )
    # Series mask created for easier processing of multiple filters
    mask = pd.Series(True, index=df.index)
    if pedestrianflag:
        mask &= df['HASPEDESTRIAN']
    if cyclistflag:
        mask &= df['HASCYCLIST']
    if injuryflag:
        mask &= df['HASINJURY']
    if seriousinjuryflag:
        mask &= df['HASSERIOUSINJURY']
    if fatalityflag:
        mask &= df['HASFATALITY']
    if speedingflag:
        mask &= df['SPEEDINGBOOL']
    if parkedcarflag:
        mask &= df['HITPARKEDBOOL']
    if selected_months:
        mask &= df['MONTHNAME'].isin(selected_months)
    if selected_years:
        mask&= df['YEAR'].isin(selected_years)
    if selected_road:
        mask &= df['ROADCOND'].isin(selected_road)
    if selected_light:
        mask &= df['LIGHTCOND'].isin(selected_light)
    if selected_collision:
        mask &= df['COLLISIONTYPE'].isin(selected_collision)
    if selected_severity:
        mask &= df['SEVERITYDESC'].isin(selected_severity) 
    filtered_df = df[mask]
    return filtered_df

