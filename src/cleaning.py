import pandas as pd

def cleaning_co2_data(df):

    # lo primero que hago es establecer la fila 3 como las columnas de mi data frame
    columns = df.iloc[3]
    df.columns = columns
    
    #como las primeras 4 filas no me interesan, las elimino
    df = df.iloc[4:]

    #cambio el nombre de algunas columnas
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

    # por ultimo elimino algunas columnas que no me interesan
    df = df.drop(["N", "2015", "2016", "2017", "2018"], axis = 1)
    return df


