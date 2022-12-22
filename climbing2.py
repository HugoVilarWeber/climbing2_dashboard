import pandas as pd  # pip install pandas openpyxl
import plotly.express as px  # pip install plotly-express
import plotly.graph_objects as go
import streamlit as st  # pip install streamlit
from pathlib import Path
from PIL import Image

#to run the program, use cmd, change directory to python files 
# (cd C:\Users\Usuario\Dropbox\coding\Python files\climbing dashboard) and type 
# streamlit run climbing.py


# emojis: https://www.webfx.com/tools/emoji-cheat-sheet/
st.set_page_config(page_title="Climbing Dashboard", page_icon=":monkey:", layout="wide")

current_dir = Path(__file__).parent if "__file__" in locals() else Path.cwd()
excel_file = current_dir / "sport_climbing.xlsx"

df = pd.read_excel(io=excel_file,
    engine="openpyxl",
    sheet_name="sport_climbing",
    skiprows=0,
    usecols="A:I",
    nrows=513,
)
df["Year"] = df["Date"].dt.strftime("%Y")
print(df)



#---- SIDEBAR ----
st.sidebar.header("Please filter here:")
grade = st.sidebar.multiselect(
    "Select the Grade:",
    options=df["Grade"].unique(),
    default=df["Grade"].unique()
)

status = st.sidebar.multiselect(
    "Select the Status:",
    options=df["Status"].unique(),
    default=df["Status"].unique()
)

zone = st.sidebar.multiselect(
    "Select the Zone:",
    options=df["Zone"].unique(),
    default=df["Zone"].unique()
)

year = st.sidebar.multiselect(
    "Select the Year:",
    options=df["Year"].unique(),
    default=df["Year"].unique()
)

df_selection = df.query(
    "Grade == @grade & Status ==@status & Zone == @zone & Year == @year"
)



st.dataframe(df_selection)

# ---- MAINPAGE ----
st.title(":monkey: Climbing Dashboard")
st.markdown("##")

# TOP KPI's
total_climbs = df_selection["Name"].count()
total_meters = ((df_selection["Length"])*(df_selection["Tries"])).sum()
total_tries = df_selection["Tries"].sum()
tries_per_route = round((df_selection["Tries"].sum()/df_selection["Name"].count()), 2)


column_one, column_two, column_three, column_four = st.columns(4)
with column_one:
    st.subheader("Number of routes climbed:")
    st.subheader(f"{total_climbs} routes")
with column_two:
    st.subheader("Number of meters climbed:")
    st.subheader(f"{total_meters} meters")
with column_three:
    st.subheader("Total number of attemps:")
    st.subheader(f"{total_tries} attempts")
with column_four:
    st.subheader("Average number of attempts per route:")
    st.subheader(f"{tries_per_route} attemps per route")

st.markdown("""---""")

# ROUTES BY GRADE [BAR CHART]
fig_routes_by_status = px.histogram(df_selection, 
    x="Grade", 
    color="Status",
    title="<b>Number of routes by grade and status</b>",
)
fig_routes_by_status.update_layout(yaxis_title="Number of routes")


fig_routes_by_year = px.histogram(df_selection, 
    x="Year",
    title="<b>Number of routes by year</b>",
)
fig_routes_by_year.layout.bargap = 0.3
fig_routes_by_year.update_layout(yaxis_title="Number of routes")


left_column, right_column = st.columns(2)
left_column.plotly_chart(fig_routes_by_status, use_container_width=True)
right_column.plotly_chart(fig_routes_by_year, use_container_width=True)




# ---- HIDE STREAMLIT STYLE ----
hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)