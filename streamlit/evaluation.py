from fbprophet import Prophet
from fbprophet.diagnostics import performance_metrics
from fbprophet.diagnostics import cross_validation
from fbprophet.plot import plot_cross_validation_metric

import plotly.express as px
import pickle

import streamlit as st
import pandas as pd

def app():

    with st.expander("More info on evaluation metrics"):
     st.write("""
         
    The following metrics can be computed to evaluate model performance:

    - **Mean Absolute Percentage Error (MAPE)**: Measures the average absolute size of each error in percentage of the truth. This metric is not ideal for low-volume forecasts, because being off by a few units can increase the percentage error signficantly. It can't be calculated if the true value is 0 (here samples are excluded from calculation if true value is 0).
    
    - **Symmetric Mean Absolute Percentage Error (SMAPE)**: Slight variation of the MAPE, it measures the average absolute size of each error in percentage of the truth summed with the forecast. It is therefore a bit more robust to 0 values.
    
    - **Mean Squared Error (MSE)**: Measures the average squared difference between forecasts and true values. This metric is not ideal with noisy data, because a very bad forecast can increase the global error signficantly as all errors are squared.
    
    - **Root Mean Squared Error (RMSE)**: Square root of the MSE. This metric is more robust to outliers than the MSE, as the square root limits the impact of large errors in the global error.
    
    - **Mean Absolute Error (MAE)**: Measures the average absolute error. This metric can be interpreted as the absolute average distance between the best possible fit and the forecast.
     """)


    with open('prophet_model.pkl', "rb") as f:
        obj = pickle.load(f)


    cutoffs = pd.to_datetime(['1918-09-3', '1958-09-3', '2018-09-3'])

    df_cv2 = cross_validation(obj, cutoffs=cutoffs, horizon='365 days')

    df_p = performance_metrics(df_cv2)

    def create_plot(df_, column):
                df_ = round(df_, 3)
                df_["horizon"] = df_["horizon"].astype(str)
                fig = px.bar(df_, x = "horizon", y = f"{column}",color = "horizon" , template='plotly_white', text='mse', color_discrete_sequence=px.colors.qualitative.Prism)
                fig.update_traces(textfont_size=12, textangle=0, textposition="outside", cliponaxis=False, marker_line_width=1.5, opacity=1, showlegend=False)

                return fig

    st.markdown("# Model Evaluations")
    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(create_plot(df_p, "mse"))
        
    with col2:
        st.plotly_chart(create_plot(df_p, "rmse"))

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(create_plot(df_p, "mae"))
        
    with col4:
        st.plotly_chart(create_plot(df_p, "mdape"))