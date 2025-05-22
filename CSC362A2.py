# -*- coding: utf-8 -*-
"""
CSC 362. Owen Manley. Assignment #2
This assignment goes over a video from Gina Sprint introducing 
data preparation/cleaning with NumPy/Pandas.

Overall, I was introduced to many functions regarding numpy/pandas and 
somewhat understand its usage. I think I'll need more practice; also, I have a 
resource to fall back on if I ever have trouble (that being the Youtube 
video and this program).
"""
import numpy as np 
import pandas as pd

#LOAD DATA  
df = pd.read_csv("pd_hoa_dataset.csv", header=0)
print(df.shape)

#EXPLORE DATA
print(df.head(5))
print(df.tail(5))

print("Number of participants:", df.shape[0] //9)
print(df.iloc[660:670, :])

#MISSING DATA
print(df["duration"].value_counts()["?"])
#Ways to handle missing values...
#1. Discard them.
#Never want to throw away data.
#2. Fill the missing values.
#Fill w/most frequent label
#Fill w/central tendency measure (mean, median, mode).
#3. Do nothing with them and handle case by case later.

#Replace the "?" with np.NaN
#"Inplace" modify the dataframe in place of memory.
#If inplace weren't there, there would need to be an assignment to overwrite dataframe with return copy.
df.replace("?", np.NaN, inplace=True)
#isnull returns a boolean array designating if a value is null or not.
#Sum is a method that returns the sum of all True column-wise.
print(df.isnull().sum())

df.dropna(inplace=True)
print("AFTER DROPPING:", df.isnull().sum())
print(df.shape)
df.reset_index(inplace=True, drop=True) #Resets the index so there are no jumps in the datasets/logic errors in the future.
print(df.head(2))

#DECODE TASK
#Replace 1-8 and dot with more human readable/meaningful labels.

task_decoder = {"1": "Water Plants", "2": "Fill Medication Dispenser", 
                "3": "Wash Countertop", "4": "Sweep and Dust", 
                "5": "Cook", "6": "Wash Hands", "7": "Perform TUG", 
                "8": "Perform TUG w/Questions", "dot": "Day Out Task"}
def decode_task(df):
    ser = df["task"]
    for key in task_decoder:
        ser.replace(key, task_decoder[key], inplace=True)
decode_task(df)
print(df.head(10))

#CLEAN CLASS
def clean_class(df):
    ser = df["class"].copy()
    for i in range(len(ser)):
        curr_class = str(ser.iloc[i])
        curr_class = curr_class.lower()
        if "hoa" in curr_class or "healthy" in curr_class:
            ser.iloc[i] = "HOA"
        elif "pd" in curr_class or "parkinson" in curr_class:
            ser.iloc[i] = "PD"
        else:
            print("Unrecognized status: %d, %s" %(i, curr_class) )
    df["class"] = ser
clean_class(df)
print(df.head(25))
print(df["class"].value_counts())

#Check the types of all attributes to make sure that the data frame is storing 
#each attribute(column) in the most appropriate type.
#CHECK COLUMN TYPES
for column in df.columns:
    print(column, df[column].dtype) #Print columns and datatype of each column in data frame.
#Duration is stored as an object. Which is bad because it determines the amount of time it takes to do a task (int) and 
#there were mixed typed "?".
#print(df["duration"].mean()) #Didn't compute.
#print((df["duration"].sum())) #Also didn't compute. Durations values are supposedly stored as strings.
df["duration"] = df["duration"].astype(np.int32)
print((df["duration"].sum(), df["duration"].mean(), df["duration"].std()))
#Okay, I had to do the for loop again to essentially "update" the types of each column.
#For some reason, I would run it and "duration" would still be "object". 
for column in df.columns:
    print(column, df[column].dtype)
    
# WRITE OUT THE CLEANED DATA
df.to_csv("pd_hoa_activities_cleaned.csv", index=False)
#Makes a new csv file of the new dataset.


        
    

