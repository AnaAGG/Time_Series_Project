import streamlit as st
import pandas as pd
import plotly.express as px

def app():

    # Creating a title for the page
    st.title('Home 🌡')
    st.write('Welcome to the temperature prediction app')

    
    df = pd.read_csv("../Data/temp_clean.csv")
    # CSS to inject contained in a string
    hide_table_row_index = """
                <style>
                tbody th {display:none}
                .blank {display:none}
                </style>
                """

    # Inject CSS with Markdown
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    # Display a static table
    st.table(df.head(10))

    st.table(df.tail(10))

    def pie_chart_genus():
        

        fig = px.line(df, x='date', y = "Avg_anomalies", title = "Evolution of temperature over time")
        

        return fig

    st.plotly_chart(pie_chart_genus())
    