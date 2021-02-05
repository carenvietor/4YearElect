import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

filename = "GDP_1997_2019.csv"
df = pd.read_csv(filename)

df.info()
df = df.drop(['GeoFIPS', 'Region', 'TableName', 'IndustryClassification'], axis = 1)

df = df[df["LineCode"].isin([1,2,3])]

df.info()
