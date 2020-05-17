# Project 2 in Udacity Programing for Data Analysis
# Explore US Bikeshare Data
# Submitted by James Sturges
# ====================================================================================

import datetime as dt
import pandas as pd
import numpy as np
#from IPython.display import display
#pd.options.display.max_rows = 999
def cleanup(df):
    df.columns = [item.lower() for item in list(df.columns)]
    df.columns = df.columns.str.replace(r" ", "_")       #replace space in cols with underscore
    df.drop(df.columns[0], axis=1, inplace=True)               #get rid of first column
    df['start_time']=pd.to_datetime(df['start_time'])          #convert start time to datetime
    df['start_hour']=df['start_time'].dt.hour
    df['end_time']=pd.to_datetime(df['end_time'])              #convert end time to datetime
    df['end_hour']=df['end_time'].dt.hour
    df[['birth_year']] = df[['birth_year']].fillna(value=0)    #clean up nans in birth year
    df['birth_year']=df['birth_year'].astype('int')            #convert birth year to int
    df['day_of_week']=df['start_time'].dt.day_name().astype('str').str[:3] #+ col for day
    df['month']=df['start_time'].dt.month_name().astype('str').str[:3] #+ col for month
    
    return(df)

def city_input():
    print('==========================================================================')
    print('Please type the number corresponding to the city you would like to explore')
    print(' 1 - Chicago')
    print(' 2 - New York City')
    print(' 3 - Washington DC')
    print(' q - quit')
    print(' return key only for all city data')
    print('==========================================================================')
    print()
    city_num = input(' City Number? ')
    print()
    return(city_num.lower())

def stats_input():
    print('================================================================================')
    print('Please type the number corresponding to the statistics you would like to explore')
    print(' 1 - "Month" frequency distribution')
    print(' 2 - "Day of Week" frequency distribution')
    print(' 3 - "Top 5 Start Hours" frequency distribution')
    print(' 4 - "Top 5 End Hours" frequency distribution')
    print(' 5 - "Gender" frequency distribution')
    print(' 6 - "Top 5 Start stations" frequency distribution')
    print(' 7 - "Top 5 End stations" frequency distribution')
    print(' 8 - Trip Duration Statistics')
    print(' return key only for all stat data')
    print(' any other input:  quit stats')
    print('================================================================================')
    print()
    stats_num = input(' Stats Number? ')
    print()
    return(stats_num.lower())

def stats_response(df,stats_num):
    run_it_again=True
    if stats_num == '2':
        df=df.groupby(['city'])['day_of_week'].value_counts()
    if stats_num == '1':
        df=df.groupby(['city'])['month'].value_counts()
    if stats_num == '3':
        df=pd.DataFrame(df.groupby("city")["start_hour"].value_counts())   \
        .rename(columns={'start_hour': 'sh_count'}).reset_index()  \
        .sort_values(by=['city','sh_count'],ascending=[True,False]) \
        .groupby('city').head(5)
    if stats_num == '4':
        df=pd.DataFrame(df.groupby("city")["end_hour"].value_counts())   \
        .rename(columns={'end_hour': 'eh_count'}).reset_index()  \
        .sort_values(by=['city','eh_count'],ascending=[True,False]) \
        .groupby('city').head(5)      
    if stats_num == '5':
        df=df.groupby(['city'])['gender'].value_counts()
    if stats_num == '6':
        df=pd.DataFrame(df.groupby("city")["start_station"].value_counts())   \
        .rename(columns={'start_station': 'ss_count'}).reset_index()  \
        .sort_values(by=['city','ss_count'],ascending=[True,False]) \
        .groupby('city').head(5)
    if stats_num == '7':
        df=pd.DataFrame(df.groupby("city")["end_station"].value_counts())   \
        .rename(columns={'end_station': 'es_count'}).reset_index()  \
        .sort_values(by=['city','es_count'],ascending=[True,False]) \
        .groupby('city').head(5)
    if stats_num == '8':
        df=df.groupby('city')['trip_duration'].describe().reset_index()
    return(df,run_it_again)


# divide data by city selection process
def get_data(df):
    run_it_again=True
    if city_num=='1':
        df=df[df['city']=='chi']
    else:
        if city_num=='2':
            df=df[df['city']=='nyc']
        else:
            if city_num=='3':
                df=df[df['city']=='wdc']
            #else:
                #if city_num=='q':
                    #run_it_again=False           
    return(df,run_it_again)
#************ main prog *************

# *************** read in and cleanup data
df1=pd.read_csv('chicago.csv')
df1['city']='chi'
df2=pd.read_csv('new_york_city.csv')
df2['city']='nyc'
df3=pd.read_csv('washington.csv')
df3['city']='wdc'
df=pd.concat([df1,df2,df3],axis=0)
df=cleanup(df)

# *************** dictionary set up
city_response = {}
city_response['1']= df[df['city']=='chi']
city_response['2']= df[df['city']=='nyc']
city_response['3']= df[df['city']=='wdc']
city_response[''] = df

city_pair={
    "1" : "Chicago",
    "2" : "New York City",
    "3" : "Washington DC",
    "" : "all Cities"
    }
stats_pair={
    "1" : "Frequency by Month",
    "2" : "Frequency by Day of the Week",
    "3" : "Frequency by Top 5 Start Hours",
    "4" : "Frequency by Top 5 End Hours",
    "5" : "Frequency by Gender",
    "6" : "Top 5 Start stations",
    "7" : "Top 5 End stations",
    "8" : "Show Trip Duration Statistics",
    "" : "all Stats"
    }



# *************** Begin program loop
run_it_again=True

while run_it_again:
#*************** city input and limits in data
    stats_again=True
    city_input_needed=True
    while city_input_needed:
        city_num=city_input()
        if city_num in ['1','2','3','']:
            df4=city_response[city_num]
            raw_data=input('Would you like to see the top 5 and bottom 5 rows of the raw data (y for yes)?')
            if raw_data.lower()=="y":
                print(pd.concat([df.head(5),df.tail(5)]))
            city_input_needed=False    
        else:
            if city_num=='q':
                run_it_again=False
                stats_again=False
                city_input_needed=False
            else:
                print('###################################################')
                print('Input not in range (i.e. 1,2,3,q or return(for all), please re-enter' )
                print('###################################################')
                print()
                city_input_needed=True

#*************** stats input
    while stats_again:
        stats_num=stats_input()
        if stats_num in ['1','2','3','4','5','6','7','8']:
                    print('*********** '+city_pair[city_num]+' ***********')
                    print('*********** '+stats_pair[stats_num]+' ***********')
                    print(stats_response(df4,stats_num))
        else:
            if stats_num=='':
                for item in ['1','2','3','4','5','6','7','8']:
                    print('*********** '+city_pair[city_num]+' ***********')
                    print('*********** '+stats_pair[item]+' ***********')
                    print(stats_response(df4,item))
            else:
                stats_again=False
