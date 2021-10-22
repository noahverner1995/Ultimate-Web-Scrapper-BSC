# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 19:32:50 2021

@author: Noah Verner & @felipesalda
"""
#Initial Installs in case of deploying this program in a new virtual environment
#%%bash
#sudo apt-get update
#sudo apt-get install chromium-driver -y
#!pip install selenium==3.141.0
#!pip install webdriver_manager==3.4.2
import os
if os.name == 'nt': # Let's add some colors for the lulz
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
import re
import json
import random
import pandas as pd
from selenium import webdriver
import numpy as np
#import date library to know how much takes this program takes for analyzing an specific interval of blocks
from datetime import datetime
import time
#import selenium functions to make sure the program will wait enough time before getting some data from pages
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
initial_time = datetime.now()

#set webdriver
options = webdriver.ChromeOptions()
#open driver without UI for automated testing
options.add_argument('--headless')
#remove warning in console
options.add_argument("--log-level=3")
#set the location of driver executable path and enable options for the driver
driver = webdriver.Chrome(executable_path='C:/Users/ResetStoreX/AppData/Local/Programs/Python/Python39/Scripts/chromedriver.exe', options=options)
#Here we start to automate the big process down below
#First we set our counter (y) to 1
y = 1
#Now we set the amount of reruns (limite) to 6, this means this loop will run 5 times, because it starts in 1, not in 0
limite = 6
#Here's where the party begins
while y < limite:
    print(f'\u001b[45m Intento No. {y} de {limite-1} \033[0m')
    #make the driver wait up to 10 seconds before doing anything
    driver.implicitly_wait(10)  
    #parameters for the scrapping
    #values for the example
    #Declaring several variables for looping over all the blocks
    #Let's start scrapping automatically from the newest block
    link = 'https://bscscan.com/blocks'
    driver.get(link)
    #Here we use the Xpath element of the most recent block validated BscScan
    initial_block = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[1]/a').text)
    print(f'El bloque inicial para este proceso es el No. {initial_block}')   
    final_block = initial_block + 100
    #It seems that the current most recent validated block from bitquery explorer is delayed by around 57 blocks to BscScan, so for the blocks arange, initial_block element is incremented in 48
    blocks = np.arange(initial_block, final_block+1, 1)
    minimun_value_txn = 2.15
    maximum_value_txn = 16.2
    to_chain = 'PancakeSwap: Router v2'
    BNB = 'BNB'
    #set a final dataframe which will contain all the desired data from the arange that matches with the parameters set
    df_final = pd.DataFrame()
    dataframe_final = pd.DataFrame()
    #set another final dataframe which will contain the projects which are likely to pump soon (2ND PART OF THE PROCESS)
    initial_df = pd.DataFrame()
    #set a loop for each block from the arange.
    for block in blocks:
        #INITIAL SEARCH
        #look for general data of the link
        #amount of results and pages for the execution of the for loop, "block" variable is used within the {} 
        url = 'https://bscscan.com/txs?block={}&p=1'.format(block)
        print(f'\u001b[42m Bloque actual: {block} \033[0m '+'\u001b[42m Bloque Final: '+str(final_block)+'\033[0m '+'\u001b[42m Bloques Restantes: '+str(final_block-block)+'\033[0m '+'\u001b[45m Intento No. '+str(y)+' de '+str(limite-1)+'\033[0m'+'\n')
        driver.get(url)
        #Here we order the scrapper to try finding the total number of pages for a block if such element that contains it exists
        #if so, the scrapper will proceed to execute the rest of the procedure
        try:
            pages = driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_topPageDiv"]/nav/ul/li[3]/span').text
            print(f'Leyendo información sobre el número de páginas de este bloque ... {pages}')
            pages = int(re.search(r'\d{0,3}$', pages).group())
            print(f'Este bloque posee {pages} páginas en total')
            #FOR LOOP
            #search at each page all the values we are looking for
            #following conditions like number of the block, minimun value and maximum value of the txn and the destiny
            
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
                            if value_txn >= minimun_value_txn and value_txn < maximum_value_txn and to_chain in to_destiny:
                                row_data = [txn_hash, block_num, value_txn]
                                df_data = pd.DataFrame([row_data], columns = ['Transaction Id', 'Block No', 'BNB Value'])                        
                                df = df.append(df_data, ignore_index = True)
                                print(df)
                        else:
                            value_txn = 0            
                            if value_txn >= minimun_value_txn and value_txn < maximum_value_txn and to_chain in to_destiny:
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
                            if value_txn >= minimun_value_txn and value_txn < maximum_value_txn and to_chain in to_destiny:
                                row_data2 = [txn_hash, block_num, value_txn]
                                df_data2 = pd.DataFrame([row_data2], columns = ['Transaction Id', 'Block No', 'BNB Value'])
                                df2  = df2.append(df_data2, ignore_index = True)
                                print(df2)
                                df = df.append(df2, ignore_index = True)
                        else:
                            value_txn = 0                      
                            if value_txn >= minimun_value_txn and value_txn < maximum_value_txn and to_chain in to_destiny:
                                row_data2 = [txn_hash, block_num, value_txn]
                                df_data2 = pd.DataFrame([row_data2], columns = ['Transaction Id', 'Block No', 'BNB Value'])
                                df2  = df2.append(df_data2, ignore_index = True)
                                print(df2)
                                df = df.append(df2, ignore_index = True)
                                
            #delete every single duplicated row in the df for then adding it to the the final dataframe                
            df.drop_duplicates(subset='Transaction Id', keep='first', inplace= True)
            df.drop_duplicates(subset='BNB Value', keep='first', inplace= True)
            df_final = df_final.append(df, ignore_index = True)
        #if such element doesn't exist, then the scrapper will print an statement informing it, for then proceeding to repeat the previous process with the next block.
        except:
            print(f'El Bloque No. {block} NO CONTIENE UN CARAJO ¯\_₍⸍⸌̣ʷ̣̫⸍̣⸌₎_/¯, ¡SIGUIENTE! ')
    
    #delete every single duplicated row once again, then add this final df to another one
    #this is because a bot may appear asking swap a very large amount of BNB and its transaction fails because there's not enough liquidity, making it loop until it's done
    df_final.drop_duplicates(subset='BNB Value', keep='first', inplace= True)
    dataframe_final = dataframe_final.append(df_final, ignore_index = True)
    
    #Here's the second part of the process (filtering) <------------------------------------------------ IMPORTANT
    initial_df = initial_df.append(dataframe_final, ignore_index = True)
    filas_iniciales = len(initial_df)
    total_rows = len(initial_df)
    #Here we add some new columns that will contain some relevant data on the premium coins
    initial_df.insert(3,'Name Tag', None)
    initial_df.insert(4,'Contract Address', None)
    initial_df.insert(5,'Hodlers', None)
    initial_df.insert(6,'Transfers', None)
    initial_df.insert(7,'Age', None)
    initial_df.insert(8,'Date Taken', None)
    print('\n')
    print(f'Esta DataFrame tiene {total_rows} filas en total')
    print('\n')
    
    #here we set our beautiful counter to 0
    i=0
    #here we set the greatest final dataframe which will only contain good options to invest in
    dataframe_definitiva = pd.DataFrame()
    #let's do the fucking while loop bro    
    while i < (len(initial_df)):
        print(f'Analizando la fila #{i}')
        check = initial_df['Transaction Id'].iloc[i]
        print(f'Analizando la siguiente Id de transacción: {check}')
        print('\n')
        url = 'https://bscscan.com/tx/{}'.format(check)
        driver.get(url)
        time.sleep(3)
        #Here we check first if the Tx Id provided was a Success or a Failure, If Success, we continue with the process, else we delete the current row from the df and start again with the following one.
        #However, firstly we are going to set a new while loop to make sure that the status element is going to be located and readable when needed
        #But first, we set our counter (z) to 0
        z = 0
        while z < 10:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_maintable"]/div[2]/div[2]/span')))
                status = str(driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[2]/div[2]/span').text) 
                print(f'Esta transacción tiene un estado {status}')
                break        
            except:
                #Else, this bitch is going to sleep tight for 3 seconds for then repeating the loop until problem is no more!
                print(f'Intento: {z} - Joder, el estado de esta transacción aún no es visible (-_-"), lo intentaré de nuevo...')
                time.sleep(2.3)
                driver.refresh()
                time.sleep(5.2)
                z += 1
        if status != 'Success':
            print('Qué mal, esta transacción falló')
            tokens_transferred = 0
        else:
            tokens_transferred = int(driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[7]/div[1]/div/span[2]').text)
        #Also, We are going to make sure that the "Tokens Transferred" counter is less or equal to 5 and greater than 0
        if status == 'Success' and tokens_transferred <= 5 and tokens_transferred > 0:
            print(f'Esta transacción tiene un status: {status} y la siguiente cantidad de tokens transferidos: {tokens_transferred}')
            #get the list that contains every single token that was transferred in the current Tx Id
            token_list = driver.find_elements_by_xpath('/html/body/div[1]/main/div[3]/div[1]/div[2]/div[1]/div/div[7]/div[2]/ul/li/div/a')
            print(token_list)
            #get the total number of rows the list above has
            total_rows = len(token_list)
            #create a new df to store and read the data more easily
            df_token = pd.DataFrame()
            #extract the Name Tag and the Link from the contract address of every single token the list above has
            for token in token_list:    
                #we use a dictionary trick here because this was the only way this shit worked properly lol
                #the following regular expression " .rsplit('(', 1)[-1].rstrip(')') " is used to get only the ticket 'Name' that's inside the parenthesis ()
                datos = {'Name': token.text.rsplit('(', 1)[-1].rstrip(')'), 'Address': token.get_attribute("href").replace('https://bscscan.com/token/','')}
                print(datos)
                #then we append the data above to the df_token, while ignoring the index, fuck the index
                df_token = df_token.append(datos, ignore_index = True)                  
            print(df_token)
            #get the total number rows the df_token has
            total_rows = len(df_token)
            #here we start a while loop at the end of our df_token to read each token transferred til it finds our desired one.
            while total_rows > 0:
                print('\n')
                print('Analizando el token de la fila #'+str(total_rows-1)+':')
                #we need to save this information (Name Tag + Address) because it will be appended to the dataframe_definitiva
                Name = df_token['Name'].iloc[total_rows-1]
                Addresser = df_token['Address'].iloc[total_rows-1]
                print('Palabras de filtrado: "LPs" o "WBNB"')
                #we set these "LPs" and "WBNB" as words to avoid when reading df_token
                matches = ["LPs", "WBNB"]
                print(f'Este token se llama: {Name}')
                if any(x in Name for x in matches):
                    print('la fila #'+str(total_rows-1)+' contiene un token con nombre "LP" o "BNB", procedo a descartarla y a seguir con la siguiente.')
                    #if true, we substract 1 to continue the while loop in our df_token
                    total_rows -= 1
                else:
                    print('La fila #'+str(total_rows-1)+' contiene un token con nombre '+'"'+Name+'", '+'se ha encontrado el token deseado')
                    print(f'La dirección de contrato de este token es: {Addresser}')
                    print('\n')
                    print('A continuación se procede a verificar sí la anterior dirección de contrato inteligente está en "la lista negra" de contratos no deseados...')
                    #Now that we found our desired token, we check first if it exists in our lista_negra
                    #Here we CALL our black list of tokens which are not interesting to us
                    a_file = open("lista_negra.json", "r") #looks for the file in the current path of this script and enables it for reading
                    lista_negra = a_file.read() #converts the content of the file into a string
                    lista_negra = json.loads(lista_negra) #converts the content of the file into a dictionary
                    a_file.close() #close this variable because bEsT PrAcTiCEs
                    if Addresser in lista_negra.values():
                        print('\n')
                        print(f'Qué pena, este contrato "{Addresser}" está en la lista negra, por ende no nos interesa y se procede a borrar su Tx Id de la df')
                        initial_df = initial_df.drop(initial_df.index[i])
                        print(initial_df)
                        i +=1
                        break
                    else:
                        print('\n')
                        print(f'Bien, parece que este contrato "{Addresser}" NO ESTÁ en la lista negra de contratos no deseados, vamos a aplicar más filtros...')
                        url_2 = 'https://bscscan.com/token/{}'.format(Addresser)
                        driver.get(url_2)
                        print('\n')
                        print('Evaluando número de HODLERS...')
                        #In case our desired token doesn't exist in our lista_negra, we check now its current amount of hodlers
                        #Again, firstly we are going to set a new while loop to make sure that the No. of Hodlers element is going to be located and readable when needed
                        #But first, we set our counter (z) to 0
                        z = 0
                        while z < 10:
                            try:
                                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div')))                        
                                Hodlers = int(driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div').text.replace(',','').replace(' ','').replace('addresses',''))
                                print(f'Este contrato tiene posee esta cantidad de hodlers: {Hodlers}')
                                break
                            except:
                                #Else, this bitch is going to sleep tight for 3 seconds for then repeating the loop until problem is no more!
                                print(f'Intento: {z} - Joder, el número de hodlers de esta dirección aún no es visible (-_-"), lo intentaré de nuevo...')
                                time.sleep(3.5)
                                driver.refresh()
                                time.sleep(4.7)
                                z += 1
                        if Hodlers >= 5600 and Hodlers < 20000:
                            print('\n')
                            print('Dado que esta criptomoneda pasa este filtro de los HODLERS, procederemos a aplicar otro filtro')
                            Transfers = driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[4]/div/div[2]/span').text.replace(',','')
                            while Transfers == '-':
                                Transfers = driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[4]/div/div[2]/span').text.replace(',','')
                                if Transfers != '-':
                                    Transfers = int(Transfers)
                                    break
                            print(f'Se han realizado hasta el momento un total de {Transfers} transferencias dentro de este contrato inteligente')
                            #Assuming the amount of hodlers is greater than 3000 and less than 20000, we now check its number of transfers
                            if int(Transfers) >= 3*Hodlers:
                                print('Estupendo, esta criptomoneda cumple con el filtro de las transferencias, procederemos a aplicar un último filtro')
                                url_3 = 'https://explorer.bitquery.io/bsc/token/{}'.format(Addresser)
                                driver.get(url_3)
                                print('\n')
                                print('Evaluando la edad de esta criptomoneda...')
                                time.sleep(4)
                                #Right below, we are going to set a new while loop to make sure that the contract_age element is going to be located and readable when needed
                                #But first, we set our counter (x) to 0
                                x = 0
                                while x < 10:
                                    try:
                                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr[9]/td[2]/span')))
                                        contract_age = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr[9]/td[2]/span').text
                                        #If contract_age element is located and read, Bingo, problem is no more!
                                        print(f'Esta criptomoneda tiene {contract_age} días de edad')
                                        break
                                    except:
                                        #Else, this bitch is going to sleep tight for 3 seconds for then repeating the loop until problem is no more!
                                        print(f'Intento: {x} - Joder, no encontré este elemento en el tiempo deseado (-_-), lo intentaré de nuevo...')                                        
                                        time.sleep(3)
                                        driver.refresh()
                                        time.sleep(5)
                                        x += 1                                     
                                #Assuming the number of transfers is at least 2 times the number of hodlers, we now check how old is our desired token (in days)
                                if int(contract_age) < 26:
                                    print('Excelente, esta criptomoneda ha pasado todos los filtros, se procede a añadir información de su NameTag, Contract Address, Hodlers, Transfers, y Age a la nueva DataFrame junto con la fecha y hora en la que se tomó esta información')
                                    print(initial_df)
                                    #Now that our desired token has met all of our requirements, we are going to append its data to our dataframe_definitiva, including the current date and time at the moment this part is being executed
                                    hora_actual = time.ctime()
                                    initial_df.loc[initial_df.index[i], 'Name Tag'] = [Name]
                                    initial_df.loc[initial_df.index[i], 'Contract Address'] = [Addresser]
                                    initial_df.loc[initial_df.index[i], 'Hodlers'] = [Hodlers]
                                    initial_df.loc[initial_df.index[i], 'Transfers'] = [Transfers]
                                    initial_df.loc[initial_df.index[i], 'Age'] = [str(contract_age)+" days"]
                                    initial_df.loc[initial_df.index[i], 'Date Taken'] = [hora_actual]
                                    lista_negra[Name] = Addresser #updates the dictionary (variable) by adding the Ticket (Key) and Contract Address (Value) of the new cryptocurrency found 
                                    jsonFile = open("lista_negra.json", "w+") #looks for the file in the current path of this script and enables it for update
                                    json.dump(lista_negra, jsonFile) #copies and pastes the dictionary from the lista_negra variable into the json file
                                    jsonFile.close() #close this variable because bEsT PrAcTiCEs 
                                    i +=1
                                    break
                                else:
                                    print('Lastimomsamente, esta criptomoneda no pasó este último filtro, ya es muy vieja, procederemos a eliminarla de la lista de opciones, para luego seguir con la siguiente Tx Id')
                                    initial_df = initial_df.drop(initial_df.index[i])
                                    print(initial_df)
                                    i +=1
                                    break
                                                            
                            else:
                                print('Ni modo, esta criptomoneda no pasó este filtro de las transferencias, procederemos a eliminarla de la lista de opciones, para luego seguir con la siguiente Tx Id')
                                initial_df = initial_df.drop(initial_df.index[i])
                                print(initial_df)
                                i +=1
                                break
                        else: 
                            if Hodlers < 5600 or Hodlers > 20000:
                                print('Lamentablemente, esta criptomoneda no pasó este filtro de los HODLERS, procederemos a eliminarla de la lista de opciones, para luego seguir con la siguiente Tx Id')
                                initial_df = initial_df.drop(initial_df.index[i])
                                print(initial_df)
                                i +=1
                                break
        else:
            print("Esta transacción falló o tiene más de 5 tokens transferidos, se procede a eliminarla.")
            initial_df = initial_df.drop(initial_df.index[i])
            print(initial_df)
            i +=1
                    
    driver.quit()
    #here we delete duplicated rows just in case they appear at the end of our second part of the process, we use "Contract Address" as parameter.
    initial_df.drop_duplicates(subset='Contract Address', keep='first', inplace= True)
    dataframe_definitiva = dataframe_definitiva.append(initial_df, ignore_index = True)
    print(dataframe_definitiva)
    dataframe_definitiva = dataframe_definitiva.dropna()
    print(dataframe_definitiva)
    final_total_rows = len(dataframe_definitiva)
    #Now here we make sure that we are going to export only non-empty dfs.
    if final_total_rows == 0:
        print('Qué mal, al final de todo el proceso esta dataframe estuvo vacía (=/)')
    else:
        print(f'Ahora esta nueva DataFrame tiene {final_total_rows} fila(s) en total, fueron eliminadas: '+str(filas_iniciales-final_total_rows)+' filas en total.')
        dataframe_definitiva.to_csv(f'PREMIUM_Block_{initial_block}_to_{final_block}_1point95_BNB_PANCAKESWAPV2_without_duplicates_NOR_EMPTY_BLOCKS.csv')
        print('\n')
    #set 2 variables to know how much time has passed since this program was run
    final_time = datetime.now()
    time_elapsed = final_time - initial_time
    #print the time elapsed
    print(f'PROCESO FINALIZADO ʕ•́ᴥ•̀ʔっ♡, Tiempo de Ejecución: {time_elapsed}')
    print('\n')
    y += 1
    time.sleep(3)       
    #Here we re-instantiate the driver again to avoid a MaxRetryError
    driver = webdriver.Chrome(executable_path='C:/Users/ResetStoreX/AppData/Local/Programs/Python/Python39/Scripts/chromedriver.exe', options=options)
    #Now we set our delay time (seconds) randomly from 22 seconds to 87 seconds
    seconds = random.randint(2, 5)
    if y < limite:
        time.sleep(5)
        print('\033[46mAhora vamos a esperar un tiempo antes de repetir el proceso anterior :)')
        for o in range(seconds):
            if seconds - o == 1:
                print(f'\u001b[43mFalta {seconds - o} segundo para repetir el proceso anterior')
                print('\n')
            else:
                print(f'\u001b[43mFaltan {seconds - o} segundos para repetir el proceso anterior')
            time.sleep(1)
    else: 
        print('Ciclo terminado :3')
