import streamlit as st
import pandas as pd
import plotly.express as px
import json


def app():

    # Creating a title for the page
    st.title('Home')
    st.image("images/main.jpeg", use_column_width= True)
    st.write(""" 

    # The problem and objective
    Global climate change has already had observable effects on the environment. Glaciers have shrunk, ice on rivers and lakes is breaking up earlier, plant and animal ranges have shifted and trees are flowering sooner.

    Effects that scientists had predicted in the past would result from global climate change are now occurring: loss of sea ice, accelerated sea level rise and longer, more intense heat waves.

    According to the IPCC, the extent of climate change effects on individual regions will vary over time and with the ability of different societal and environmental systems to mitigate or adapt to change.

    The IPCC predicts that increases in global mean temperature of less than 1.8 to 5.4 degrees Fahrenheit (1 to 3 degrees Celsius) above 1990 levels will produce beneficial impacts in some regions and harmful ones in others. Net annual costs will increase over time as global temperatures increase.

    On the other hand, at the dawn of the industrial revolution, the Earth’s atmosphere contained 278 parts of CO₂ per million. Today, after more than two and a half centuries of fossil fuel use, that figure is around 414 parts per million (ppm). If the build-up of CO₂ continues at current rates, by 2060 it will have passed 560 ppm – more than double the level of pre-industrial times.

    Exactly how the climate will respond to all this extra CO₂ is one of the central questions in climate science.

    The aim of this project is to make predictions of the evolution of temperature and CO2 emissions through Time Series Analysis using Prophet python library.
        
        
    
    """)
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    df = pd.read_csv("../Data/temp_clean.csv")

    col1, col2 = st.columns(2)
    with col1:
        st.table(df.head(10))
    with col2:
        st.table(df.tail(10))


    # Display a static table
    

    

    def pie_chart_genus():
        

        fig = px.line(df, x='date', y = "Avg_anomalies", title = "Evolution of temperature over time", color_discrete_sequence=["#FF0066"]  )
        

        return fig

    st.plotly_chart(pie_chart_genus(), use_container_width= True)


    st.markdown("# Information around the world")
    full = pd.read_csv("../Data/temp_world_clean.csv", index_col = 0)

    full = full[full["Element"] == "Temperature change"]
    full.drop("Element", axis = 1, inplace = True)

    st.table(full.head())


    df_ordenado_limpio = pd.read_csv("../Data/temp_world_clean.csv")

    with open('../Data/countries.geojson') as response:
        counties = json.load(response)

    target_states = list(df_ordenado_limpio.Area.unique())


    st.plotly_chart(px.choropleth_mapbox(df_ordenado_limpio, locations='Area', geojson = counties 
    , color='Values',
                            color_continuous_scale="Viridis",
                            range_color=(0, 2),featureidkey="properties.ADMIN",
                            mapbox_style="carto-positron",
                            zoom=0.1, center = {"lat": 37.0902, "lon": -95.7129},
                            opacity=0.5,
                            labels={'Values':'temperature'}
                            ), use_container_width= True)

    paises = list(full["Area"].unique())

    pais = st.selectbox("Elige un pais",["Choose a country"] + paises)

    if pais == "Choose a country":
        st.write("Please enter a country")
    else: 
        st.plotly_chart(px.line((full[full["Area"] == pais ].groupby("Year").mean()).reset_index(), 
        x = "Year", y = "Values", color_discrete_sequence=["#FF0066"] ), use_container_width= True)



