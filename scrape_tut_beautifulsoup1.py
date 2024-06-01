
from bs4 import BeautifulSoup
from urllib.request import urlopen

url = "http://olympus.realpython.org/profiles/dionysus"
page = urlopen(url)
html = page.read().decode("utf-8")
soup = BeautifulSoup(html, "html.parser")

print(soup.prettify())
print("!!!!!!!!!!!!!!!!!!!!!")
print(soup.get_text())
print("@@@@@@@@@@@@@@@@@@@@@")
print(soup.find_all("img"))
print("######################")
image1, image2 = soup.find_all("img")
print("image1.name=",image1.name,"; image1['src']=",image1['src'])
print("$$$$$$$$$$$$$$$$$$$$$$")
print("soup.title=",soup.title)
print("soup.title.string=",soup.title.string)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%")
print("soup.find_all('img', src='/static/dionysus.jpg')=",soup.find_all('img', src='/static/dionysus.jpg'))
"""
<html>
 <head>
  <title>
   Profile: Dionysus
  </title>
 </head>
 <body bgcolor="yellow">
  <center>
   <br/>
   <br/>
   <img src="/static/dionysus.jpg"/>
   <h2>
    Name: Dionysus
   </h2>
   <img src="/static/grapes.png"/>
   <br/>
   <br/>
   Hometown: Mount Olympus
   <br/>
   <br/>
   Favorite animal: Leopard
   <br/>
   <br/>
   Favorite Color: Wine
  </center>
 </body>
</html>

!!!!!!!!!!!!!!!!!!!!!


Profile: Dionysus





Name: Dionysus

Hometown: Mount Olympus

Favorite animal: Leopard

Favorite Color: Wine




@@@@@@@@@@@@@@@@@@@@@
[<img src="/static/dionysus.jpg"/>, <img src="/static/grapes.png"/>]
######################
image1.name= img ; image1['src']= /static/dionysus.jpg
$$$$$$$$$$$$$$$$$$$$$$
soup.title= <title>Profile: Dionysus</title>
soup.title.string= Profile: Dionysus
%%%%%%%%%%%%%%%%%%%%%%%%%%
soup.find_all('img', src='/static/dionysus.jpg')= [<img src="/static/dionysus.jpg"/>]
"""      
