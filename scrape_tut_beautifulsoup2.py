import requests 
from bs4 import BeautifulSoup, SoupStrainer  
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# Making a GET request 
r = requests.get('https://www.geeksforgeeks.org/python-programming-language/') 
  
# check status code for response received :success code - 200 
print("r=",r) 
print("#################################################")

# print content of request 
print("r.content=",r.content)
print("#################################################")

# Parsing the HTML 
soup = BeautifulSoup(r.content, 'html.parser')
print(soup.prettify()) 

print("****************************************************")
"""
s = soup.find('div', class_='entry-content')# find tags <div class="entry-content">
lines = s.find_all('p') # find tags <p> inside of above-mentioned tags.
for line in lines:
    print(line.text) #prints text without tags
"""
print("||||||||||||||||||||||||||||||||||||||||||||||||||||")
# Finding by id
s = soup.find('div', id= 'main')

# Getting the left bar
leftbar = s.find('ul', class_='leftBarList')
 
# All the li under the above ul
lines = leftbar.find_all('li')
 
for line in lines:
    print(line.text)
print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
URL = "https://en.wikipedia.org/wiki/Nike,_Inc."

# We send Header and added a user agent to ensures that the target website web scraping doesn’t consider
# traffic from our program as spam and finally gets blocked by them
HEADERS = ({'User-Agent':  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36', 
            'Accept-Language': 'en-US, en;q=0.5'})  
  
r = requests.get(URL, headers= HEADERS)
soup = BeautifulSoup(r.content, "lxml", #NOTE: pip install lxml 
                     parse_only = SoupStrainer('span', class_ = 'mw-headline')
                    ) 
  
print(soup.prettify()) 
print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
r = requests.get('https://demo.vuestorefront.io/category/accessories/accessories-women/accessories-women-sunglasses')
soup = BeautifulSoup(r.content, 'html.parser')
#NOTE: select anchor tags with the attribute data-testid set to link within elements having the class grid.
for item in soup.select('.grid a[data-testid="link"]'):
    print(item.text)