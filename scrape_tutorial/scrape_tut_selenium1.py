from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService

#Following opens the web browser
driver = webdriver.Firefox() #works
driver.get("https://google.co.in/search?q=geeksforgeeks") #opens the browser too
##################################################

# for holding the resultant list 
element_list = [] 
  
for page in range(1, 3, 1): 
  
    page_url = "https://webscraper.io/test-sites/e-commerce/static/computers/laptops?page=" + str(page) 
    #driver = webdriver.Chrome(ChromeDriverManager().install()) #NOT working
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(page_url) 
    title = driver.find_elements(By.CLASS_NAME, "title") 
    price = driver.find_elements(By.CLASS_NAME, "price") 
    description = driver.find_elements(By.CLASS_NAME, "description") 
    rating = driver.find_elements(By.CLASS_NAME, "ratings") 
  
    for i in range(len(title)): 
        element_list.append([title[i].text, price[i].text, description[i].text, rating[i].text]) 
    #end for
#end for
  
print(element_list) 
  
#closing the driver 
driver.close()
print("######################################")
from selenium.webdriver.common.keys import Keys

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
driver.get("https://www.python.org")
print("driver.title=",driver.title)
search_bar = driver.find_element("name", "q") #i.e. find element by name
search_bar.clear()
search_bar.send_keys("getting started with python")
search_bar.send_keys(Keys.RETURN)
print("driver.current_url=",driver.current_url)
driver.close()

"""
    
DevTools listening on ws://127.0.0.1:50300/devtools/browser/c88c4bb1-2e44-425f-bce8-e6e5f583b224
[['Packard 255 G2', '$416.99', '15.6", AMD E2-3800 1.3GHz, 4GB, 500GB, Windows 8.1', '2 reviews'],
 ['Aspire E1-510', '$306.99', '15.6", Pentium N3520 2.16GHz, 4GB, 500GB, Linux', '2 reviews'], 
 ['ThinkPad T540p', '$1178.99', '15.6", Core i5-4200M, 4GB, 500GB, Win7 Pro 64bit', '2 reviews'],...
 ...]
 ######################################

DevTools listening on ws://127.0.0.1:56610/devtools/browser/2d7b747f-639d-4abf-acc5-309525d39342
driver.title= Welcome to Python.org
driver.current_url= https://www.python.org/search/?q=getting+started+with+python&submit=
"""