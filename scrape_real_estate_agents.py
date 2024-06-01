import requests
import lxml.html
from bs4 import BeautifulSoup
#from lxml import etree
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# note that without this header, a website may give you a puzzle to solve
my_headers = {'User-Agent': 'Mozilla/5.0'}

# scrape the webpage
url = "https://maharera.maharashtra.gov.in/agents-search-result"
#url = "https://www.reddit.com/r/puppies/"
r = requests.get(url, headers=my_headers)
# Ensure the request was successful and parse the content
if r.status_code != 200:
    print("Failed to retrieve the webpage")
    sys.exit()

soup = BeautifulSoup(r.content, 'html.parser')
#print(soup.prettify()) 

html_data = soup.find('table', class_='tableData')

print("html_data=",html_data)
print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
root = lxml.html.fromstring(html_data.text)
print("root=",root)

for element in root.iter():
    #print(f"{element.tag} - {element.text}")
    print(f"{element.text}")
print("\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\")
