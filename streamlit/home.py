import streamlit as st
import pandas as pd
import plotly.express as px

def app():

    # Creating a title for the page
    st.title('Home 🌡')
    st.write('Welcome to the temperature prediction app')
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
        

        fig = px.line(df, x='date', y = "Avg_anomalies", title = "Evolution of temperature over time")
        

        return fig

    st.plotly_chart(pie_chart_genus())
    