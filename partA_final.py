import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import requests
from bs4 import BeautifulSoup
from selenium.common.exceptions import WebDriverException
import pandas as pd

#take the required website as an input
inp=input('Enter the link: ')

driver = webdriver.Chrome()
driver.get(inp)

link = driver.find_elements_by_tag_name("a")

links_list=list()

status_code_list=list()

time_taken=list()

count=0
sum=0
#scanning for each link
for each_link in link:
    current_link = each_link.get_attribute("href")
    links_list.append(current_link)
    if str(current_link) != current_link:
        status_code_list.append(-1)
        time_taken.append(-1)
        continue
    #removing non-working links
    condition_1 = current_link.startswith("https://")
    condition_2 = current_link.startswith("http://")
    final_ans = condition_1 | condition_2
    if final_ans == 0:
        status_code_list.append(-1)
        time_taken.append(-1)
        continue
    try:
        r = requests.head(current_link)
        status_code_list.append(r.status_code)
    except:
        status_code_list.append("-1")

    #checking the link 5 times and averaging it
    no_response=0
        #count=count+1
    for i in range(5):
        driver1 = webdriver.Chrome()
        count=count+1
        start_time = time.time()
        try:
            driver1.get(current_link)
        except WebDriverException:
            print('A page didnt respond.')
            no_response=no_response+1
            #status_code_list.append('Not working.')
            #time_taken.append('Not working.')
        end_time = time.time()
        final=end_time-start_time
        sum=sum+final
        driver1.close()
    avg=sum/count
    time_taken.append(avg)

print(links_list)
print(status_code_list)
print(time_taken)

link_yesno=list()

for i in time_taken:
    if float(i)==-1:
        link_yesno.append('N')
    elif float(i)>60:
        link_yesno.append('N')
    else:
        link_yesno.append('Y')


total_no_response=no_response/5

print(link_yesno)
df=pd.DataFrame({'names':links_list,'status':status_code_list,'time_taken':time_taken,'yes/no':link_yesno})
df.to_excel('./test_website.xlsx')
print('Total dead links are:',total_no_response)
