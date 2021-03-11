import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

#Sociological Metrics
data_sm=pd.read_csv('Sociological_metrics.csv')
print(data_sm)

#Without Health Insurance
data_wh=pd.read_excel('without_health_2013_2016.xls',sheet_name='Table 6',usecols='A,C,E,G,I', skiprows=12,skipfooter=12)
data_wh.columns=['States','2013 Uninsured','2014 Uninsured','2015 Uninsured','2016 Uninsured']
data_whw=data_wh.dropna()
print(data_whw)
data_wh_describe=data_whw.mean(axis=1)
print(data_wh_describe)

#Health Insurance
data_hi=pd.read_excel('Health Insur_State_2008 to 2019.xlsx',sheet_name='hic04_acs',usecols='A,B,E,I,M,Q,U,Y,AC,AG,AK,AO,AS,AW', skiprows=16,skipfooter=4)
data_hi.columns=['States','Coverage','2019 Insured','2018 Insured','2017 Insured','2016 Insured', '2015 Insured', '2014 Insured','2013 Insured','2012 Insured','2011 Insured','2010 Insured','2009 Insured','2008 Insured']
data_hil=data_hi[data_hi['Coverage']=='Any coverage']
print(data_hil)
data_hi_describe=data_hil.mean(axis=1)
print(data_hi_describe)

#Data Votes
data_dv=pd.read_csv('DataVotes 1976-2016.csv',usecols=[0,1,8,10])
res = data_dv.pivot_table(index=['state','party'], columns='year',
                     values='candidatevotes').reset_index()
value_list=['democrat','republican']
ress=res[res.party.isin(value_list)]
print(ress)