from selenium import webdriver
import selenium
import re
import time
import datetime

#enter keyword
product = input("Enter the keyword for which you want to check the relevancy: ")
product = product.lower()
if len(product)>0:
    print("Searching for:", product)
else:
    print("No product entered, exiting the program.")
    quit()

#login_via_password
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
address = "http://dir.indiamart.com/search.mp?ss=" + product
driver.get(address)

SCROLL_PAUSE_TIME = 20 ## wait for 15 seconds

# Get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

print("Current time:", datetime.datetime.now())

## load list items count
last_items_count = len(driver.find_elements_by_class_name("lst_cl"))

i = 4

# userLoggedIn = False
while True:
    scroll_value = "scroll" + str(i)
    try:

        ## load last list item from unordered list
        unordered_list = driver.find_element_by_class_name("wlm")

        ## getting list items
        list_items = unordered_list.find_elements_by_tag_name("li")[-1]
        scroll_attribute = list_items.get_attribute("id")

        if scroll_attribute.find('scroll') != -1:

            fxn_name = "javascript: displayResultsLogin('" + scroll_attribute + "')"

            driver.execute_script(fxn_name)

            # scroll_button = driver.find_element_by_id(scroll_value).click()
            print('Clicked on scroll button, with id:', i)

            i = i + 1
    except selenium.common.exceptions.NoSuchElementException as error:
        print("No such element found")


    # Scroll down to bottom
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

    # Wait to load page
    print("pausing programming to scroll down a bit, i:", i)
    time.sleep(SCROLL_PAUSE_TIME)

    new_height = driver.execute_script("return document.body.scrollHeight")

    new_item_count = len(driver.find_elements_by_class_name("lst_cl"))
    print("New Items count:", new_item_count)

    if  (new_height == last_height) & (new_item_count == last_items_count) :
        break
    last_height = new_height
    last_items_count = new_item_count

    print("\nCurrent time:", datetime.datetime.now())


# driver.close()

## get the overall suppliers count
suppliers_count = driver.find_element_by_class_name("cafp").text

suppliers_count = re.sub(r'[\(\)]', '', suppliers_count)

# suppliers_count = suppliers_count.split()
print("\nNo. of products available(cd_list_count):", suppliers_count)

items = driver.find_elements_by_class_name("lst_cl")
print("Total products/services found:", len(items))

product = product.lower()

count = 0

for item in items:

    s_name = item.find_element_by_class_name("lg").text
    s_name = s_name.lower()

    if product.find(' ') != -1:
        product = product.split()
        new_value = ""
        for value in product:
            new_value = new_value + value
        product = new_value

    if s_name.find(' ') != -1:
        s_name = s_name.split()
        new_value = ""
        for value in s_name:
            new_value = new_value + value
        s_name = new_value

    if s_name.find(product) != -1:
        count = count+1

print("Relevant Product/services found:", count, "out of", len(items), "total products found")
driver.close()


