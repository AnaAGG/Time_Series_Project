import pandas as pd
import numpy as np

def cleaning_co2_data(df):
    """
    This function clean the co2 dataframe
    Args:
        df (dataframe): the complete CO2 information before cleaning

    Returns:
        df (dataframe): the complete CO2 information after cleaning
    """

    # Setting the column names to the 4th row of the dataframe.
    columns = df.iloc[3]
    df.columns = columns
    

    # Removing the first 4 rows of the dataframe.
    df = df.iloc[4:]


    # Setting the column names to the 4th row of the dataframe.
    columns2 = ['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code',
       '1960', '1961', '1962', '1963', '1964', '1965', '1966',
       '1967', '1968', '1969', '1970', '1971', '1972', '1973',
       '1974', '1975', '1976', '1977', '1978', '1979', '1980',
       '1981', '1982', '1983', '1984', '1985', '1986', '1987',
       '1988', '1989', '1990', '1991', '1992', '1993', '1994',
       '1995', '1996', '1997', '1998', '1999', '2000', '2001',
       '2002', '2003', '2004', '2005', '2006', '2007', '2008',
       '2009', '2010', '2011', '2012', '2013', '2014', '2015',
       '2016', '2017', '2018', 'N']
    df.columns  = columns2

    # Dropping the columns N, 2015, 2016, 2017, 2018 from the dataframe.
    df = df.drop(["N", "2015", "2016", "2017", "2018", "Indicator Name", "Indicator Code"], axis = 1)
    return df


def cleaning_temp_data(df):
    # como todos los datos de este csv estan en el indice lo que tengo que haces es resetear el indice para que cada una
    # de las columnas del indice se convierta en una columna de verdad. 
    # una vez que tengo esto hecho,le pongo nombre a las columnas. 
    df.reset_index(inplace=True)
    columns = ["Year", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec", "J-D", "D-N", "DJF", "MAM", "JJA", "SON"]
    df.columns = columns
    df = df.iloc[1:]
    return df

def merge_data(df, new_df):
    d = df.T
    d = d.iloc[1:]
    
    lst = []
    for i in range(1,141):
        lst.append(d[i].tolist())
    lst2 = []
    for i in lst:
        for n in i:
            lst2.append(n)
            
    new_df["Avg_anomalies"] = pd.DataFrame({'col':lst2})
    # En times series la fecha debe estar como indice
    new_df['Datetimes'] = pd.to_datetime(new_df['date'])
    new_df.drop("Datetimes", axis = 1, inplace = True)
    new_df.set_index("date", inplace = True)
    new_df.tail()
    return new_df


def clean_anomaly_value(raw_value):
    # Define function to convert values to floats, and return a 'NaN = Not a Number' if this is not possible

    try:
        return float(raw_value)
    except:
        return np.NaN