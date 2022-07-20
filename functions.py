#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#This file contains the functions that we commonly use


# In[ ]:


import pandas as pd
import numpy as np
from scipy import interpolate
import requests
import json


# In[1]:


def convert_to_export_list(code_list1):
    """This function created a new list from code List1 wherein we drop all rows that donot have string with Export."""
    export_code_list2=[]
    for i in range(len(code_list1)):
        if type(code_list1[i]) == str:
            if code_list1[i][0:6].upper() == "EXPORT":
                a = code_list1[i][0:6].strip()
                b = code_list1[i][6:].strip()
                export_code_list2.append(a.upper()+b)
            else:
                export_code_list2.append(' ')
        else:
            export_code_list2.append(" ")
    return export_code_list2


# In[2]:


def curr_to_sql_query(curr_list):
    """Functions creates a string that is required to be passed to select currency pairs to be selected in the sql query"""
    newvalue=''
    for i in range(len(curr_list)):
        if i < len(curr_list)-1:
            newvalue = newvalue+ "`currency` = " + "'"+curr_list[i] +"'"+" OR "

        else:
            newvalue = newvalue+ "`currency` = " + "'"+curr_list[i] +"'"
     
    return  newvalue   


# In[3]:


def interpolated_forward(exposure):
    """function to generate a list of interploated forwards. 
    NOTE: MATURITY DATE HAS TO BE WITHIN A YEAR"""
    # generating a list of premium, days and maturity for interpolation
    Premium =[] 
    Day = []
    Maturity = []

    for index, rows in exposure.iterrows(): 
        Premium.append([rows.m0,rows.m1,rows.m2,rows.m3,rows.m4,rows.m5,rows.m6,rows.m7,rows.m8,
                  rows.m9,rows.m10,rows.m11,rows.m12,rows.m24])
        print(([rows.m0,rows.m1,rows.m2,rows.m3,rows.m4,rows.m5,rows.m6,rows.m7,rows.m8,
                  rows.m9,rows.m10,rows.m11,rows.m12,rows.m24]))

        Day.append([rows.Start, rows.Start+30,rows.Start+60,rows.Start+90,
                  rows.Start+120,rows.Start+150,rows.Start+180,rows.Start+210,rows.Start+240,
                  rows.Start+270,rows.Start+300,rows.Start+330,rows.Start+360,rows.Start+720])

        Maturity.append([rows.Target])
    #interpolating based on the lists generated above and saving interpolation forwards to the data list    
    data = []
    for i in range(len(Maturity)):
        f = interpolate.interp1d(Day[i],Premium[i], fill_value = 'extrapolate')
        print(Premium[i])
        print(f(Maturity[i])[0])
        data.append(f(Maturity[i])[0])
    return data


# In[4]:


def start_target(df):
    """Function to Calculate Number of Days for Interpolation Purpose"""
    if df.empty == False:
        
        df["Start"] = (df['Start Date']-min(df['Start Date'])) / np.timedelta64(1, "D")
        df['Target'] = (df['End Date']-min(df['Start Date'])) / np.timedelta64(1,'D')
        
    else:
        df["Start"]= 0
        df["Target"] = 0
        
    return df


# In[ ]:
def get_token():
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    data = {"username": "tickerplant","password": "gbfx.703"}	
    r = requests.post("http://api.greenbackforex.com/user/auth", data=json.dumps(data), headers=headers)
    token = r.json()
    t= token["tokenValue"]
    return t


def option_price(t, spot, strike, expiry_dt, notional,opt_type):
    headers = {'Content-type': 'application/json', 'Accept': 'application/json'}
    my_inputs = {    
        "Token": t,
        "SpotRate": spot,
        "StrikePrice": strike,
        "ExpiryDate": expiry_dt,
        "Notional": notional,
        "RequestType": opt_type
    }
    r = requests.post("http://api.greenbackforex.com/user/getData", data=json.dumps(my_inputs), headers=headers)
    output = r.json()
    return output


# %%