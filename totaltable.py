import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from functools import partial
from scipy import stats
import matplotlib.patches as mpatches


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
    df = df.replace(',', '')
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

# GDP swing states
print(df)  # GDP
x_labels = df.columns.tolist()[1:-1]  # Jahre
selected_states = {'Nevada': 'green', 'Florida': 'blue', 'North Carolina': 'yellow', 'New Hampshire': 'red',
                   'Pennsylvania': 'orange'}
for idx, row in df.iterrows():
    if row['States'] not in selected_states.keys():
        continue
    y_values = row[1:-1].tolist()
    plt.plot(y_values, color=selected_states[row['States']])
plt.title('GDP of Swing States')
plt.xlabel('Years')
plt.ylabel('GDP')
plt.xticks(np.arange(len(x_labels)), x_labels, rotation=90)
legend = []
for key,value in selected_states.items():
    legend.append(mpatches.Patch(color=value, label=key))
plt.legend(handles=legend)
plt.grid(False)
plt.show()

#maxGDP by swing states
print(df)
swingGDP = df.iloc[[8, 27, 28, 32, 37], :]
topswingGDP = swingGDP['GDP average'].max()
maxGDPstate= swingGDP[swingGDP['GDP average'] == topswingGDP]['States'].str
print(topswingGDP)

#maxGDP by state
topGDP =df['GDP average'].max()
maxGDPstate= df[df['GDP average'] == topGDP]['States'].str
print(topGDP)

#minGDP by state
flopGDP =df['GDP average'].min()
minGDPstate= df[df['GDP average'] == topGDP]['States'].str
print(topGDP)

#maxGDP by swing states
print(df)
swingGDP = df.iloc[[8, 27, 28, 32, 37], :]
flopswingGDP = swingGDP['GDP average'].max()
minGDPstate= swingGDP[swingGDP['GDP average'] == flopswingGDP]['States'].str
print(flopswingGDP)

#income per person per swing state
print(df3)
x_labels = df3.columns.tolist()[1:-1]  # Jahre
selected_states = {'Nevada': 'green', 'Florida': 'blue', 'North Carolina': 'yellow', 'New Hampshire': 'red',
                   'Pennsylvania': 'orange'}
for idx, row in df3.iterrows():
    if row['States'] not in selected_states.keys():
        continue
    y_values = row[1:-1].tolist()
    plt.plot(y_values, color=selected_states[row['States']])
plt.title('Income per person of Swing States')
plt.xlabel('Years')
plt.ylabel('Income per person')
plt.xticks(np.arange(len(x_labels)), x_labels, rotation=90)
legend = []
for key,value in selected_states.items():
    legend.append(mpatches.Patch(color=value, label=key))
plt.legend(handles=legend)
plt.grid(False)
plt.show()


#crime per swing state
print(df_crime_total)
x_labels = df_crime_total.columns.tolist()[1:-1]  # Jahre
x_labels = ['2001', '2002', '2003', '2004', '2005', '2006', '2007', '2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016']
selected_states = {'Nevada': 'green', 'Florida': 'blue', 'North Carolina': 'yellow', 'New Hampshire': 'red',
                   'Pennsylvania': 'orange'}
for idx, row in df_crime_total.iterrows():
    if row['States'] not in selected_states.keys():
        continue
    y_values = row[1:-1].tolist()
    plt.plot(y_values, color=selected_states[row['States']])
plt.title('Crime rate per Swing States')
plt.xlabel('Years')
plt.ylabel('Crime rate')
plt.xticks(np.arange(len(x_labels)), x_labels, rotation=90)
legend = []
for key,value in selected_states.items():
    legend.append(mpatches.Patch(color=value, label=key))
plt.legend(handles=legend)
plt.grid(False)
plt.show()

#Insured swing states
print(df_health)
x_labels = df_health.columns.tolist()[1:-1]  # Jahre
x_labels= ['2008', '2009', '2010', '2011','2012', '2013', '2014', '2015', '2016', '2017', '2018', '2019']
selected_states = {'Nevada': 'green', 'Florida': 'blue', 'North Carolina': 'yellow', 'New Hampshire': 'red',
                   'Pennsylvania': 'orange'}
for idx, row in df_health.iterrows():
    if row['States'] not in selected_states.keys():
        continue
    y_values = row[1:-1].tolist()
    plt.plot(y_values, color=selected_states[row['States']])
plt.title('Insurance rate per Swing States')
plt.xlabel('Years')
plt.ylabel('Insurance rate')
plt.xticks(np.arange(len(x_labels)), x_labels, rotation=90)
legend = []
for key,value in selected_states.items():
    legend.append(mpatches.Patch(color=value, label=key))
plt.legend(handles=legend)
plt.show()

#election per swing state total votes
print(df_votes)
df_votes_swingtotal = df_votes.drop(['1976 winner','1980 winner','1984 winner','1988 winner','1992 winner','1996 winner','2000 winner', '2004 winner', '2008 winner', '2012 winner', '2016 winner'], axis=1)
x_labels = ['1976','1980','1984','1988','1992','1996','2000', '2004', '2008', '2012', '2016']
selected_states = {'Nevada': 'green', 'Florida': 'blue', 'North Carolina': 'yellow', 'New Hampshire': 'red',
                   'Pennsylvania': 'orange'}
for idx, row in df_votes_swingtotal.iterrows():
    if row['States'] not in selected_states.keys():
        continue
    y_values = row[1:].tolist()
    plt.plot(y_values, color=selected_states[row['States']])
plt.title('Total Votes per Swing States')
plt.xlabel('Years')
plt.ylabel('Total votes')
plt.xticks(np.arange(len(x_labels)), x_labels, rotation=90)
legend = []
for key,value in selected_states.items():
    legend.append(mpatches.Patch(color=value, label=key))
plt.legend(handles=legend)
plt.grid(False)
plt.show()

#unemployment
highunemployment = df2.nlargest(5, ['unemployment average'])
print(highunemployment)
x = list(highunemployment['States'])
y = list(highunemployment['unemployment average'])
plt.bar(x,y, color='red')
plt.xlabel('States')
plt.ylabel('Unemployment in %')
plt.title('Top 5 States with highest unemployment rate')
plt.grid(False)
plt.show()


lowunemployment = df2.nsmallest(5,['unemployment average'])
print(lowunemployment)
x = list(lowunemployment['States'])
y = list(lowunemployment['unemployment average'])
plt.bar(x,y, color='blue')
plt.xlabel('States')
plt.ylabel('Unemployment in %')
plt.title('Top 5 States with lowest unemployment rate')
plt.grid(False)
plt.show()


#seaborn boxplot GDP avergae
sns.set_theme(style='whitegrid', palette='muted')
sns.swarmplot(data = df2,x='States', y= 'unemployment average')
plt.xticks(rotation =70)
plt.show()

#seaborn boxplot GDP over the years
df_GDPbox = pd.DataFrame(data = df, columns =['GDP 1997', 'GDP 1998', 'GDP 1999', 'GDP 2000', 'GDP 2001', 'GDP 2002', 'GDP 2003', 'GDP 2004', 'GDP 2005', 'GDP 2006', 'GDP 2007', 'GDP 2008', 'GDP 2009', 'GDP 2010', 'GDP 2011', 'GDP 2012', 'GDP 2013', 'GDP 2014', 'GDP 2015', 'GDP 2016', 'GDP 2017', 'GDP 2018', 'GDP 2019'])
sns.boxplot(x="variable", y="value", data=pd.melt(df_GDPbox))
plt.xticks(rotation =70)
plt.show()

#seaborn boxplot GDP per states
df= df.sort_values(by=['GDP average'])
df_GDPboxstates = pd.melt(df,id_vars= ['States'], value_vars= ['GDP 1997', 'GDP 1998', 'GDP 1999', 'GDP 2000', 'GDP 2001', 'GDP 2002', 'GDP 2003', 'GDP 2004', 'GDP 2005', 'GDP 2006', 'GDP 2007', 'GDP 2008', 'GDP 2009', 'GDP 2010', 'GDP 2011', 'GDP 2012', 'GDP 2013', 'GDP 2014', 'GDP 2015', 'GDP 2016', 'GDP 2017', 'GDP 2018', 'GDP 2019'],
                          var_name= 'GDP')
sns.boxplot(x="States", y="value", data= df_GDPboxstates)
plt.xlabel('States')
plt.ylabel('GDP')
plt.title('GDP from 1997 to 2019')
plt.xticks(rotation =70)
plt.show()

#seaborn boxplot unemployment per states
df2= df2.sort_values(by=['unemployment average'])
df_unemplboxstates = pd.melt(df2,id_vars= ['States'], value_vars= df2.iloc[:, 1:], var_name= 'unemploment')
sns.boxplot(x="States", y="value", data= df_unemplboxstates)
plt.xlabel('States')
plt.ylabel('Unemployment rate')
plt.title('Unemployment rate from 1980 to 2018')
plt.xticks(rotation =70)
plt.show()

# highschool education
df4["Percantage highschool graduates"] = df4["highschool average"] / df7["2014 Population"]

# Most Highschool Grads
highschool = df4.nlargest(5, ['Percantage highschool graduates'])
print(highschool)
x = list(highschool["States"])
y = list(highschool["Percantage highschool graduates"])
plt.bar(x, y, color="green")
plt.title('States with the most Highschool Graduates 2010 to 2018')
plt.xlabel('States')
plt.ylabel('High school graduates in %')
plt.grid(False)
plt.show()

# what are they voting for
df_votes1 = df_votes.drop(
    ["1976 votes", "1980 votes", "1984 votes", "1988 votes", "1992 votes", "1996 votes", "2000 votes", "2004 votes",
     "2008 votes", "2012 votes", "2016 votes"], axis=1)
print(df_votes1)
highschool_voting = df_votes1[df_votes1.States.isin(highschool.States)]
print(highschool_voting)

# least highschoolgrads
highschools = df4.nsmallest(5, ['Percantage highschool graduates'])
print(highschools)
x = list(highschools["States"])
y = list(highschools["Percantage highschool graduates"])
plt.bar(x, y, color="red")
plt.title('States with the least Highschool Graduates 2010 to 2018')
plt.xlabel('States')
plt.ylabel('Average High school graduates in %')
plt.grid(False)
plt.show()

# what are they voting for
highschools_voting = df_votes1[df_votes1.States.isin(highschools.States)]
print(highschools_voting)

# bachelor degree
df5["Percantage Bachelor graduates"] = df5["bachelor average"] / df7["2014 Population"]

# most bachelor degrees
bachelor = df5.nlargest(5, ['Percantage Bachelor graduates'])
print(bachelor)
x = list(bachelor["States"])
y = list(bachelor["Percantage Bachelor graduates"])
plt.bar(x, y, color="green")
plt.title('States with the most Bachelor Graduates 2010 to 2018')
plt.xlabel('States')
plt.ylabel('Average Bachelor graduates in %')
plt.grid(False)
plt.show()

# what are they voting for
bachelor_voting = df_votes1[df_votes1.States.isin(bachelor.States)]
print(bachelor_voting)

#least bachelor degrees
bachelors = df5.nsmallest(5, ['Percantage Bachelor graduates'])
print(bachelors)
x = list(bachelors["States"])
y = list(bachelors["Percantage Bachelor graduates"])
plt.bar(x, y, color="red")
plt.title('States with the least Bachelor Graduates 2010 to 2018')
plt.xlabel('States')
plt.ylabel('Average Bachelor graduates in %')
plt.grid(False)
plt.show()

# what are they voting for
bachelors_voting = df_votes1[df_votes1.States.isin(bachelor.States)]
print(bachelors_voting)

# degree
df6["Percantage Graduates"] = df6["graduate average"] / df7["2014 Population"]

#most degrees
graduate = df6.nlargest(5, ['Percantage Graduates'])
print(graduate)
x = list(graduate["States"])
y = list(graduate["Percantage Graduates"])
plt.bar(x, y, color="green")
plt.title('States with most Graduates 2010 to 2018')
plt.xlabel('States')
plt.ylabel('Average Graduates in %')
plt.grid(False)
plt.show()

# what are they voting for
graduate_voting = df_votes1[df_votes1.States.isin(graduate.States)]
print(graduate_voting)

# least degree
graduates = df6.nsmallest(5, ['Percantage Graduates'])
print(graduates)
x = list(graduates["States"])
y = list(graduates["Percantage Graduates"])
plt.bar(x, y, color="red")
plt.title('States with least Graduates 2010 to 2018')
plt.xlabel('States')
plt.ylabel('Average Graduates in %')
plt.grid(False)
plt.show()

# what are they voting for
graduates_voting = df_votes1[df_votes1.States.isin(graduates.States)]
print(graduates_voting)

# Top insured
topinsured = df_health.nlargest(5, ['insured average'])
print(topinsured)
x = list(topinsured["States"])
y = list(topinsured['insured average'])
plt.bar(x, y, color="green")
plt.title('States with the most Insured 2008 to 2019')
plt.xlabel('States')
plt.ylabel('Average Insured in %')
plt.grid(False)
plt.show()

#what are they voting for
topinsured_voting = df_votes1[df_votes1.States.isin(topinsured.States)]
print(topinsured_voting)

# Top income
topincome = df3.nlargest(5, ['income average'])
print(topincome)
x = list(topincome["States"])
y = list(topincome['income average'])
plt.bar(x, y, color="green")
plt.title('States with the highest Income 2014 to 2018')
plt.xlabel('States')
plt.ylabel('Average Income in %')
plt.grid(False)
plt.show()
topincome_voting = df_votes1[df_votes1.States.isin(topincome.States)]
print(topincome_voting)

# GDP
df["Difference"] = df["GDP 2019"] - df["GDP 1997"]
print(df)
topdifference_gdp = df.nlargest(5, ['Difference'])
print(topdifference_gdp)
topdifference_gdp_voting = df_votes1[df_votes1.States.isin(topdifference_gdp.States)]
print(topdifference_gdp_voting)
topgdp = df.nlargest(5, ['GDP average'])
print(topgdp)
topgdp_voting = df_votes1[df_votes1.States.isin(topgdp.States)]
print(topgdp_voting)

# Rape
toprape = df_rape_legacy.nlargest(5, ['rape average'])
print(toprape)
toprape_voting = df_votes1[df_votes1.States.isin(toprape.States)]
print(toprape_voting)
df_rape_legacy= df_rape_legacy.sort_values(by=['rape average'])
df_rape_legacy = pd.melt(df2,id_vars= ['States'], value_vars= df2.iloc[:, 1:], var_name= 'rape')
sns.boxplot(x="States", y="value", data= df_rape_legacy)
plt.xlabel('States')
plt.ylabel('Rape Cases')
plt.title('Rape Cases in the different States')
plt.xticks(rotation =70)
plt.show()


#Votes first 25 states
labels = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri']
democrat = [1, 0, 1, 3, 7, 4, 7, 8, 4, 3, 10, 0, 7, 1, 6, 0, 3, 3, 7, 9, 9, 6, 11, 1, 3]
republican = [10, 11, 10, 8, 4, 7, 4, 3, 7, 8, 1, 11, 4, 10, 5, 11, 8, 8, 4, 2, 2, 5, 0, 10, 8]
width = 0.35
fig, ax = plt.subplots()
ax.bar(labels, democrat, width, label = 'Democrats')
ax.bar(labels, republican, width, label = 'Republican')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of votes from 1976 to 2016')
plt.xticks(rotation=45)
ax.legend()
plt.show()

#Votes second half
x_labels = ['Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio', 'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia', 'Wisconsin', 'Wyoming']
democrat_2 = [1, 0, 5, 6, 7, 6, 10, 2, 0, 5, 0,8, 7, 10, 1, 0, 3, 1, 0, 7, 3, 8, 5, 8, 0]
republican_2 = [10, 11, 6, 5, 4, 5, 1, 9, 11, 6, 11, 3, 4, 1, 10, 11, 8, 10, 11, 4, 8, 3, 6, 3, 11]
width = 0.35
fig, ax = plt.subplots()
ax.bar(labels, democrat, width, label = 'Democrats')
ax.bar(labels, republican, width, label = 'Republican')
ax.set_ylabel('Frequency')
ax.set_title('Distribution of votes from 1976 to 2016')
plt.xticks(rotation=45)
ax.legend()
plt.show()
