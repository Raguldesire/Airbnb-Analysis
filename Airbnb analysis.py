import pandas as pd
import pymongo
import matplotlib.pyplot as plt
import seaborn as sn
import plotly.express as px
import streamlit as st
from streamlit_option_menu import option_menu

ragul = pymongo.MongoClient("mongodb+srv://ragul_s:raguldesire@cluster0.l7eucom.mongodb.net/?retryWrites=true&w=majority")
db = ragul["sample_airbnb"]
col = db["listingsAndReviews"]


#reading preprocced csv data
df = pd.read_csv(".venv\Airbnb_data.csv")

#setting page configuration
st.set_page_config(page_title="Airbnb Data Visualization | By Ragul",layout="wide")


# Creating option menu in the side bar
with st.sidebar:
    selected = option_menu("Menu", ["Home","Overview","Explore"],
                           icons=["house","graph-up-arrow","bar-chart-line"],
                           menu_icon="menu-button-wide",
                           default_index=0,
                           styles={"nav-link": {"font-size": "18px", "text-align": "left", "margin": "-2px", "--hover-color": "#FF5A5F"},
                                   "nav-link-selected": {"background-color": "#6495ED"}}
                           )
    

# HOME PAGE
if selected == "Home":
    # Title Image
    st.header(":violet[*Airbnb Data Visualization*] By Viswanathan")
    col1, col2 = st.columns(2, gap='medium')
    with col1:

        col1.markdown("## :violet[Domain] : Travel Industry, Property Management and Tourism")
        col1.markdown("## :violet[Technologies used] : Python, Pandas, Plotly, Streamlit, MongoDB")
        col1.markdown("## :blue[Overview] : To analyze Airbnb data using MongoDB Atlas, perform data cleaning and preparation, develop interactive visualizations, and create dynamic plots to gain insights into pricing variations, availability patterns, and location-based trends. ")
        col1.markdown("##  :green[About Airbnb] :Airbnb uniquely leverages technology to economically empower millions of people around the world to unlock and monetize their spaces, passions and talents to become hospitality entrepreneurs. Airbnb accommodation marketplace provides access to 6+ million unique places to stay in 81,000 cities and more than 191 countries.")
    with col2:
        col2.markdown("#   ")
        st.image("https://i.gifer.com/7lI8.gif")
        col2.markdown("#   ")
        col2.image(".venv/promote-travel-and-tourism-companies-online-7.png")

# OVERVIEW PAGE
if selected == "Overview":
    tab1, tab2 = st.tabs(["$\huge 📝 RAW DATA $", "$\huge🚀 INSIGHTS $"])

    # RAW DATA TAB
    with tab1:
        # RAW DATA
        col1, col2 = st.columns(2)
        if col1.button("Click to view Raw data"):
            col1.write(col.find_one())
        # DATAFRAME FORMAT
        if col2.button("Click to view Dataframe"):
            col1.write(col.find_one())
            col2.write(df)

    # INSIGHTS TAB
    with tab2:
        # GETTING USER INPUTS
        country = st.sidebar.multiselect('Select a country', sorted(df.country.unique()), sorted(df.country.unique()))
        prop = st.sidebar.multiselect('Select property_type', sorted(df.property_type.unique()),
                                      sorted(df.property_type.unique()))
        room = st.sidebar.multiselect('Select room_type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
        price = st.slider('Select price', df.price.min(), df.price.max(), (df.price.min(), df.price.max()))

        # CONVERTING THE USER INPUT INTO QUERY
        query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

        # CREATING COLUMNS
        col1, col2 = st.columns(2, gap='medium')
        with col1:
            # TOP 10 PROPERTY TYPES BAR CHART
            df1 = df.query(query).groupby(["property_type"]).size().reset_index(name="listings").sort_values(
                by='listings', ascending=False)[:10]
            fig = px.bar(df1,
                         title='Top 10 Property Types',
                         x='listings',
                         y='property_type',
                         orientation='h',
                         color='property_type',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            st.plotly_chart(fig, use_container_width=True)

            # TOP 10 HOSTS BAR CHART
            df2 = df.query(query).groupby(["host_name"]).size().reset_index(name="listings").sort_values(by='listings', ascending=False)[:10]
            fig = px.bar(df2,
                         title='Top 10 Hosts with Highest number of Listings',
                         x='listings',
                         y='host_name',
                         orientation='h',
                         color='host_name',
                         color_continuous_scale=px.colors.sequential.Agsunset)
            fig.update_layout(showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            # TOTAL LISTINGS IN EACH ROOM TYPES PIE CHART
            df1 = df.query(query).groupby(["room_type"]).size().reset_index(name="counts")
            fig = px.pie(df1,
                         title='Total Listings in each Room_types',
                         names='room_type',
                         values='counts',
                         color_discrete_sequence=px.colors.sequential.Rainbow
                         )
            fig.update_traces(textposition='outside', textinfo='value+label')
            st.plotly_chart(fig, use_container_width=True)

            # TOTAL LISTINGS BY COUNTRY CHOROPLETH MAP
            country_df = df.query(query).groupby(['country'], as_index=False)['name'].count().rename(
                columns={'name': 'total_Listings'})
            fig = px.choropleth(country_df,
                                title='Total Listings in each Country',
                                locations='country',
                                locationmode='country names',
                                color='total_Listings',
                                color_continuous_scale=px.colors.sequential.Plasma
                                )
            st.plotly_chart(fig, use_container_width=True)


# EXPLORE PAGE
if selected == "Explore":
    st.markdown("## Explore more about the Airbnb data")

    # GETTING USER INPUTS
    country = st.sidebar.multiselect('Select a country', sorted(df.country.unique()), sorted(df.country.unique()))
    prop = st.sidebar.multiselect('Select property_type', sorted(df.property_type.unique()),
                                  sorted(df.property_type.unique()))
    room = st.sidebar.multiselect('Select room_type', sorted(df.room_type.unique()), sorted(df.room_type.unique()))
    price = st.slider('Select price', df.price.min(), df.price.max(), (df.price.min(), df.price.max()))

    # CONVERTING THE USER INPUT INTO QUERY
    query = f'country in {country} & room_type in {room} & property_type in {prop} & price >= {price[0]} & price <= {price[1]}'

    # HEADING 1
    st.markdown("## Price Analysis")

    # CREATING COLUMNS
    col1, col2 = st.columns(2, gap='medium')
    with col1:
        # AVG PRICE BY ROOM TYPE BARCHART
        pr_df = df.query(query).groupby('room_type', as_index=False)['price'].mean().sort_values(by='price')
        fig = px.bar(data_frame=pr_df,
                     x='room_type',
                     y='price',
                     color='price',
                     title='Avg Price in each Room type'
                     )
        st.plotly_chart(fig, use_container_width=True)

        # HEADING 2
        st.markdown("## Availability Analysis")

        # AVAILABILITY BY ROOM TYPE BOX PLOT
        fig = px.box(data_frame=df.query(query),
                     x='room_type',
                     y='availability_365',
                     color='room_type',
                     title='Availability by Room_type'
                     )
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        # AVG PRICE IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country', as_index=False)['price'].mean()
        fig = px.scatter_geo(data_frame=country_df,
                             locations='country',
                             color='price',
                             hover_data=['price'],
                             locationmode='country names',
                             size='price',
                             title='Avg Price in each Country',
                             color_continuous_scale='agsunset'
                             )
        col2.plotly_chart(fig, use_container_width=True)

        # BLANK SPACE
        st.markdown("#   ")
        st.markdown("#   ")

        # AVG AVAILABILITY IN COUNTRIES SCATTERGEO
        country_df = df.query(query).groupby('country', as_index=False)['availability_365'].mean()
        country_df.availability_365 = country_df.availability_365.astype(int)
        fig = px.scatter_geo(data_frame=country_df,
                             locations='country',
                             color='availability_365',
                             hover_data=['availability_365'],
                             locationmode='country names',
                             size='availability_365',
                             title='Avg Availability in each Country',
                             color_continuous_scale='agsunset'
                             )
        st.plotly_chart(fig, use_container_width=True)
