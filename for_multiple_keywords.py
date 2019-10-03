#install selenium and pandas packages
from selenium import webdriver
import re
import time
import datetime
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait


##importing csv(make sure csv file is situated in same folder in which python file exist else give the directory)
data = pd.read_csv(r'keywords.csv')  #csv file named as "keyword_relevancy"
data['keywords'] = data["keywords"].map(lambda x: x.lower())

# searching for keywords
kwd = data['keywords']    #column named as "keywords"

#output
finaldf = pd.DataFrame(columns = ['Keyword','cd_list_count','total products','Relevant Products'])

##login using password
driver = webdriver.Chrome("chromedriver.exe")
address = "http://dir.indiamart.com"
driver.get(address)
time.sleep(2)
driver.find_element_by_id("user_sign_in").click()
time.sleep(2)
driver.find_element_by_id("mobile").send_keys("9193977613")          #enter mobile no.
driver.find_element_by_class_name("continue_s").click()
time.sleep(5)
driver.find_element_by_class_name("cntmsg").click()
time.sleep(2)
driver.find_element_by_class_name("chat_view-all-contact-btn").click()
time.sleep(5)
driver.find_element_by_id("passwordbtn1").click()
time.sleep(2)
driver.find_element_by_id("usr_pass").send_keys("iamthebest")       #enter password
driver.find_element_by_id("submtbtn").click()
time.sleep(10)

products_count=0
def search(kw):
    address = "http://dir.indiamart.com/search.mp?ss=" + kw
    driver.get(address)
    SCROLL_PAUSE_TIME = 12


    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    print("Current time:", datetime.datetime.now())

    while True:
        try:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            print("pausing programming to scroll down a bit")
            time.sleep(SCROLL_PAUSE_TIME)

            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height

            print("\nCurrent time:", datetime.datetime.now())

        except:
            pass

    ## get the cd_list_count
    global products_count
    try:
        products_count = driver.find_element_by_class_name("cafp").text
        products_count = re.sub(r'[\(\)]', '', products_count)
        # products_count = products_count.split()

        print("\nNo. of products available(appearing after the keyword searched/cd_list_count): ", products_count)
    except:
        pass


    ## get the overall products count
    global items
    items = driver.find_elements_by_class_name("lst_cl")
    print("Total number of products coming after searching : ", len(items))

    ## get the relevant products count
    kw = kw.lower()

    global count
    count = 0

    for item in items:

        s_name = item.find_element_by_class_name("lg").text
        s_name = s_name.lower()

        if (kw.find(' ') != -1):
            kw = kw.split()
            new_value = ""
            for value in kw:
                new_value = new_value + value
            kw = new_value

        if (s_name.find(' ') != -1):
            s_name = s_name.split()
            new_value = ""
            for value in s_name:
                new_value = new_value + value
            s_name = new_value

        if (s_name.find(kw) != -1):
            count = count + 1

    print("Relevant products matching string= ", count)

row=0
for i in kwd:
    search(i)

    finaldf.set_value(row, 'Keyword', i)
    finaldf.set_value(row, 'cd_list_count', products_count)
    finaldf.set_value(row, 'total products', len(items))
    finaldf.set_value(row, 'Relevant Products', count)
    row = row + 1

driver.close()
finaldf.to_csv("D:/finalOutput1.csv")   # csv file downloaded as "finalOutput"

