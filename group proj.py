# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import sqlite3
import pandas as pd
import seaborn as sns

#cnx = sqlite3.connect('FPA_FOD_20170508.sqlite')
cnx = sqlite3.connect('FPA_FOD_20170508.sqlite')

emissions = pd.read_excel('emmissions.xlsx',header=4)

df = pd.read_sql_query("SELECT FIRE_YEAR,STAT_CAUSE_DESCR,LATITUDE,LONGITUDE,STATE,DISCOVERY_DATE,FIRE_SIZE FROM 'Fires'", cnx)

#df = df[df['FIRE_SIZE'] > .2]

by_state = df.groupby('STATE').mean()

"""
sns.set()
sns.relplot(x="FIRE_YEAR",y="FIRE_SIZE", hue = "STATE", data=by_state.reset_index())
"""

# Source: https://gist.github.com/rogerallen/1583593
us_state_abbrev = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


emissions = emissions.dropna()

emissions = emissions.replace({"State": us_state_abbrev})

emissions_transposed = emissions.T

emissions_transposed.columns = emissions_transposed.iloc[0]

emissions_transposed = emissions_transposed.drop("State")

merged = pd.concat([df, emissions], axis=1, sort= False)


epoch = pd.to_datetime(0, unit='s').to_julian_date()

pd.to_datetime(df.DISCOVERY_DATE - epoch, unit='D')

melted_df = pd.melt(emissions, id_vars=["State"], 
                  var_name="Year", value_name="CO2")

df = df.rename(index=str, columns={"FIRE_YEAR": "Year"})

melted_df = melted_df.rename(index=str, columns={"State": "STATE"})

melted_df = melted_df[melted_df.STATE != 'Total of states (unadjusted)¹']

melted_df = melted_df[melted_df.STATE != 'United States']

melted_df = melted_df[melted_df.Year != 'Percent']

melted_df = melted_df[melted_df.Year != 'Absolute']

california = melted_df[melted_df.STATE == 'CA']


