import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial
from scipy import stats

def test(col,x):
    if col.isdigit():
        return x + col
    else:
        return col

def cleanGDP():
    filename = "data/GDP_1997_2019.csv"
    df = pd.read_csv(filename)
    df = df.drop(['GeoFIPS', 'Region', 'TableName', 'IndustryClassification', 'Unit', 'Description'], axis=1)
    df = df[df["LineCode"].isin([1])]
    df = df.drop(['LineCode'], axis=1)
    df = df[df["GeoName"] != 'United States']
    df = df.rename(index=str, columns={'GeoName': 'States'})
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df = df.drop([8])
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df['GDP average'] = df.iloc[:, 2:].mean(axis=1)
    df = df.rename(mapper=partial(test, x='GDP '), axis='columns')
    return df

def unemployment():
    filename = 'data/emp-unemployment rate.csv'
    df = pd.read_csv(filename, sep=';', decimal=',')
    df = df.drop(['Fips'], axis=1)
    df = df[df["Area"]!= 'United States']
    df = df.rename(index=str, columns={'Area': 'States'})
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df = df.drop([8])
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df['unemployment average'] = df.iloc[:,2:].mean(axis=1)
    df = df.rename(mapper=partial(test, x='unemployment '),axis='columns')
    return df

def capitaperperson():
    filename = 'data/Capita per person.csv'
    df = pd.read_csv(filename)
    df = df.drop(['GeoFips'], axis=1)
    df = df[df["GeoName"] != 'United States']
    df = df.rename(index=str, columns={'GeoName': 'States'})
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df = df.drop([8])
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df['income average'] = df.iloc[:, 2:].mean(axis=1)
    df = df.rename(mapper=partial(test, x='incomeperson '), axis='columns')
    return df

def education_highschool():
    filename = 'data/Edu_HighSchool.csv'
    df = pd.read_csv(filename, sep=';')
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df['highschool average'] = df.iloc[:, 2:].mean(axis=1)
    df = df.rename(mapper=partial(test, x='highschool '), axis='columns')
    return df

def education_bachelor():
    filename = 'data/Edu_Bachelor.csv'
    df = pd.read_csv(filename, sep=';')
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df['bachelor average'] = df.iloc[:, 2:].mean(axis=1)
    df = df.rename(mapper=partial(test, x='bachelor '), axis='columns')
    return df

def education_graduate():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df['graduate average'] = df.iloc[:, 1:].mean(axis=1)
    df = df.rename(mapper=partial(test, x='graduate '), axis='columns')
    return df

def state_facts():
    filename = "data/state_facts.csv"
    df = pd.read_csv(filename, sep=';')
    df.info()
    df = df.drop(['fips'], axis=1)
    df = df.rename(index=str, columns={'area_name': 'States'})
    df = df[df["States"] != 'United States']
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    df = df.drop([327])
    df = df[df['state_abbreviation'].isna()]
    df = df.drop(['state_abbreviation'], axis=1)
    df.reset_index(inplace=True)
    df = df.drop(["index"], axis=1)
    return df

def crime():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    filename = "data/crime_and_incarceration_by_state.csv"
    df_crime_total = pd.read_csv(filename, sep=",", usecols=[0, 2, 7])
    df_crime_total.drop(df_crime_total[df_crime_total["jurisdiction"] == "FEDERAL"].index, inplace=True)
    df_crime_total = df_crime_total.rename(index=str, columns={'jurisdiction': 'States'})
    new_rec = {}
    for item in df_crime_total.itertuples():
        if item.States in new_rec.keys():
            rec = new_rec[item.States]
            rec[str(item.year) + ' crime'] = item.violent_crime_total
        else:
            new_rec[item.States] = {str(item.year) + ' crime': item.violent_crime_total}
    df_crime_total = pd.DataFrame.from_dict(new_rec, orient='index')
    df_crime_total = df_crime_total.reset_index()
    df_crime_total['index'] = df['States'].values
    df_crime_total = df_crime_total.rename(index=str, columns={'index': 'States'})
    df_crime_total["crime average"] = df_crime_total.iloc[:, 2:].mean(axis=1)
    return df_crime_total


def murder():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    filename = "data/crime_and_incarceration_by_state.csv"
    df_murder_manslaughter = pd.read_csv(filename, sep=",", usecols=[0, 2, 8])
    df_murder_manslaughter.drop(df_murder_manslaughter[df_murder_manslaughter["jurisdiction"] == "FEDERAL"].index,
                                inplace=True)
    df_murder_manslaughter = df_murder_manslaughter.rename(index=str, columns={'jurisdiction': 'States'})
    new_rec = {}
    for item in df_murder_manslaughter.itertuples():
        if item.States in new_rec.keys():
            rec = new_rec[item.States]
            rec[str(item.year) + ' murder'] = item.murder_manslaughter
        else:
            new_rec[item.States] = {str(item.year) + ' murder': item.murder_manslaughter}
    df_murder_manslaughter = pd.DataFrame.from_dict(new_rec, orient='index')
    df_murder_manslaughter = df_murder_manslaughter.reset_index()
    df_murder_manslaughter['index'] = df['States'].values
    df_murder_manslaughter = df_murder_manslaughter.rename(index=str, columns={'index': 'States'})
    df_murder_manslaughter["murder average"] = df_murder_manslaughter.iloc[:, 2:].mean(axis=1)
    return df_murder_manslaughter

def robbery():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    filename = "data/crime_and_incarceration_by_state.csv"
    df_robbery = pd.read_csv(filename, sep=",", usecols=[0, 2, 11])
    df_robbery.drop(df_robbery[df_robbery["jurisdiction"] == "FEDERAL"].index, inplace=True)
    df_robbery = df_robbery.rename(index=str, columns={'jurisdiction': 'States'})
    new_rec = {}
    for item in df_robbery.itertuples():
        if item.States in new_rec.keys():
            rec = new_rec[item.States]
            rec[str(item.year) + ' robbery'] = item.robbery
        else:
            new_rec[item.States] = {str(item.year) + ' robbery': item.robbery}
    df_robbery = pd.DataFrame.from_dict(new_rec, orient='index')
    df_robbery = df_robbery.reset_index()
    df_robbery['index'] = df['States'].values
    df_robbery = df_robbery.rename(index=str, columns={'index': 'States'})
    df_robbery["robbery average"] = df_robbery.iloc[:, 2:].mean(axis=1)
    return df_robbery


def rape():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)

    filename = "data/crime_and_incarceration_by_state.csv"
    df_rape_legacy = pd.read_csv(filename, sep=",", usecols=[0, 2, 9])
    df_rape_legacy.drop(df_rape_legacy[df_rape_legacy["jurisdiction"] == "FEDERAL"].index, inplace=True)
    df_rape_legacy = df_rape_legacy.rename(index=str, columns={'jurisdiction': 'States'})
    new_rec = {}
    for item in df_rape_legacy.itertuples():
        if item.States in new_rec.keys():
            rec = new_rec[item.States]
            rec[str(item.year) + ' rape'] = item.rape_legacy
        else:
            new_rec[item.States] = {str(item.year) + ' rape': item.rape_legacy}
    df_rape_legacy = pd.DataFrame.from_dict(new_rec, orient='index')
    df_rape_legacy = df_rape_legacy.reset_index()
    df_rape_legacy['index'] = df['States'].values
    df_rape_legacy = df_rape_legacy.rename(index=str, columns={'index': 'States'})
    df_rape_legacy= df_rape_legacy.drop(['2016 rape'], axis=1)
    df_rape_legacy["rape average"] = df_rape_legacy.iloc[:, 2:].mean(axis=1)
    return df_rape_legacy


def socialmetrics():
    df_social=pd.read_csv('data/Sociological metrics.csv')
    df_social = df_social.rename(index=str, columns={'State': 'States'})
    df_social= df_social.sort_values(by='States')
    df_social.reset_index(inplace=True)
    df_social= df_social.drop(['index'], axis=1)
    return df_social

def withouthealth():
    filename = 'data/Edu_Graduate.csv'
    df = pd.read_csv(filename, sep=';')
    df['average'] = df.iloc[:, 1:].mean(axis=1)
    df.reset_index(inplace=True)
    df = df.rename(mapper=partial(test, x='graduate '), axis='columns')
    df_nohealth = pd.read_csv('data/without_health_2013_2016.csv', sep =';', decimal=',', usecols=[0,2,4,6,8])
    df_nohealth.columns = ['States', '2013 Uninsured', '2014 Uninsured', '2015 Uninsured', '2016 Uninsured']
    df_nohealth= df_nohealth.drop([8])
    df_nohealth = df_nohealth.dropna()
    df_nohealth = df_nohealth.reset_index()
    df_nohealth['States'] = df['States'].values
    df_nohealth = df_nohealth.drop(['index'], axis=1)
    df_nohealth["uninsured average"] = df_nohealth.iloc[:, 2:].mean(axis=1)
    return df_nohealth

def healthinsurance():
    df_health=pd.read_csv('data/Health Insur_2008 -2019.csv',sep =';',decimal=',')
    df_health.columns=['States','Coverage','2019 Insured','2018 Insured','2017 Insured','2016 Insured', '2015 Insured', '2014 Insured','2013 Insured','2012 Insured','2011 Insured','2010 Insured','2009 Insured','2008 Insured']
    df_health = df_health.reset_index()
    df_health = df_health[df_health['Coverage'] == 'Any coverage']
    df_health = df_health.drop(['Coverage'], axis=1)
    df_health= df_health.drop([89])
    df_health = df_health.reset_index()
    df_health = df_health.drop(['level_0'], axis=1)
    df_health = df_health.drop(['index'], axis=1)
    df_health["insured average"] = df_health.iloc[:, 2:].mean(axis=1)
    return df_health

def datavotes():
    df_votes=pd.read_csv('data/DataVotes 1976-2016.csv',usecols=[0,1,8,10])
    df_votes= df_votes.loc[df_votes.groupby(['state', 'year'])['candidatevotes'].idxmax()]
    new_rec = {}
    for item in df_votes.itertuples():
        if item.state in new_rec.keys():
            rec = new_rec[item.state]
            rec[str(item.year) + ' winner'] = item.party
            rec[str(item.year) + ' votes'] = item.candidatevotes
        else:
            new_rec[item.state] = {str(item.year) + ' winner': item.party, str(item.year) + ' votes': item.candidatevotes}
    df_votes = pd.DataFrame.from_dict(new_rec, orient= 'index')
    df_votes = df_votes.drop(['District of Columbia'])
    df_votes = df_votes.reset_index()
    df_votes = df_votes.rename(index=str, columns={'index': 'States'})
    return df_votes

if __name__ == '__main__':
    df= cleanGDP()
    print(df)
    df2= unemployment()
    print(df2)
    df3= capitaperperson()
    print(df3)
    df4= education_highschool()
    print(df4)
    df5= education_bachelor()
    print(df5)
    df6= education_graduate()
    print(df6)
    df7= state_facts()
    print(df7)
    df_crime_total = crime()
    print(df_crime_total)
    df_murder_manslaughter = murder()
    print(df_murder_manslaughter)
    df_robbery = robbery()
    print(df_robbery)
    df_rape_legacy = rape()
    print(df_rape_legacy)
    df_social = socialmetrics()
    print(df_social)
    df_nohealth = withouthealth()
    print(df_nohealth)
    df_health = healthinsurance()
    print(df_health)
    df_votes = datavotes()
    print(df_votes)

#merge
df_total1= pd.merge(df,df2, on='States')
print(df_total1)

df_total2= pd.merge(df_total1,df3, on='States')
print(df_total2)

df_total3= pd.merge(df_total2,df4, on='States')
print(df_total3)

df_total4= pd.merge(df_total3,df5, on='States')
print(df_total4)

df_total5= pd.merge(df_total4,df6, on='States')
print(df_total5)

df_total6= pd.merge(df_total5,df7, on='States')
print(df_total6)

df_total7= pd.merge(df_total6,df_crime_total, on='States')
print(df_total7)

df_total8= pd.merge(df_total7,df_murder_manslaughter, on='States')
print(df_total8)

df_total9= pd.merge(df_total8,df_robbery, on='States')
print(df_total9)

df_total10= pd.merge(df_total9,df_rape_legacy, on='States')
print(df_total10)

df_total11= pd.merge(df_total10,df_social, on='States')
print(df_total11)

df_total12= pd.merge(df_total11,df_nohealth, on='States')
print(df_total12)

df_total13= pd.merge(df_total12,df_health, on='States')
print(df_total13)

df_final= pd.merge(df_total13,df_votes, on='States')
print(df_final)


#export
df_final.to_csv('finaldata.csv',index=False)