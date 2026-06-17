import streamlit as st
import pandas as pd
import sqlite3
import plotly.express as px

# ==========================================
# PAGE SETUP & TITLES
# ==========================================
st.set_page_config(page_title="Global Weather Dashboard", layout= 'wide')
st.title("Global Weather Dashboard")
st.markdown("Welcome to the Larrenz's weather dashboard! This app visualizes real-time temperature data scraped from TimeAndDate.com.")

# ==========================================
# LOAD DATA
# ==========================================

# @st.cache_data so it doesnt refresh every time user does something. Keeps data. 
@st.cache_data
def load_data():
    conn = sqlite3.connect("capstone_database.db")
    df = pd.read_sql_query("SELECT * FROM weather_data", conn)
    conn.close()
    return df

df = load_data()
print(df.head())

# ==========================================
# SIDEBAR USER INTERACTIONS (REQUIRED: DROPDOWN OR SLIDERS)
# ==========================================
st.sidebar.header("Filter the Data")
st.sidebar.markdown("Use these tools to explore different aspects of the weather data.")

# Interaction 1: Temperature Slider Based On User
min_temp = int(df["Temperature"].min())
max_temp = int(df["Temperature"].max())

selected_temp_range = st.sidebar.slider("Temperature Range (°F): ", min_value=min_temp, max_value=max_temp, value=(min_temp, max_temp)) 

# Apply the slider filter to df to show
filtered_df = df[(df["Temperature"] >= selected_temp_range[0]) & (df["Temperature"] <= selected_temp_range[1])]

# Interaction 2: City Dropdown (Multiselect)
selected_cities = st.sidebar.multiselect( "Compare Specific Cities: ", options=df["City"].unique(), default=df["City"][:5])

# ==========================================
# DASHBOARD VISUALIZATIONS (REQUIRED: 3)
# ==========================================

# --- Header Stats ---
st.markdown("### Quick Stats (Based on Slider Range)")
col1, col2, col3 = st.columns(3)
col1.metric("Total Cities in Range", len(filtered_df))
col2.metric("Hottest Temp", f"{filtered_df['Temperature'].max()} °F" if not filtered_df.empty else "N/A")
col3.metric("Coldest Temp", f"{filtered_df['Temperature'].min()} °F" if not filtered_df.empty else "N/A")

st.divider()

# --- Vis 1: Temperature Distribution (Histogram) ---
st.markdown("### Temperature Distribution")
fig_hist = px.histogram(
    filtered_df,
    x="Temperature",
    title="How many cities fall into each temperature range?",
    color_discrete_sequence=["#51a9ed"],
    labels={"Temperature": "Temperature (°F)"}
)

st.plotly_chart(fig_hist)


# --- Vis 2: Top 10 Hottest Cities (Bar Chart) ---
st.markdown("### Top 10 Hottest Cities Right Now")
# Grab the top 10 highest temps from the currently filtered data
top_hottest = filtered_df.nlargest(10, "Temperature").copy()

#X-axis label of City & Current Time
top_hottest["City_Label"] = top_hottest["City"] + "<br>" + top_hottest["Current Time"]

fig_hot = px.bar(
    top_hottest,
    x="City_Label",
    y="Temperature",
    color="Temperature",
    color_continuous_scale="Reds",
    title="Highest Temps in Selected Range",
    hover_data=["Current Time"]
)

fig_hot.update_layout(xaxis_title="City and Local Time")
st.plotly_chart(fig_hot)


# --- Vis 3: Custom City Comparison (Bar Chart) ---
st.markdown("### Custom City Comparison")
st.markdown("#### Please Use The Sidebar To Select Your Cities to Compare. ")

# Filter the dataframe just for the cities picked in the sidebar dropdown
comparison_df = df[df["City"].isin(selected_cities)].copy()

#X-axis label of City & Current Time
comparison_df["City_Label"] =comparison_df["City"] + "<br>" + comparison_df["Current Time"]

if not comparison_df.empty:
    fig_comp = px.bar(
        comparison_df,
        x="City_Label",
        y="Temperature",
        color="City",
        title="Comparing Your Selected Cities",
        hover_data=["Current Time"]
    )
    fig_comp.update_layout(xaxis_title="City and Local Time")
    st.plotly_chart(fig_comp)
else:
    st.info("Please select at least one city from the sidebar.")
