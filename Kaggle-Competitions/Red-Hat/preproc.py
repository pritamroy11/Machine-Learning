# -*- coding: utf-8 -*-
"""
Created on Thu Aug 04 11:20:20 2016

@author: JSULLIVAN
"""

# Pre-processing the data 

import pandas as pd 


act_train = 'act_train.csv'     # Activity test file
act_test = 'act_test.csv'
people = 'people.csv'           # People file


# Function to read in the files to pandas dataframe
def read_file(act_train):
    df = pd.read_csv(act_train)
    return df 
        
df_act_train = read_file(act_train)   # Activities training set dataframe
df_act_test = read_file(act_test)
df_p = read_file(people)        # People dataframe

# Function to preprocess the activity files
def preproc_act(df):
    
    # Dropping the date column and activity_id
    df = df.drop(['date', 'activity_id'], axis = 1)   # axis=1 b/c this applies to a colummn label;  axis=0 applies to row
    
    # Filling in the empty cells with dummy type 'type 0'    
    columns = list(df)    
    for col in columns[0:12]:
        df[col] = df[col].fillna('type 0')
        
    # Changing categorical variables to integers 
    for col in columns[0:12]:
        df[col] = df[col].astype('category')
    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

    # Renaming the columns to distinguish activity characteristics from people characteristics
    for col in columns[2:12]:
        df = df.rename(columns = {col:'act_'+col})
    return df 


# Function to preprocess the people data    
def people_preproc(df):
        
    # Dropping the date column
    df = df.drop('date', axis = 1)   # axis=1 b/c this applies to a colummn label;  axis=0 applies to row
        
    # Changing categorical variables to integers 
    columns = list(df)
    for col in columns[0:11]:
        df[col] = df[col].astype('category')
    cat_columns = df.select_dtypes(['category']).columns
    df[cat_columns] = df[cat_columns].apply(lambda x: x.cat.codes)

    # Changing booleans to integers 
    for col in columns[11:39]:
        df[col] = df[col].astype(int)

    return df     

act_train_preproc = preproc_act(df_act_train)
act_test_preproc = preproc_act(df_act_test)
people_preproc = people_preproc(df_p)


# Merging the activity and people data 

def join_data(df1, df2):
    merged = df1.merge(df2, how = 'left', on = 'people_id')
    return merged 
    
train_merged = join_data(act_train_preproc, people_preproc)
test_merged = join_data(act_test_preproc, people_preproc)


# Writing the preprocessed data to csv files
train_merged.to_csv('train_preproc.csv')
test_merged.to_csv('test_preproc.csv')
