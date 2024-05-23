from lxml import html
from bs4 import BeautifulSoup
import requests
import sys
sys.stdin.reconfigure(encoding='utf-8')
sys.stdout.reconfigure(encoding='utf-8')

TOTAL_RESULTS=0
RESULTS_PER_PAGE=0
# note that without this header, a website may give you a puzzle to solve
my_headers = {'User-Agent': 'Mozilla/5.0'}

"""
#First find total number of results(TOTAL_RESULTS) and number of results per page(RESULTS_PER_PAGE):
url = "https://maharera.maharashtra.gov.in/agents-search-result?agent_name=&agent_project_name=&agent_location=&agent_state=27" + \
    "&agent_division=&agent_district=&page=1&op=Search"
r = requests.get(url, headers=my_headers)

# Ensure the request was successful and parse the content
if r.status_code != 200:
    print("Failed to retrieve the webpage")
    sys.exit()

tree = html.fromstring(r.content)
p_tags= tree.xpath("//p")
print(len(p_tags))
for p in p_tags:
    #print(f"{p.text}")
    #print(p.text_content()) #=>Showing Final 47242 Result
    if "Showing Final" in p.text_content():
        TOTAL_RESULTS = int(p.text_content().split(" ")[2])
        print("TOTAL_RESULTS=",TOTAL_RESULTS)

# Find all table elements
tables = tree.xpath('//table')

for table in tables: #outer for
    # Assuming each table has rows (tr) and cells (th/td)
    rows = table.xpath('.//tr')
    
    for row in rows:
        # Extract data cells
        cells = row.xpath('.//td/text()')
        if cells:
            RESULTS_PER_PAGE +=1
            
#end outer for
#print(RESULTS_PER_PAGE)
#TOTAL_RESULTS=47240
print("Number of pages to scrape:" ,str((TOTAL_RESULTS//RESULTS_PER_PAGE) + 1))
"""

# Now scrape all webpages
#NUM_PAGES_TO_SCRAPE=(TOTAL_RESULTS//RESULTS_PER_PAGE) + 1# This is around 4,742+ pages
NUM_PAGES_TO_SCRAPE=1
agents = []
for page in range(1,NUM_PAGES_TO_SCRAPE+1):
    
    url = "https://maharera.maharashtra.gov.in/agents-search-result?agent_name=&agent_project_name=&agent_location=&agent_state=27" + \
        "&agent_division=&agent_district=&page=" + str(page) + "&op=Search"
    r = requests.get(url, headers=my_headers)

    # Ensure the request was successful and parse the content
    if r.status_code != 200:
        print("Failed to retrieve the webpage")
        sys.exit()

    tree = html.fromstring(r.content)

    # Find all table elements
    tables = tree.xpath('//table')

    for table in tables: #outer for
        # Assuming each table has rows (tr) and cells (th/td)
        rows = table.xpath('.//tr')
        
        for row in rows:
            # Extract headers (assuming they are in the first row)
            #headers = row.xpath('.//th/text()')# Not needed
            #if headers:
            #    print('Headers:', headers)
            
            href='' 
            #print("type(row)=",type(row)) # type(row)= <class 'lxml.html.HtmlElement'>
            for e in row.xpath('.//a'):
                #print(f"{e.tag} - {e.attrib}") #works
                href = e.get("href")
                print("href=",href)
                break # just read href of first a tag
            #end for
            if href == '':
                continue
            print("href=", href)
            
            
            #Now goto the href page and extract contact details:
            response = requests.get(href, headers=my_headers)
            if response.status_code != 200:
                print("Failed to retrieve the webpage")
                sys.exit()
                
            
            #soup = BeautifulSoup(response.content, 'html.parser')
            #print(soup.prettify())
            #s = soup.find_all('div', class_='row')
            #for line in s:
            #    print(line.text)


            
            address_tree = html.fromstring(response.content)
            print("address_tree=",address_tree)
            address_cells = address_tree.xpath("//div[@class='x_content']")
            print("len(address_cells)=",len(address_cells)) # => 2
            
            for parent in address_cells[1]:
                print(f"Parent tag: {parent.tag} - Text: {parent.text}")
                for child in parent:
                    print(f"..Child tag: {child.tag} - Text: {child.text}")
                    for grandchild in child:
                        print(f"....Grandchild tag: {grandchild.tag}, Attribute: {grandchild.attrib}, Text: {grandchild.text}")
            #end for
            
            for e in address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']"):
                print("e.text=",e.text.strip())
            
            print('Block Number:',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[25].strip())
            print('Bldg Name   :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[29].strip())
            print('Street Name :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[33].strip())
            print('Locality    :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[37].strip())
            print('Landmark :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[41].strip())
            print('Division :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[45].strip())
            print('District :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[49].strip())
            print('Taluka :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[55].strip())
            print('Village :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[58].strip())
            print('Pin code :',address_cells[1].xpath("//div[@class='col-md-3 col-sm-3']/text()")[61].strip())
            
            
            
            
            
            
    
                
    
                #print(f"{e.text}")
            
                  
            # Extract data cells
            cells = row.xpath('.//td/text()')# print(len(cells)) works
            if cells:
                print('Row Data:', cells,)
                name, reg_num = cells[1], cells[2]
                agents.append({'name': name, 'reg_num': reg_num})
                break #TODO: just read one record for now. Disable this later
    #end outer for

print("len(agents)=",len(agents))
print("agents=",agents)
