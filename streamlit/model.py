import streamlit as st
import pandas as pd
import fbprophet
from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric

import plotly.express as px
import pickle


def app():
    st.title('APP2')
    st.write('Welcome to app2')

    df = pd.read_csv("../Data/temp_clean.csv")
    df.rename(columns={'date': 'ds', 'Avg_anomalies': 'y'}, inplace=True)


    st.write("SELECT FORECAST PERIOD") #text displayed
    max_date = df['ds'].max() #compute latest date in the data 

    #periods_input = st.number_input('How many days forecast do you want?', min_value = 15, max_value = 365)
    periods_input = st.text_input('How many days forecast do you want?')

    if periods_input == "":
        print("we need some information")
    else:
        st.write('Wait for the prediction') 
    
        obj = Prophet()
        obj.fit(df)

        #text to be displayed
        st.write("VISUALIZE FORECASTED DATA")  
        st.write("The following plot shows future predicted values. 'yhat' is the predicted value; upper and lower limits are 80% confidence intervals by  default")
        future = obj.make_future_dataframe(periods=int(periods_input))

        fcst = obj.predict(future)  #make prediction for the extended data
        forecast = fcst[['ds', 'yhat', 'yhat_lower', 'yhat_upper']]



        #Choose only the forecasted records (having date after the latest date in #original data)
        forecast_filtered =  forecast[forecast['ds'] > max_date]    
        st.write(forecast_filtered)  #Display some forecasted records
        st.write("The next visual shows the actual (black dots) and predicted (blue line) values over time.")    
        figure1 = obj.plot(fcst) #plot the actual and predicted values
        st.write(figure1)  #display the plot

        #Plot the trends using Prophet.plot_components()
        st.write("The following plots show a high level trend of predicted values, day of week trends and yearly trends (if dataset contains multiple years’ data).Blue shaded area represents upper and lower  confidence intervals.")
        figure2 = obj.plot_components(fcst) 
        st.write(figure2) 

  
        cutoffs = pd.to_datetime(['1918-09-3', '1958-09-3', '2018-09-3'])

        df_cv2 = cross_validation(obj, cutoffs=cutoffs, horizon='365 days')

        df_p = performance_metrics(df_cv2)

        with open('prophet_model.pkl', "wb") as f:
            # dump information to that file
            pickle.dump(obj, f)
       





  

        

        



    
