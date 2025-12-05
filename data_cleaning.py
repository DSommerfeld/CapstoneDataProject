"""Dorian Sommerfeld
Applied Computing Capstone Project
Identifying Trends in Seattle Traffic Accidents
Instructor: Laurie Anderson

File for cleaning columns like location and processing time and dates"""

import pandas as pd

def clean_location(df):
    """Cleans the location column so instances of AND and BETWEEN are 
    eliminated."""
    df['LOCATION'] = df['LOCATION'].astype(str).str.upper().str.strip()
    # New column created for removing AND and BETWEEN keywords
    df['MAINSTREET'] = (
        #Erasing mentions of AND and BETWEEN
        df['LOCATION']
        .str.split(' BETWEEN', n=1).str[0]
        .str.split(' AND', n=1).str[0]
        .str.strip()
    )
    # New column overwrite to also remove NSEW
    df['MAINSTREET'] = df['MAINSTREET'].str.replace(
        r"\b(N|S|E|W)\b", "", regex=True
        #Erases mentions of North, South, East, West
    )

    df['MAINSTREET'] = df['MAINSTREET'].str.replace(r"\s+", " ", regex=True)
    # Replacing missing cells with unknown
    df['MAINSTREET'] = df['MAINSTREET'].replace("", 'UNKNOWN')

    return df

def datetime_process(df):
    """Splits up the times and dates for ease of filtering, also rounds
    specific time frames to either :00 or :30."""
    # Removing errors
    df['INCDATE'] = pd.to_datetime(df['INCDATE'], errors = 'coerce')
    df['INCDTTM'] = pd.to_datetime(df['INCDTTM'], errors='coerce')
    #Splitting year, month, hour and weekday
    df['YEAR'] = df['INCDATE'].dt.year
    df['MONTH'] = df['INCDATE'].dt.month
    df['DAYOFWEEK'] = df['INCDATE'].dt.day_name()
    df['HOUR'] = df['INCDTTM'].dt.hour
    #string formatting
    df['MONTHNAME'] = df['INCDATE'].dt.strftime("%B")
    return df

def daylight_savings_marking(df):
    """Processes INCDATE for the use of conducting analysis on
    the effect daylight savings has on crashes in Seattle."""
    #New columns created and made false or none first
    df['ISDSTPERIOD'] = False
    df['DSTEVENT'] = None
    df['DAYSFROMDST'] = None

    years = df['INCDATE'].dt.year.dropna().unique()

    for year in years:
        #Daylight savings starts in March
        march = pd.date_range(f'{year}-03-01', f'{year}-03-31', freq='D')
        march_sundays = [d for d in march if d.weekday() == 6]
        #first sunday of march is start
        dst_start = march_sundays[1]
        #Daylight savings ends in November
        november = pd.date_range(f'{year}-11-01', f'{year}-11-30', freq='D')
        november_sundays = [d for d in november if d.weekday() == 6]
        dst_end = november_sundays[0]

        #Creating windows for daylight savings start and end
        startwindow = (df['INCDATE'] >= dst_start - pd.Timedelta(days=7)) & (df['INCDATE'] <= dst_start + pd.Timedelta(days=7))
        endwindow = (df['INCDATE'] >= dst_end - pd.Timedelta(days=7)) & (df['INCDATE'] <= dst_end + pd.Timedelta(days=7))
        #Dictionary created for easier processing of multiple DST events
        df.loc[startwindow, 'ISDSTPERIOD'] = True
        df.loc[startwindow, 'DSTEVENT'] = 'Spring Forward'
        df.loc[startwindow, 'DAYSFROMDST'] = ((df.loc[startwindow, 'INCDATE'] - dst_start).dt.days)

        df.loc[endwindow, 'ISDSTPERIOD'] = True
        df.loc[endwindow, 'DSTEVENT'] = 'Fall Back'
        df.loc[endwindow , 'DAYSFROMDST'] = ((df.loc[endwindow, 'INCDATE'] - dst_end).dt.days)

    return df

def boolean_flags(df):
    """Turns columns with numbers like PEDCOUNT and INJURIES into simplified
    columns stating if someone was involved, injured or killed."""
    # Added to haspedestrian if pedcount is 1 or more
    df['HASPEDESTRIAN'] = df['PEDCOUNT'] > 0
    # Added to hascyclist if pedcylcount is 1 or more
    df['HASCYCLIST'] = df['PEDCYLCOUNT'] > 0
    # Added to hasinjury if injuries is 1 or more
    df['HASINJURY'] = df['INJURIES'] > 0
    # Added to hasseriousinjury if seriousinjuries is 1 or more
    df['HASSERIOUSINJURY'] = df['SERIOUSINJURIES'] > 0
    # Added to hasfatality if fatalities is 1 or more
    df['HASFATALITY'] = df['FATALITIES'] > 0

    return df

def parked_car_boolean(df):
    """Makes a new boolean column that takes data from the hitparkedcar"
    "column and removes any 'not recorded' options."""
    df['HITPARKEDBOOL'] = df['HITPARKEDCAR'].astype(str).str.upper().map({
        "Y": True,
        "N": False
    # Anything missing is filled as false
    }).fillna(False)
    return df

def speeding_boolean(df):
    """Makes a new boolean column collecting data from the speeding
    column and removes 'not recorded' options."""
    df['SPEEDINGBOOL'] = df['SPEEDING'].astype(str).str.upper().map({
        "Y": True
    # Anything missing filled as false
    }).fillna(False)
    return df


