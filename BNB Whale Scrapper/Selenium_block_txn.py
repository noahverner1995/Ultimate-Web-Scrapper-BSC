#previous requirements

#sudo apt-get update
#sudo apt-get install chromium-driver -y
#!pip install webdriver-manager
#!pip install selenium


#libraries
import re
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

#general config for the web driver
driver = webdriver.Chrome(ChromeDriverManager().install())
driver.implicitly_wait(10)


#parameters for the scrapping
#values for the example

block = 9875875
minimun_value_txn = 0.10
to_chain = 'Pancake'

#INITIAL SEARCH
#look for general data of the link
#amount of results and pages for the execution of the for loop
url = 'https://bscscan.com/txs?block={}&p=1'.format(block)
driver.get(url)
pages =  driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_topPageDiv"]/nav/ul/li[3]/span').text
pages = int(re.search(r'\d{0,3}$', pages).group())


#FOR LOOP
#search at each page all the values we are looking for
#following conditions like number of the block, minimun value of the txn and the destiny

for page in range(1,pages+1):
    
    url = 'https://bscscan.com/txs?block={}&p={}'.format(block,page)
    driver.get(url)
    txn_found = int(driver.find_element_by_xpath('//*[@id="ContentPlaceHolder1_topPageDiv"]/p/span').text.replace('A total of ','').replace(' transactions found',''))
    txn_found_last=txn_found%50
    
    if page < pages:
        for txn in range(1,50+1):
            txn_hash = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[2]'.format(txn)).text)
            block_num = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[3]'.format(txn)).text)
            value_txn = float((driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[9]'.format(txn)).text).replace(' BNB',''))
            to_destiny = driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[8]'.format(txn)).text
            if value_txn >= minimun_value_txn and to_chain in to_destiny:
                print(txn_hash,block_num,value_txn)
    else:
        for txn in range(1,txn_found_last+1):
            txn_hash = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[2]'.format(txn)).text)
            block_num = str(driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[3]'.format(txn)).text)
            value_txn = float((driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[9]'.format(txn)).text).replace(' BNB',''))
            to_destiny = driver.find_element_by_xpath('//*[@id="paywall_mask"]/table/tbody/tr[{}]/td[8]'.format(txn)).text
            if value_txn >= minimun_value_txn and to_chain in to_destiny:
                print(txn_hash,block_num,value_txn)
        
print('busqueda finalizada')

#you can replace de prints for appends in order to save them on a pandas dataframe, for example.
