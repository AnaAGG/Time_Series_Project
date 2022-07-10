import streamlit as st
import pandas as pd
import fbprophet
from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric

import plotly.express as px
import pickle
from PIL import Image
from datetime import datetime

def app():
    st.title('Temperature prediction using Prophet')

    
    # Reading the data from the csv file and storing it in a dataframe called df.
    df = pd.read_csv("../Data/temp_clean.csv")

    # Renaming the columns in the dataframe.
    df.rename(columns={'date': 'ds', 'Avg_anomalies': 'y'}, inplace=True)


    #compute latest date in the data 
    max_date = df['ds'].max() 

    # Asking the user to input the number of days they want to forecast.
    periods_input = st.text_input('How many days forecast do you want?')




    # A condition that checks if the user has entered a value in the text box. If the user has not
    # entered a value, then the image is displayed.
    if periods_input == "":
        print("we need some information")
        st.image("images/portada_modelo_temperature.png", use_column_width= True)


    else:    
        # initializing teh Prophet model
        with st.spinner("⏳ Waiting for the model ⏳"):
            obj = Prophet()
            obj.fit(df)

            
            # Creating a dataframe with the dates of the original dataframe plus the number of days that
            # the user has entered.
            future = obj.make_future_dataframe(periods=int(periods_input))

            #make prediction for the extended data
            fcst = obj.predict(future) 

            # Creating a new dataframe with the columns ds, yhat, yhat_lower and yhat_upper.
            forecast = round(fcst[['ds', 'yhat', 'yhat_lower', 'yhat_upper']], 2)
        



            #Choose only the forecasted records (having date after the latest date in #original data)
            forecast_filtered =  forecast[forecast['ds'] > max_date]   

            max_temp_predicted = round(forecast_filtered["yhat"].max(), 2)
            min_temp_predicted = round(forecast_filtered["yhat"].min(), 2)

            date_max_temp = str(forecast_filtered[forecast_filtered["yhat"] == max_temp_predicted]["ds"].values[0]).split("T")[0]
            date_min_temp = str(forecast_filtered[forecast_filtered["yhat"] == min_temp_predicted]["ds"].values[0]).split("T")[0]


            col1, col2 = st.columns(2)
            # Creating a column in the app.
            with col1:
                # Creating a title with the max temperature predicted and the date.
                original_title = f'<p style="font-weight:bold; color:#FF0066; font-size: 20px;text-align: center; ">MAX TEMP PREDICTED WAS FOR {date_max_temp}</p>'
                st.markdown(original_title, unsafe_allow_html=True)

                # Creating a title with the max temperature predicted and the date.
                value = f'<p style="font-weight:bold;font-size: 15px; text-align: center; ">{max_temp_predicted}</p>'
                st.markdown(value, unsafe_allow_html= True)

            with col2:
                # Creating a title with the min temperature predicted and the date.
                original_title = f'<p style="font-weight:bold; color:#FF0066; font-size: 20px;">MIN TEMP PREDICTED WAS FOR {date_min_temp}</p>'
                st.markdown(original_title, unsafe_allow_html=True)

                # Creating a title with the max temperature predicted and the date.
                value = f'<p style="font-weight:bold;font-size: 15px; text-align: center; ">{min_temp_predicted}</p>'
                st.markdown(value, unsafe_allow_html=True)







            
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
        





  

        

        



    
