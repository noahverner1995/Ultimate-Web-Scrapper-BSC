# -*- coding: utf-8 -*-
"""
Created on Thu Aug  5 15:33:42 2021

@author: Noah Verner
"""
from bs4 import BeautifulSoup
import requests
import pandas as pd
import numpy as np
from time import sleep
from random import randint

pd.set_option('display.max_columns', None) 

#Declaring a variable for looping over all the pages
pages = np.arange(1, 101, 1)

a = pd.DataFrame()
#loop cycle

for url in pages:      

    #get html for each new page
    url ='https://bscscan.com/accounts/'+str(url)+'?ps=100'
    page = requests.get(url)
    sleep(randint(3,10))
    soup = BeautifulSoup(page.text, 'lxml')
    
    #get the table
    table = soup.find('table', {'class':'table table-hover'})
    headers = []
    
    #get the headers of the table and delete the "white space"
    for i in table.find_all('th'):
        title = i.text.strip()
        headers.append(title)
    
    #set the headers to columns in a new dataframe 
    df = pd.DataFrame(columns=headers)
    
    #get the rows of the table but omit the first row (which are headers)
    for row in table.find_all('tr')[1:]:
        data = row.find_all('td')
        row_data = [td.text.strip() for td in data]  
        length = len(df)
        df.loc[length] = row_data 
    
    #set the data of the Txn Count column to float
    Txn = df['Txn Count'].values
    for e in range(len(Txn)):
      myVal = Txn[e].replace(",", "")
      Txn[e] = float(myVal)
    
    #combine all the data rows in one single dataframe
    a = a.append(pd.DataFrame(df))  
    
    def tester(mejora):
        mejora = mejora[(mejora['Txn Count']>200.0) & (mejora['Txn Count']<1000.0)] 
        return mejora.to_csv('new_100pages_test_Txn_Count.csv') 
    
    tester(a)
    
#print the variable type of each header and  
#print rows from the last page that matches an specific condition set upon the data of their Txn Count
print(df.dtypes)
print(df[(df['Txn Count']>200.0) & (df['Txn Count']<1000.0)])
