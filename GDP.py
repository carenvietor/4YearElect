import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial

def test(col,x):
    if col.isdigit():
        return x + col
    else:
        return col

def cleanGDP():
    filename = "data/GDP_1997_2019.csv"
    df = pd.read_csv(filename)

    df.info()
    df = df.drop(['GeoFIPS', 'Region', 'TableName', 'IndustryClassification', 'Unit', 'Description'], axis=1)

    df = df[df["LineCode"].isin([1])]
    df = df.drop(['LineCode'], axis=1)

    df.info()
    df = df[df["GeoName"]!= 'United States']
    df= df.rename(index=str, columns={'GeoName':'states'})

    df['average'] = df.iloc[:,3:].mean(axis=1)
    df.reset_index(inplace=True)
    df = df.rename(mapper=partial(test, x='GDP '),axis='columns')
    return df

def unemployment():
    filename = 'data/emp-unemployment rate.csv'
    df = pd.read_csv(filename, sep=';')
    df.info()

    df = df.drop(['Fips'], axis=1)
    df = df[df["Area"]!= 'United States']
    df = df.rename(index=str, columns={'Area': 'states'})

    df['average'] = df.iloc[:,1:].mean(axis=1)
    df.reset_index(inplace=True)

    df = df.rename(mapper=partial(test, x='unemployment '),axis='columns')
    return df

def capitaperperson():
    filename = 'data/Capita per person.csv'
    df = pd.read_csv(filename)
    df.info()

    df = df.drop(['GeoFips'], axis=1)
    df = df[df["GeoName"] != 'United States']
    df = df.rename(index=str, columns={'GeoName': 'states'})

    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    df = df.rename(mapper=partial(test, x='incomeperson '), axis='columns')
    return df

def education_highschool():
    filename = 'data/Edu_HighSchool.csv'
    df = pd.read_csv(filename, sep=';')
    df.info()
    df = df.rename(index=str, columns={'States': 'states'})
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    df = df.rename(mapper=partial(test, x='highschool '), axis='columns')
    return df

def education_bachelor():
    filename = 'data/Edu_Bachelor.csv'
    df = pd.read_csv(filename, sep=';')
    df.info()
    df = df.rename(index=str, columns={'States': 'states'})
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    df = df.rename(mapper=partial(test, x='bachelor '), axis='columns')
    return df

def education_graduate():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df.info()
    df = df.rename(index=str, columns={'States': 'states'})
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    df = df.rename(mapper=partial(test, x='graduate '), axis='columns')
    return df

def state_facts():
    filename = "data/state_facts.csv"
    df = pd.read_csv(filename, sep=';')
    df.info()
    df = df.drop(['fips'], axis=1)
    df = df.rename(index=str, columns={'area_name': 'states'})
    df = df[df["states"] != 'United States']
    df = df[df['state_abbreviation'].isna()]
    df = df.drop(['state_abbreviation'], axis=1)
    return df

if __name__ == '__main__':
    df= cleanGDP()
    print(df.head())
    df2= unemployment()
    print(df2.head())
    df3= capitaperperson()
    print(df3.head())
    df4= education_highschool()
    print(df4.head())
    df5= education_bachelor()
    print(df5.head())
    df6= education_graduate()
    print(df6.head())
    df7= state_facts()
    print(df7.head())



