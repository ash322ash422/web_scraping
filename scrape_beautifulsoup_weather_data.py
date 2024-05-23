import requests
from bs4 import BeautifulSoup
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')
 
# enter city name
city = "lucknow"
 
# creating url and requests instance
url = "https://www.google.com/search?q="+"weather"+city # URL=https://www.google.com/search?q=weatherlucknow
html = requests.get(url).content
 
# getting raw data
soup = BeautifulSoup(html, 'html.parser')
print("soup=",soup)
temp = soup.find('div', attrs={'class': 'BNeawe iBp4i AP7Wnd'}).text
print("temp=",temp)

str = soup.find('div', attrs={'class': 'BNeawe tAd8D AP7Wnd'}).text 
# formatting data
data = str.split('\n')
time = data[0]
sky = data[1]
 
# getting all div tag
listdiv = soup.findAll('div', attrs={'class': 'BNeawe s3v9rd AP7Wnd'})
strd = listdiv[5].text
 
# getting other required data
pos = strd.find('Wind')
other_data = strd[pos:]
 
# printing all data
print("Temperature is", temp)
print("Time: ", time)
print("Sky Description: ", sky)
print(other_data)