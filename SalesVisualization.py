import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="SalesVisualization", page_icon=":bar_chart:", layout="wide")

@st.cache_data
def get_data_from_csv():
    df = pd.read_csv("Sample-Data-Screener.csv")
    return df

df = get_data_from_csv()

st.sidebar.header("Please Filter Here:")
sectors = st.sidebar.multiselect(
    "Select Sector(s):",
    options=df["Sector"].unique(),
    default=df["Sector"].unique()
)

industries = st.sidebar.multiselect(
    "Select Industry(ies):",
    options=df["Industry"].unique(),
    default=df["Industry"].unique()
)

# Filtering the data based on user selection
df_selection = df[df['Sector'].isin(sectors) & df['Industry'].isin(industries)]

if df_selection.empty:
    st.warning("No data available based on the current filter settings!")
    st.stop()

st.title(":bar_chart: Sales Dashboard")
st.markdown("##")

revenue_sum = df_selection["revenue"].sum()
gp_mean = df_selection["gp"].mean()
fcf_mean = df_selection["fcf"].mean()
capex_mean = df_selection["capex"].mean()

left_column, middle_column, right_column = st.columns(3)

with left_column:
    st.subheader("Total Revenue:")
    st.subheader(f"US $ {revenue_sum:,}")

with middle_column:
    st.subheader("Mean Gross Profit:")
    st.subheader(f"US $ {gp_mean:,.2f}")

with right_column:
    st.subheader("Mean Free Cash Flow:")
    st.subheader(f"US $ {fcf_mean:,.2f}")

st.markdown("""---""")

# Visualization
fig_sector_revenue = px.bar(
    df_selection,
    x='Sector',
    y='revenue',
    title="<b>Revenue by Sector</b>",
    color='Sector',
    template="plotly_white"
)

fig_industry_capex = px.bar(
    df_selection,
    x='Industry',
    y='capex',
    title="<b>Capex by Industry</b>",
    color='Industry',
    template="plotly_white"
)

left_column, right_column = st.columns(2)

left_column.plotly_chart(fig_sector_revenue, use_container_width=True)
right_column.plotly_chart(fig_industry_capex, use_container_width=True)

hide_st_style = """
            <style>
            #MainMenu {visibility: hidden;}
            footer {visibility: hidden;}
            header {visibility: hidden;}
            </style>
            """
st.markdown(hide_st_style, unsafe_allow_html=True)
