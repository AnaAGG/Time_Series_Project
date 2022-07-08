import streamlit as st
import pandas as pd
import fbprophet
from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric


def app():
    st.title('APP2')
    st.write('Welcome to app2')

    df = pd.read_csv("../Data/temp_clean.csv")
    df.rename(columns={'date': 'ds', 'Avg_anomalies': 'y'}, inplace=True)


    st.write("SELECT FORECAST PERIOD") #text displayed

    periods_input = st.number_input('How many days forecast do you want?', min_value = 15, max_value = 365)

    obj = Prophet()
    obj.fit(df)

    #text to be displayed
    st.write("VISUALIZE FORECASTED DATA")  
    st.write("The following plot shows future predicted values. 'yhat' is the predicted value; upper and lower limits are 80% confidence intervals by  default")
    future = obj.make_future_dataframe(periods=periods_input)

    fcst = obj.predict(future)  #make prediction for the extended data
    forecast = fcst[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]

    st.table(forecast.tail(periods_input))



    
