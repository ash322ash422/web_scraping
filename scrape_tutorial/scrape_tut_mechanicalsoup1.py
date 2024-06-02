import mechanicalsoup
browser = mechanicalsoup.Browser()
url = "http://olympus.realpython.org/login"
login_page = browser.get(url)
print("login_page=",login_page)

login_html = login_page.soup
print("login_html=",login_html)

form = login_html.select("form")[0]
print("form.select('input')=",form.select('input'))
form.select("input")[0]["value"] = "zeus"
form.select("input")[1]["value"] = "ThunderDude"
#NOTE: tag = login_page.soup.select("#result") would return list of all tags with id=result

profiles_page = browser.submit(form, login_page.url)
print("profiles_page.url=",profiles_page.url)
# NOTE:For successful login you will see http://olympus.realpython.org/profiles
# NOTE:For failed login you will see http://olympus.realpython.org/login
print("###################################")
base_url = "http://olympus.realpython.org"
links = profiles_page.soup.select("a")#select all the <a> anchor elements on the page
for link in links:
    address = base_url + link["href"]
    text = link.text
    print(f"{text}: {address}")
"""
login_page= <Response [200]>
login_html= <html>
<head>
<title>Log In</title>
</head>
<body bgcolor="yellow">
<center>
<br/><br/>
<h2>Please log in to access Mount Olympus:</h2>
<br/><br/>
<form action="/login" method="post" name="login">
Username: <input name="user" type="text"/><br/>
Password: <input name="pwd" type="password"/><br/><br/>
<input type="submit" value="Submit"/>
</form>
</center>
</body>
</html>

form.select('input')= [<input name="user" type="text"/>, <input name="pwd" type="password"/>, <input type="submit" value="Submit"/>]
profiles_page.url= http://olympus.realpython.org/profiles
###################################
Aphrodite: http://olympus.realpython.org/profiles/aphrodite
Poseidon: http://olympus.realpython.org/profiles/poseidon
Dionysus: http://olympus.realpython.org/profiles/dionysus
"""