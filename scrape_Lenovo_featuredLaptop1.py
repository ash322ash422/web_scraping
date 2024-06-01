from selenium import webdriver 
from selenium.webdriver.common.by import By 
from webdriver_manager.chrome import ChromeDriverManager 
from selenium.webdriver.chrome.service import Service as ChromeService
import time
from collections import OrderedDict

DEBUG = False
def dbg(*s, endline = '\n'):
    if DEBUG and isinstance(s, tuple):
        print( 'dbg:' + ''.join(map(str,s)) , end=endline)
#NOTE: This program reads the following featured laptops data: titles, prices, image links and descriptions.

URL = 'https://www.lenovo.com/in/en/laptops/'
#Following is not going to work b/c site is populated via javascript. So we use selenium.
#k = requests.get(URL, headers=headers) 
            
if __name__=='__main__':
    
    # for holding the resultant list 
    od = OrderedDict() 
    driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))
    driver.get(URL)
    time.sleep(5)

    #Read the featured list:
    titles = driver.find_elements(By.CLASS_NAME, "featureName") # featureName
    
    #Now we convert titles into str
    sanitized_titles = []
    for i in range(len(titles)): 
        dbg(titles[i].text)
        sanitized_titles.append(str(titles[i].text))
        
    #print("111111111111111111111111111")

    prices = driver.find_elements(By.CLASS_NAME, "prices > span")
    #Now we sanitize the price by removing duplicates. It contains each price twice.
    sanitized_prices = []
    for i in range(0,len(prices),2): #pick only odd 
        sanitized_prices.append(str(prices[i].text))
        
    dbg("222222222222222222222222222222")

    #Recurse class Feature_Home and then class imgWrap and finally find tag img
    images = driver.find_elements(By.CSS_SELECTOR, ".Feature_Home > .imgWrap > img") 
    sanitized_images_src = []
    for i in range(len(images)): 
        image_src = images[i].get_attribute("src")     
        dbg(image_src)
        sanitized_images_src.append(str(image_src))
    
    dbg("3333333333333333333333333333333333")
    #Find href that links to description
    links = driver.find_elements(By.CSS_SELECTOR, ".searchFeatureProduct .searchList a.lazy_href") 
    for i in range(len(links)):
        href = links[i].get_attribute("href") #NOTE: print(links[i].text) prints text
     
    #Now we sanitize the href by removing duplicates. It contains each href twice.
    sanitized_href = []
    for i in range(0,len(links),2): #pick only odd 
        sanitized_href.append(str(links[i].get_attribute("href")))
    dbg("4444444444444444444444444444444444")
    
    #Now we load the href and read the description:
    sanitized_descriptions = []
    for i in range(0,len(sanitized_href)):
        dbg(sanitized_href[i])
        driver.get(sanitized_href[i])
        time.sleep(5)
        descriptions = driver.find_elements(By.CSS_SELECTOR, ".banner_content_desc > ul > li")
        desc = []
        for i in  range(0,len(descriptions)):
            dbg("..",descriptions[i].text)
            desc.append(str(descriptions[i].text))
        sanitized_descriptions.append(desc)

    #Now we create element List
    elements = []
    for i in range(len(titles)):
        elements.append([sanitized_titles[i],
                        sanitized_prices[i],
                        sanitized_images_src[i],
                        sanitized_href[i],
                        sanitized_descriptions[i], #This is a list
                        ])
    dbg("FFFFFFFFFFFFFFFFFFFFFFFFFFFFFF")
    
    for i in range(0,len(elements)):
        print(elements[i])
    
    # Close the webdriver
    driver.quit()
    
