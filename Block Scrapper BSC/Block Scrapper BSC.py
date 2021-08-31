# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 19:32:50 2021

@author: Noah Verner & @felipesalda
"""

import re
import pandas as pd
from selenium import webdriver
import numpy as np
#import date library to know how much takes this program takes for analyzing an specific interval of blocks
from datetime import datetime
initial_time = datetime.now()

#set webdriver
options = webdriver.ChromeOptions()
#open driver without UI for automated testing
options.add_argument('--headless')
#set the location of driver executable path and enable options for the driver
driver = webdriver.Chrome(executable_path='C:/Users/ResetStoreX/AppData/Local/Programs/Python/Python39/Scripts/chromedriver.exe', options=options)
#make the driver wait up to 10 seconds before doing anything
driver.implicitly_wait(10)

#parameters for the scrapping
#values for the example
#Declaring a variable for looping over all the blocks
blocks = np.arange(10479311, 10479314, 1)
minimun_value_txn = 1.95
to_chain = 'PancakeSwap: Router v2'
BNB = 'BNB'
#set a final dataframe which will contain all the desired data from the arange that matches with the parameters set
df_final = pd.DataFrame()

#set a loop for each block from the arange.
for block in blocks:
    #INITIAL SEARCH
    #look for general data of the link
    #amount of results and pages for the execution of the for loop, "block" variable is used within the {} 
    url = 'https://bscscan.com/txs?block={}&p=1'.format(block)
    print(f'Bloque actual: {block}')
    driver.get(url)
    #Here we order the scrapper to try finding the total number of pages for a block if such element that contains it exists
    #if so, the scrapper will proceed to execute the rest of the procedure
    try:
        pages =  driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_topPageDiv"]/nav/ul/li[3]/span').text
        pages = int(re.search(r'\d{0,3}$', pages).group())
        
        #FOR LOOP
        #search at each page all the values we are looking for
        #following conditions like number of the block, minimun value of the txn and the destiny
        
        df = pd.DataFrame()
        df2 = pd.DataFrame()
        
        
        print(df)
        print(df2)
        
        
        #set a sub loop for each row from the table of each page of each block
        for page in range(1,pages+1):
        
            url = 'https://bscscan.com/txs?block={}&p={}'.format(block,page)
            driver.get(url)
            txn_found = int(driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_topPageDiv"]/p/span').text.replace('A total of ','').replace(' transactions found','').replace(',',''))
            txn_found_last=txn_found%50
            
            print(f'Página: {page} de {pages}')
        
            if page < pages:
                for txn in range(1,50+1):
                    txn_hash = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[2]'.format(txn)).text)
                    block_num = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[4]'.format(txn)).text)
                    to_destiny = driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[9]'.format(txn)).text
                    value_txn = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[10]'.format(txn)).text)
                    if BNB in value_txn:
                        value_txn = float(value_txn.replace(' BNB','').replace(',',''))
                        if value_txn >= minimun_value_txn and to_chain in to_destiny:
                            row_data = [txn_hash, block_num, value_txn]
                            df_data = pd.DataFrame([row_data], columns = ['Transaction Id', 'Block No', 'BNB Value'])                        
                            df = df.append(df_data, ignore_index = True)
                            print(df)
                    else:
                        value_txn = 0            
                        if value_txn >= minimun_value_txn and to_chain in to_destiny:
                            row_data = [txn_hash, block_num, value_txn]
                            df_data = pd.DataFrame([row_data], columns = ['Transaction Id', 'Block No', 'BNB Value'])
                            df = df.append(df_data, ignore_index = True)
                            print(df)                                                                 
            else:
                for txn in range(1,txn_found_last+1):
                    txn_hash = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[2]'.format(txn)).text)
                    block_num = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[4]'.format(txn)).text)
                    to_destiny = driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[9]'.format(txn)).text
                    value_txn = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[10]'.format(txn)).text)
                    if BNB in value_txn:
                        value_txn = float(value_txn.replace(' BNB','').replace(',',''))
                        if value_txn >= minimun_value_txn and to_chain in to_destiny:
                            row_data2 = [txn_hash, block_num, value_txn]
                            df_data2 = pd.DataFrame([row_data2], columns = ['Transaction Id', 'Block No', 'BNB Value'])
                            df2  = df2.append(df_data2, ignore_index = True)
                            print(df2)
                            df = df.append(df2, ignore_index = True)
                    else:
                        value_txn = 0                      
                        if value_txn >= minimun_value_txn and to_chain in to_destiny:
                            row_data2 = [txn_hash, block_num, value_txn]
                            df_data2 = pd.DataFrame([row_data2], columns = ['Transaction Id', 'Block No', 'BNB Value'])
                            df2  = df2.append(df_data2, ignore_index = True)
                            print(df2)
                            df = df.append(df2, ignore_index = True)
                            
        #delete every single duplicated row in the df for then adding it to the the final dataframe                
        df.drop_duplicates(subset='Transaction Id', keep='first', inplace= True)
        df_final = df_final.append(df, ignore_index = True)
    #if such element doesn't exist, then the scrapper will print an statement informing it, for then proceeding to repeat the previous process with the next block.
    except:
        print(f'El Bloque No. {block} NO CONTIENE UN CARAJO ¯\_₍⸍⸌̣ʷ̣̫⸍̣⸌₎_/¯, ¡SIGUIENTE! ')

#export results to one single csv file
df_final.to_csv('Block_10479311_to_10479313_1point95_BNB_PANCAKESWAPV2_without_duplicates_NOR_EMPTY_BLOCK_10479312.csv')
print(df_final)
driver.quit()

#set 2 variables to know how much time has passed since this program was run
final_time = datetime.now()
time_elapsed = final_time - initial_time

#print the time elapsed
print(f'Búsqueda finalizada ₍⸍⸌̣ʷ̣̫⸍̣⸌₎, Tiempo de Ejecución: {time_elapsed}')
