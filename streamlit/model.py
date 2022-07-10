from calendar import month_abbr
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
        


            st.markdown("## Main results of the model")
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


            

            
            # Creating a title with the text "The plot of the prediction for the days you specified"
            # and then it is creating a plot with the dataframe forecast_filtered and the columns ds
            # and yhat.
            plot_predicted = f'<p style="font-weight:bold;font-size: 20px; color:#FF0066; ">The plot of the prediction for the days you specified </p>'
            st.markdown(plot_predicted, unsafe_allow_html= True)
            st.plotly_chart(px.line(forecast_filtered, x = "ds", y = "yhat"))


            # Creating a new dataframe with the data that is before the max date.
            forecast_train = forecast[forecast['ds'] < max_date]

           
            st.markdown("### Comparison of predicted vs real values for 2018 and January")
            col3, col4 = st.columns(2)
            with col3: 
            
                
                # Creating a new column in the dataframe forecast_train called real and it is
                # assigning the values of the column y of the dataframe df to the column real.
                forecast_train["real"] = df["y"]
                st.plotly_chart(px.line(forecast_train[forecast_train["ds"].dt.year == 2018], x = "ds", y = ["yhat", "real"], title = "Comparison of predicted vs real values for 2018" ))
            with col4: 
                forecast_train["real"] = df["y"]
                st.plotly_chart(px.line(forecast_train[forecast_train["ds"].dt.month == 1], x = "ds", y = ["yhat", "real"], title = "Comparison of predicted vs real values for January"))


            st.markdown("### Do you want more information? Here you can select different years and month to explore the results")

            col5, col6 = st.columns(2)

            with col5: 
                year_ = st.text_input("From which year do you want to see the comparison between predicted and actual?")
                if year_ == "": 
                    st.write("We need a year")
                else:
                    fig = px.line(forecast_train[forecast_train["ds"].dt.year == int(year_)], x = "ds", y = ["yhat", "real"])
                    fig.update(layout_showlegend = False)
                    st.plotly_chart(fig)

            with col6: 
                month_ = st.text_input("From which month do you want to see the comparison between predicted and actual?")

                if month_ == "": 
                    st.write("We need a month")
                else:  
                    fig = px.line(forecast_train[forecast_train["ds"].dt.month == int(month_)], x = "ds", y = ["yhat", "real"])
                    fig.update(layout_showlegend = False)
                    st.plotly_chart(fig)


            with st.expander("CONCLUSIONS"):
                st.write("""
                Note, the colours in the graphs indicate: 

                - Blue : predicted values

                - Red: actual values


                If we explore the years and months a bit, we see that our model is not able to capture the changes in temperature changes well. This makes our model with Prophet not the best suited to capture the patterns. 

                For this reason, I decided to make another approach using PyCaret. 
                                    
                """)

        st.markdown("## Model Evaluation")

        cutoffs = pd.to_datetime(['1918-09-3', '1958-09-3', '2018-09-3'])

        df_cv2 = cross_validation(obj, cutoffs=cutoffs, horizon='365 days')

        df_p = performance_metrics(df_cv2)

        


        with st.expander("More info on evaluation metrics"):
            st.write("""
                
            The following metrics can be computed to evaluate model performance:
                        
            - **Mean Squared Error (MSE)**: Measures the average squared difference between forecasts and true values. This metric is not ideal with noisy data, because a very bad forecast can increase the global error signficantly as all errors are squared.
            
            - **Root Mean Squared Error (RMSE)**: Square root of the MSE. This metric is more robust to outliers than the MSE, as the square root limits the impact of large errors in the global error.
            
            - **Mean Absolute Error (MAE)**: Measures the average absolute error. This metric can be interpreted as the absolute average distance between the best possible fit and the forecast.
            """)
            if st.button("Show metric formulas"):
                    st.write("hola")

                    st.latex(r"""
                    RMSE = \sqrt{\frac{1}{n}\Sigma_{i=1}^{n}{\Big(\frac{d_i -f_i}{\sigma_i}\Big)^2}}
                    """)

                    st.latex(r"""
                    MSE = {\frac{1}{n}\Sigma_{i=1}^{n}{\Big(\frac{d_i -f_i}{\sigma_i}\Big)}}
                    """)

                    st.latex(r"""
                    MAE = (\frac{1}{n})\sum_{i=1}^{n}\left | y_{i} - x_{i} \right |

                    """)

        with st.expander("How to evaluate my model?"):
            st.write("""
            The following table and plots allow you to evaluate model performance. Go to the Evaluation section of the sidebar if you wish to customize evaluation settings by:

            - Adding more metrics

            - Changing evaluation period
            
            - Computing performance at a different granularity to understand on which periods performance drops
            """)


        col5, col6, col7 = st.columns(3)
        with col5:
            original_title = '<p style="font-weight:bold; color:#FF0066; font-size: 20px;">MSE</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.markdown(round(df_p["mse"].mean(), 2))
        with col6:
            original_title = '<p style="font-weight:bold; color:#FF0066; font-size: 20px;">RMSE</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.markdown(round(df_p["rmse"].mean(),2))
        with col7:
            original_title = '<p style="font-weight:bold; color:#FF0066; font-size: 20px;">MAE</p>'
            st.markdown(original_title, unsafe_allow_html=True)
            st.markdown(round(df_p["mae"].mean(),2))

      

        def create_plot(df_, column):
                    df_ = round(df_, 3)
                    df_["horizon"] = df_["horizon"].astype(str)
                    fig = px.bar(df_, x = "horizon", y = f"{column}",color = "horizon" , template='plotly_white', text='mse', color_discrete_sequence=px.colors.qualitative.Prism)
                    fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_line_width=1.5, opacity=1, showlegend=False)

                    return fig

        col1, col2  = st.columns(2)
        with col1:
            st.plotly_chart(create_plot(df_p, "mse"))
            
        with col2:
            st.plotly_chart(create_plot(df_p, "rmse"))

     
        st.plotly_chart(create_plot(df_p, "mae"))
        
