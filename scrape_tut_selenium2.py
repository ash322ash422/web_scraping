from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService

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

"""
    
DevTools listening on ws://127.0.0.1:50300/devtools/browser/c88c4bb1-2e44-425f-bce8-e6e5f583b224
[['Packard 255 G2', '$416.99', '15.6", AMD E2-3800 1.3GHz, 4GB, 500GB, Windows 8.1', '2 reviews'],
 ['Aspire E1-510', '$306.99', '15.6", Pentium N3520 2.16GHz, 4GB, 500GB, Linux', '2 reviews'], 
 ['ThinkPad T540p', '$1178.99', '15.6", Core i5-4200M, 4GB, 500GB, Win7 Pro 64bit', '2 reviews'],...
 ...]
"""