from selenium import webdriver
import re
import time
import datetime
import pandas as pd

data = pd.read_csv(r'C:\Users\Shaly\PycharmProjects\untitled1\keywords.csv')
gst_no = data["gst no."]
finaldf = pd.DataFrame(columns=["gst no.", "result"])

driver = webdriver.Chrome("chromedriver.exe")
address = "https://gstim4096:welcome2019@www.gstvalidator.com/~gst/~1.php"
driver.get(address)

def search(gst_no):
    global final2
    gst_enter = driver.find_element_by_xpath("//*[@id='gst_number']")
    gst_enter.send_keys(gst_no)
    driver.find_element_by_xpath("//*[@id='gst_form_submit_button']").click()
    time.sleep(4)
    final = driver.find_element_by_xpath("//*[@id='gst-panel-+str(gst_no)+']")
    final2 = final.text
    print(final2)

row = 0
for i in gst_no:
    search(i)
    finaldf.set_value(row, 'gst no.', i)
    finaldf.set_value(row, 'result', final2)
    row = row+1
    finaldf.to_csv("D:/finalOutputgst.csv")
driver.quit()
