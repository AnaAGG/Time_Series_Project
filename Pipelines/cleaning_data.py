# Adding the parent directory to the path so that we can import the cleaning module.
import sys
sys.path.append("../")

import pandas as pd
import numpy as np
import calendar
from datetime import datetime

import src.cleaning as cl

# Reading the data from the file and displaying the first 5 rows.
print("Reading data")
temp = pd.read_csv("../Data/SST_Global.csv")

# Cleaning the data and saving it to a csv file.
print("Cleaning data")
df = cl.cleaning_temp_data(temp)
df.to_csv("temp_complete_clean.csv")


