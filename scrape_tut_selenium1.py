from selenium import webdriver
  
driver = webdriver.Firefox() #works
#driver = webdriver.Chrome()
driver.get("https://google.co.in/search?q=geeksforgeeks") #opens the browser too
