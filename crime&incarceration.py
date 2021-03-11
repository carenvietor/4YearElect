import pandas as pd  # data processing
from pathlib import Path
from functools import partial

filename = "crime_and_incarceration_by_state.csv"
df = pd.read_csv(filename, sep=",")

# def test(col, x):
# if col.isdigit():
# return x + col
# else:
# return col

# only violent crime total per year per state
def crime():
    df_crime_total = pd.read_csv(filename, sep=",", usecols=[0, 2, 7])
    df_crime_total.drop(df_crime_total[df_crime_total["jurisdiction"] == "FEDERAL"].index, inplace=True)
    df_crime_total = df_crime_total.pivot_table(index=['jurisdiction'], columns='year',
                                                values='violent_crime_total').reset_index()
    df_crime_total["total crime average"] = df_crime_total.iloc[:, 2:].mean(axis=1)
    return df_crime_total

# only murder manslaughter per year per state
def murder():
    df_murder_manslaughter = pd.read_csv(filename, sep=",", usecols=[0, 2, 8])
    df_murder_manslaughter.drop(df_murder_manslaughter[df_murder_manslaughter["jurisdiction"] == "FEDERAL"].index,
                                inplace=True)
    df_murder_manslaughter = df_murder_manslaughter.pivot_table(index=['jurisdiction'], columns='year',
                                                                values='murder_manslaughter').reset_index()
    df_murder_manslaughter["murder manslaughter average"] = df_murder_manslaughter.iloc[:, 2:].mean(axis=1)
    return df_murder_manslaughter

# only robbery per year per state
def robbery():
    df_robbery = pd.read_csv(filename, sep=",", usecols=[0, 2, 11])
    df_robbery.drop(df_robbery[df_robbery["jurisdiction"] == "FEDERAL"].index, inplace=True)
    df_robbery = df_robbery.pivot_table(index=['jurisdiction'], columns='year', values='robbery').reset_index()
    df_robbery["robbery average"] = df_robbery.iloc[:, 2:].mean(axis=1)
    return df_robbery

# only Rape per State per year
def rape():
    df_rape_legacy = pd.read_csv(filename, sep=",", usecols=[0, 2, 9])
    df_rape_legacy.drop(df_rape_legacy[df_rape_legacy["jurisdiction"] == "FEDERAL"].index, inplace=True)
    df_rape_legacy = df_rape_legacy.pivot_table(index=['jurisdiction'], columns='year',
                                                values='rape_legacy').reset_index()
    df_rape_legacy["rape average"] = df_rape_legacy.iloc[:, 2:].mean(axis=1)
    # df_rape_legacy.rename(mapper=partial(test, x="Rape "), axis="columns")
    return df_rape_legacy

# print everything
if __name__ == '__main__':
    df_rape_legacy = rape()
    print(df_rape_legacy)
    df_robbery = robbery()
    print(df_robbery)
    df_murder_manslaughter = murder()
    print(df_murder_manslaughter)
    df_crime_total = crime()
    print(df_crime_total)
