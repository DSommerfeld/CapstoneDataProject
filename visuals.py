"""Dorian Sommerfeld
Applied Computing Capstone Project
Identifying Trends in Seattle Traffic Accidents
Instructor: Laurie Anderson

File for creating visualizations like bar charts, line graphs"""
#Importing libraries
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st

def plot_time_distribution(df):
    """Bar Chart distribution of collisions by time of day"""
    st.subheader("Collisions by Hour of Day")
    # Counts for collisions by hour
    hourly = df.groupby('HOUR').size().reset_index(name='COUNT')
    # Labeling for AM and PM
    hourly['HOURLABEL'] = hourly['HOUR'].apply(
        lambda h: f"{(h % 12) or 12} {'AM' if h < 12 else 'PM'}"
    )
    # Creating figure
    fig, ax = plt.subplots(figsize=(14, 6))
    # Colors for bars
    ax.bar(hourly['HOURLABEL'], hourly['COUNT'], color="#5A8FFE")

    ax.set_title("Collisions by Hour of Day", fontsize=18)
    ax.set_xlabel("Hour of Day", fontsize=14)
    ax.set_ylabel("Number of Collisions", fontsize=14)

    plt.xticks(rotation = 0)

    ax.grid(axis="y", linestyle="--", alpha=0.4)

    st.pyplot(fig)

def plot_day_of_week(df):
    """Bar Chart showcasing collisions by days of the week"""
    st.subheader("Collisions by Day of Week")
    
    if 'INCDATE' not in df.columns:
        st.error("INCDATE Missing.")
        return
    # creating copy of dataframe
    df = df.copy()
    df['WEEKDAY'] = df['INCDATE'].dt.dayofweek
    df['DAYNAME'] = df['INCDATE'].dt.day_name()
    # List for days of the week
    ordered_days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    # Creating counts for day of week collisions
    counts = df.groupby('DAYNAME').size().reindex(ordered_days).fillna(0)

    fig, ax = plt.subplots(figsize=(12, 6))
    ax.bar(counts.index, counts.values, color="#5A8FFE")
    ax.set_title("Collisions by Day of Week", fontsize=16)
    ax.set_xlabel("")
    ax.set_ylabel("Number of Collisions")
    ax.grid(axis="y", linestyle='--', alpha=0.4)

    plt.xticks(rotation = 0)

    st.pyplot(fig)

def plot_monthly_trend(df):
    """Line graph for showcasing number of crashes for each month"""
    st.subheader("Monthly Collision Trends for 2020 - 2025")
    # Map for shortened month names
    month_map = {
        "January": "Jan", "February": "Feb", "March": "Mar", "April": "Apr",
        "May": "May", "June": "Jun", "July": "Jul", "August": "Aug",
        "September": "Sep", "October": "Oct", "November": "Nov", "December": "Dec"
    }
    month_order = list(month_map.values())
    # Creating counts for month processing
    monthly = df.groupby(['YEAR', 'MONTHNAME']).size().reset_index(name='COUNT')
    monthly = monthly.dropna(subset=['MONTHNAME', 'YEAR'])
    monthly['MONTHNAME'] = monthly['MONTHNAME'].astype(str)
    monthly['MONTHSHORT'] = monthly['MONTHNAME'].map(month_map)
    # Putting shorted month order category for 'MONTHNAME' column
    monthly['MONTHSHORT'] = pd.Categorical(
        monthly['MONTHSHORT'],
        categories = month_order,
        ordered = True
    )

    monthly = monthly.sort_values(['YEAR', 'MONTHSHORT'])
    # Creating figure
    fig, ax = plt.subplots(figsize=(14, 6))

    for year in monthly['YEAR'].unique():
        subset = monthly[monthly['YEAR'] == year]
        ax.plot(subset['MONTHSHORT'], subset['COUNT'], marker="o", label=str(year))

    ax.set_title("Monthly Collision Trends by Year", fontsize=16)
    ax.set_xlabel("Month")
    ax.set_ylabel("Collisions")
    ax.legend(title="Year")
    plt.xticks(rotation=0)
    st.pyplot(fig)

def plot_dst_trend(df):
    """Line chart showcasing trends in crashes during Spring and Fall
    Daylight Savings periods."""
    st.subheader("Collision Counts 14 days Before and After DST Change")
    # Subset is a week before and after dst day
    subset = df[(df['DAYSFROMDST'] >= -7) & (df['DAYSFROMDST'] <= 7)]
    # Creating counts for DST days
    daily = (
        subset.groupby(['DSTEVENT', 'DAYSFROMDST'])
            .size()
            .reset_index(name="COUNT")
    )

    pivot = daily.pivot(index='DAYSFROMDST', columns = 'DSTEVENT', values='COUNT').fillna(0)
    # Creating figure
    fig, ax = plt.subplots(figsize=(14, 6))

    for event in pivot.columns:
        ax.plot(pivot.index, pivot[event], marker="o", linewidth=2, label=event)
        # Labeling day values as days before and after dst
    friendly_labels = {
        -7: "7 Before", -6: "6 Before", -5: "5 Before", -4: "4 Before",
        -3: "3 Before", -2: "2 Before", -1: "1 Before",
        0: "DST Day",
        1: "1 After", 2: "2 After", 3: "3 After", 4: "4 After",
        5: "5 After", 6: "6 After", 7: "7 After"
    }

    ax.set_xticks(list(friendly_labels.keys()))
    ax.set_xticklabels(list(friendly_labels.values()), rotation=45, ha="right")

    ax.axvline(0, color="gray", linestyle="--", alpha=0.7)
    ax.text(0, ax.get_ylim()[1], " ", ha="center", va="bottom", fontsize=12)

    ax.set_title("Collision Counts 7 Days Before and After DST Changes", fontsize=18)
    ax.set_xlabel("Days Relative to DST Change", fontsize=14)
    ax.set_ylabel("Number of Collisions", fontsize=14)

    ax.grid(axis="y", linestyle="--", alpha=0.4)
    ax.legend(title="DST Event")

    st.pyplot(fig)

def plot_yoy_full_year(df):
    """Plots the percentage change of crashes from 2020 to 2024."""
    st.subheader("Year-over-Year Crash Comparison (2020 to 2024)")
    # Creating yearly count with year pandas column
    yearly = df.groupby("YEAR").size().reset_index(name="COUNT")
    # yearly count is anything from 2020 to 2024
    yearly = yearly[yearly["YEAR"].between(2020, 2024)]
    # Creating percentage change column
    yearly["PCTCHANGE"] = yearly["COUNT"].pct_change() * 100
    # Creating figure
    fig, ax = plt.subplots()
    ax.bar(yearly["YEAR"], yearly["COUNT"], color="#5A8FFE")
    ax.set_xlabel("Year")
    ax.set_ylabel("Total Collisions")
    ax.set_title("Total Crashes per Year (2020-2024)")

    st.pyplot(fig)
    # Display percent change values as short dataframe
    st.write("### Percentage Change")
    st.dataframe(yearly)

def plot_yoy_partial(df):
    st.subheader("Year-over-Year (Jan-Sept) Crash Comparison (2024-2025)")
    # Creating January through September period since 2025 is incomplete
    jan_sept = df[df["MONTH"] <= 9]
    # Creating a count in the year column made with pandas
    counts = jan_sept.groupby("YEAR").size().reset_index(name="COUNT")
    # Count is anything between 2024 and 2025
    counts = counts[counts["YEAR"].isin([2024, 2025])]
    # Sorting
    counts = counts.sort_values("YEAR")

    counts["PCTCHANGE"] = counts["COUNT"].pct_change() *100
    # Creating figure
    fig, ax = plt.subplots()
    ax.bar(counts["YEAR"], counts["COUNT"], color="#5A8FFE")
    ax.set_xlabel("YEAR")
    ax.set_ylabel("Collisions (Jan-Sept)")
    ax.set_title("Jan-Sept Crash Totals (2024 - 2025)")

    st.pyplot(fig)
    # Present percent change values as short dataframe
    st.write("### Percentage Change")
    st.dataframe(counts)

def plot_dangerous_streets(df):
    """Plots the top ten most dangerous streets based on overall number of crashes."""
    st.subheader("Top 10 Streets with most crashes overall")
    #MAINSTREET column created in data_cleaning file
    streetcounts = (df['MAINSTREET'].value_counts().head(10).sort_values(ascending=True))
    # Creating figure
    fig, ax = plt.subplots()
    # Horizontal bar chart
    ax.barh(streetcounts.index, streetcounts.values, color="#5A8FFE")
    ax.set_xlabel("Number of Collisions")
    ax.set_ylabel("Street Name")
    ax.set_title("Top 10 Streets with Most Collisions")

    st.pyplot(fig)

    st.write(streetcounts.to_frame("Crash Count"))



















