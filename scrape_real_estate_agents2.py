from lxml import html
#from bs4 import BeautifulSoup
import requests
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

# note that without this header, a website may give you a puzzle to solve
my_headers = {'User-Agent': 'Mozilla/5.0'}

# scrape the webpage
url = "https://maharera.maharashtra.gov.in/agents-search-result?agent_name=&agent_project_name=&agent_location=&agent_state=27&agent_division=&agent_district=&page=1&op=Search"
#url = "https://www.reddit.com/r/puppies/"
r = requests.get(url, headers=my_headers)
# Ensure the request was successful and parse the content
if r.status_code != 200:
    print("Failed to retrieve the webpage")
    sys.exit()

#soup = BeautifulSoup(r.content, 'html.parser')

tree = html.fromstring(r.content)

# Find all table elements
tables = tree.xpath('//table')

for table in tables: #outer for
    # Assuming each table has rows (tr) and cells (th/td)
    rows = table.xpath('.//tr')
    agents = []
    for row in rows:
        # Extract headers (assuming they are in the first row)
        headers = row.xpath('.//th/text()')
        if headers:
            print('Headers:', headers)

        # Extract data cells
        cells = row.xpath('.//td/text()')
        if cells:
            print('Row Data:', cells,)
            name, reg_num = cells[1], cells[2]
            agents.append({'name': name, 'reg_num': reg_num})
#end outer for

print("agents=",agents)
