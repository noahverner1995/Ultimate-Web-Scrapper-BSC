# -*- coding: utf-8 -*-
"""
Created on Sat Aug  7 19:32:50 2021

@author: Noah Verner & @felipesalda
"""
import os
if os.name == 'nt': # Let's add some colors for the lulz
    from ctypes import windll
    k = windll.kernel32
    k.SetConsoleMode(k.GetStdHandle(-11), 7)
import re
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
#Now we set the amount of reruns (limite) to 4, this means this loop will run 3 times, because it starts in 1, not in 0
limite = 4
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
    #Here we use the Xpath element of the most recent block validated in bitquery explorer
    initial_block = int(driver.find_element_by_xpath('//*[@id="content"]/div[2]/div/div/div[2]/table/tbody/tr[1]/td[1]/a').text)
    print(f'El bloque inicial para este proceso es el No. {initial_block}')   
    final_block = initial_block + 120
    #It seems that the current most recent validated block from bitquery explorer is delayed by around 57 blocks to BscScan, so for the blocks arange, initial_block element is incremented in 48
    blocks = np.arange(initial_block, final_block+1, 1)
    minimun_value_txn = 1.95
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
    
    #Here we set a black_list of cryptocurrencies which are NOT interesting to us.
    lista_negra = {"BUSD": '0xe9e7cea3dedca5984780bafc599bd69add087d56', "Binance-Peg ETH": '0x2170ed0880ac9a755fd29b2688956bd959f933f8',
                   "Binance-Peg ADA": '0x3ee2200efb3400fabb9aacf31297cbdd1d435d47', "Binance-Peg BSC-USD": '0x55d398326f99059ff775485246999027b3197955',
                   "Binance-Peg XRP": '0x1d2f0da169ceb9fc7b3144628db156f3f6c60dbe', "Binance-Peg DOGE": '0xba2ae424d960c26247dd6c32edc70b295c744c43',
                   "Binance-Peg USDC": '0x8ac76a51cc950d9822d68b83fe1ad97b32cd580d', "Binance-Peg DOT": '0x7083609fce4d1d8dc0c979aab8c869ea2c873402',
                   "Binance-Peg UNI": '0xbf5140a22578168fd562dccf235e5d43a02ce9b1', "Binance-Peg LINK": '0xf8a0bf9cf54bb92f17374d9e9a321e6a111a51bd',
                   "Binance-Peg LTC": '0x4338665cbb7b2485a8855a139b75d5e34ab0db94', "Binance-Peg BCH": '0x8ff795a6f4d97e7887c79bea79aba5cc76444adf',
                   "Binance-Peg AVAX": '0x1ce0c2827e2ef14d5c4f29a091d735a204794041', "Binance-Peg ETC": '0x3d6545b08693dae087e957cb1180ee38b9e3c25e',
                   "Binance-Peg DAI": '0x1af3f329e8be154074d8769d1ffa4ee058b1dbc3', "Binance-Peg TRX": '0x85eac5ac2f758618dfa09bdbe0cf174e7d574d5b',
                   "Binance-Peg ATOM": '0x0eb3a705fc54725037cc9e008bdede697f62f335', "Binance-Peg EOS": '0x56b6fb708fc5732dec1afc8d8556423a2edccbd6',
                   "CAKE": '0x0e09fabb73bd3ade0a17ecc321fd13a19e81ce82', "Binance-Peg AXS": '0x715d400f88c167884bbcc41c5fea407ed4d2f8a0',
                   "Binance-Peg BTC": '0x7130d2a12b9bcbfae4f2634d864a1ee1ce3ead9c', "Binance-Peg FTM": '0xad29abb318791d579433d831ed122afeaf29dcfe',
                   "Binance-Peg BTT": '0x8595f9da7b868b1822194faed312235e43007b49', "Binance-Peg UST": '0x23396cf899ca06c4472205fc903bdb4de249d6fc',
                   "Binance-Peg SHIB": '0x2859e4544c4bb03966803b044a93563bd2d0dd4d', "Binance-Peg COMP": '0x52ce071bd9b1c4b00a0b92d298c512478cad67e8',
                   "Binance-Peg TUSD": '0x14016e85a25aeb13065688cafb43044c2ef86784', "Binance-Peg ZIL": '0xb86abcb37c3a4b64f74f59301aff131a1becc787',
                   "Binance-Peg BAT": '0x101d82428437127bf1608f699cd651e6abf9766e', "SAFEMOON": '0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
                   "C98": '0xaec945e04baf28b135fa7c640f624f8d90f1c3a6', "Binance-Peg 1INCH": '0x111111111117dc0aa78b770fa6a738034120c302',
                   "Binance-Peg SXP": '0x47bead2563dcbf3bf2c9407fea4dc236faba485a', "TWT": '0x4b0f1812e5df2a09796481ff14017e6005508003',
                   "Binance-Peg MKR": '0x5f0da599bb2cccfcf6fdfd7d81743b6020864350', "BAKE": '0xE02dF9e3e622DeBdD69fb838bB799E3F168902c5',
                   "XVS": '0xcf6bb5389c92bdda8a3747ddb454cb7a64626c63', "Binance-Peg BAND": '0xad6caeb32cd2c308980a548bd0bc5aa4306c6c18',
                   "Binance-Peg REEF": '0xf21768ccbc73ea5b6fd3c687208a7c2def2d966e', "TLM": '0x2222227e22102fe3322098e4cbfe18cfebd57c95',
                   "Binance-Peg COTI": '0xadbaf88b39d37dc68775ed1541f1bf83a5a45feb', "ALICE": '0xac51066d7bec65dc4589368da368b212745d63e8',
                   "DODO": '0x67ee3cb086f8a16f34bee3ca72fad36f7db929e2', "vBTC": '0x882c173bc7ff3b7786ca16dfed3dfffb9ee7847b',
                   "ATA": '0xa2120b9e674d3fc3875f415a7df52e382f141225', "TKO": '0x9f589e3eabe42ebc94a44727b3f3531c0c877809',
                   "ALPACA": '0x8f0528ce5ef7b51152a59745befdd91d97091d2f', "vETH": '0xf508fcd89b8bd15579dc79a6827cb4686a3592c8',
                   "EPS": '0xa7f552078dcc247c2684336020c03648500c6d9f', "POLS": '0x7e624fa0e1c4abfd309cc15719b7e2580887f570',
                   "SFP": '0xd41fdb03ba84762dd66a0af1a6c8540ff1ba5dfb', "FEG": '0xacfc95585d80ab62f67a14c566c1b7a49fe91167',
                   "CTK": '0xa8c2b8eec3d368c0253ad3dae65a5f2bbb89c929', "LIT": '0xb59490ab09a0f526cc7305822ac65f2ab12f9723',
                   "Binance-Peg CREAM": '0xd4cb328a82bdf5f03eb737f37fa6b370aef3e888', "BZRX": '0x4b87642aedf10b642be4663db842ecc5a88bf5ba',
                   "VAI": '0x4bd17003473389a42daf6a0a729f6fdb328bbbd7', "RFOX": '0x0a3a21356793b49154fd3bbe91cbc2a16c0457f5',
                   "AUTO": '0xa184088a740c695e156f91f5cc086a06bb78b827', "FRONT": '0x928e55dab735aa8260af3cedada18b5f70c72f1b',
                   "BURGER": '0xae9269f27437f0fcbc232d39ec814844a51d6b8f', "CHESS": '0x20de22029ab63cf9a7cf5feb2b737ca1ee4c82a6',
                   "SPARTA": '0x3910db0600ea925f63c36ddb1351ab6e2c6eb102', "HTB": '0x4e840aadd28da189b9906674b4afcb77c128d9ea',
                   "SKILL": '0x154a9f9cbd3449ad22fdae23044319d6ef2a1fab', "LMT": '0x9617857e191354dbea0b714d78bc59e57c411087',
                   "SPORE": '0x33a3d962955a3862c8093d1273344719f03ca17c', "CTI": '0x3f670f65b9ce89b82e82121fd68c340ac22c08d6',
                   "EGG": '0xf952fc3ca7325cc27d15885d37117676d25bfda6', "SHIELD": '0x60b3bc37593853c04410c4f07fe4d6748245bf77',
                   "Binance-Peg BETH": '0x250632378e573c6be1ac2f97fcdf00515d0aa91b', "PASTA": '0xab9d0fae6eb062f2698c2d429a1be9185a5d4f6e',
                   "BOG": '0xb09fe1613fe03e7361319d2a43edc17422f36b09', "RISE": '0xc7d43f2b51f44f09fbb8a691a0451e8ffcf36c0a',
                   "CHI": '0x0000000000004946c0e9f43f4dee607b0ef1fa1c', "POCO": '0x394bba8f309f3462b31238b3fd04b83f71a98848',
                   "MWAR": '0xf8a1919da520a6c3b92e6abc64bf83c8d4432b14', "GON": '0x610f34da19797405a276d26f95bd5c7d8cbbd644',
                   "BIN": '0xe56842ed550ff2794f010738554db45e60730371', "AIR": '0xd8a2ae43fd061d24acd538e3866ffc2c05151b53',
                   "NFTL": '0xe7f72bc0252ca7b16dbb72eeee1afcdb2429f2dd', "ULTI": '0x42bfe4a3e023f2c90aebffbd9b667599fa38514f',
                   "DZOO": '0x5419291d81c68c103363e06046f40a9056ab2b7f', "PEARL": '0x118b60763002f3ba7603a3c17f946a0c7dab789f',
                   "LORD": '0x2daf1a83aa348afbcbc73f63bb5ee3154d9f5776', "MPS": '0x9eb5b7902d2be0b5aaba2f096e043d3cd804e6df',
                   "ADAPAD": '0xdb0170e2d0c1cc1b2e7a90313d9b9afa4f250289', "WAG": '0x7fa7df4996ac59f398476892cfb195ed38543520',
                   "DOGEX": '0x1f6819d87bd6e10cae34883175232ee9774e00b2', "BPET": '0x24d787e9b88cb62d74e961c1c1d78e4ee47618e5',
                   "HONEYPAD": '0xdb607c61aaa2a954bf1f9d117953f12d6c319e15', "ECC": '0x8d047f4f57a190c96c8b9704b39a1379e999d82b',
                   "HoneyPadDividendTracker": '0x2c65debf3c7671cb79340bddb0893fbb0d5accd7', "MEDA": '0x9130990dd16ed8be8be63e46cad305c2c339dac9',
                   "MONS": '0xe4c797d43631f4d660ec67b5cb0b78ef5c902532', "IDTT": '0x6fb1e018f107d3352506c23777e4cd62e063584a',
                   "GLMS": '0x75f53011f6d51c60e6dcbf54a8b1bcb54f07f0c9', "XPNET": '0x8cf8238abf7b933bf8bb5ea2c7e4be101c11de2a',
                   "ZOO": '0x19263f2b4693da0991c4df046e4baa5386f5735e', "BIT": '0xc864019047b864b6ab609a968ae2725dfaee808a',
                   "ETERNAL": '0xd44fd09d74cd13838f137b590497595d6b3feea4', "MONS": '0xe4c797d43631f4d660ec67b5cb0b78ef5c902532',
                   "APAD": '0x366d71ab095735b7dae83ce2b82d5262ef655f10', "GEMG": '0x885c5fb8f0e67b2b0cf3a437e6cc6ebc0f9f9014',
                   "VERO": '0x0ef008ff963572d3dabc12e222420f537ddabf94', "GRBE": '0x8473927b49e6dd0548f8287ea94109b7b753e3cf',
                   "HER": '0x6b9f6f911384886b2e622e406327085238f8a3c5', "FNDZ": '0x7754c0584372d29510c019136220f91e25a8f706',
                   "THG": '0x9fd87aefe02441b123c3c32466cd9db4c578618f', "ForeverFOMO": '0x95637d4fbe7153dcc3e26e71bde7a2d82621f083',
                   "GRX": '0x8fba8c1f92210f24fb277b588541ac1952e1aac8', "DSBOWL": '0x6a43f8f4b12fcd3b3eb86b319f92eb17c955dda3',
                   "DOX": '0x30ea7c369b87fe261de28a1eefafe806696a738b', "GZONE":'0xb6adb74efb5801160ff749b1985fd3bd5000e938',
                   "BabyFloki": '0x71e80e96af604afc23ca2aed4c1c7466db6dd0c4', "GHC":'0x683fae4411249ca05243dfb919c20920f3f5bfe0',
                   "KING": '0x0ccd575bf9378c06f6dca82f8122f570769f00c2', "BEPR": '0xbf0cf158e84ebacca1b7746e794d507073e5adfe'}
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
        #Here we check first if the Tx Id provided was a Success or a Failure, If Success, we continue with the process, else we delete the current row from the df and start again with the following one.
        #However, firstly we are going to set a new while loop to make sure that the status element is going to be located and readable when needed
        #But first, we set our counter (z) to 0
        z = 0
        while z < 100:
            try:
                WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'//*[@id="ContentPlaceHolder1_maintable"]/div[2]/div[2]/span')))
                status = str(driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_maintable"]/div[2]/div[2]/span').text)
                #If status element is located and read, Bingo, problem is no more!
                z = 0
                break
            except:
                #Else, this bitch is going to sleep tight for 3 seconds for then repeating the loop until problem is no more!
                print('Joder, el estado de esta transacción aún no es visible (-_-"), lo intentaré de nuevo...')
                time.sleep(3)
                z += 1
        if status == 'Success':
            print(f'Esta transacción tiene un status: {status}')        
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
                datos = {'Name': token.text, 'Address': token.get_attribute("href").replace('https://bscscan.com/token/','')}
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
                        Hodlers = int(driver.find_element_by_xpath('/html/body/div[1]/main/div[4]/div[1]/div[1]/div/div[2]/div[3]/div/div[2]/div/div').text.replace(',','').replace(' ','').replace('addresses',''))
                        print(f'En este momento, esta criptomoneda tiene un total de {Hodlers} HODLERS')
                        if Hodlers >= 3000 and Hodlers < 20000:
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
                            if int(Transfers) >= 2*Hodlers:
                                print('Estupendo, esta criptomoneda cumple con el filtro de las transferencias, procederemos a aplicar un último filtro')
                                url_3 = 'https://explorer.bitquery.io/bsc/token/{}'.format(Addresser)
                                driver.get(url_3)
                                print('\n')
                                print('Evaluando la edad de esta criptomoneda...')
                                #Right below, we are going to set a new while loop to make sure that the contract_age element is going to be located and readable when needed
                                #But first, we set our counter (x) to 0
                                x = 0
                                while x < 100:
                                    try:
                                        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH,'/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr[9]/td[2]/span')))
                                        contract_age = driver.find_element_by_xpath('/html/body/div[2]/div[3]/div/div[2]/div/div[2]/div/div[1]/div/div[1]/table/tbody/tr[9]/td[2]/span').text
                                        #If contract_age element is located and read, Bingo, problem is no more!
                                        print(f'Esta criptomoneda tiene {contract_age} días de edad')
                                        x = 0
                                        break
                                    except:
                                        #Else, this bitch is going to sleep tight for 3 seconds for then repeating the loop until problem is no more!
                                        print('Joder, no encontré este elemento en el tiempo deseado (-_-), lo intentaré de nuevo...')
                                        time.sleep(3)
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
                            if Hodlers < 3000 or Hodlers > 20000:
                                print('Lamentablemente, esta criptomoneda no pasó este filtro de los HODLERS, procederemos a eliminarla de la lista de opciones, para luego seguir con la siguiente Tx Id')
                                initial_df = initial_df.drop(initial_df.index[i])
                                print(initial_df)
                                i +=1
                                break
        else:
            print("Esta transacción falló, se procede a eliminarla.")
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
    seconds = random.randint(22, 87)
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
    
