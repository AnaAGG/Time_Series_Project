import plotly.express as px

def pie_chart_genus(df):
    fig = px.line(df, x='date', y = "Avg_anomalies", title = "Evolution of temperature over time", color_discrete_sequence=["#FF0066"]  )
    return fig