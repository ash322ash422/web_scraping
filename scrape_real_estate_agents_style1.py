from lxml import html
import requests
import pprint, sys
from random import randint 
from time import sleep 

#NOTE: For some reason this program ios not picking 7th, 14th, 29th,etc records. Fix it.
MAX_NUM_OF_RECORDS_TO_READ=8 #For testing only. I keep this low like 1 to 10
NUM_OF_PAGES_TO_SCRAPE=1
# note that without this header, a website may give you a puzzle to solve
#my_headers = {'User-Agent': 'Mozilla/5.0'}
my_headers = {
        "Accept-Language": "en-US,en;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36",
    }

def get_num_of_pages_to_scrape():
    total_results=0
    results_per_page=0

    #First find total number of results(TOTAL_RESULTS) and number of results per page(RESULTS_PER_PAGE):
    url = "https://maharera.maharashtra.gov.in/agents-search-result"
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
            total_results = int(p.text_content().split(" ")[2])
            print("total_results=",total_results)

    # Find all table elements
    tables = tree.xpath('//table')

    for table in tables: #outer for
        # Assuming each table has rows (tr) and cells (th/td)
        rows = table.xpath('.//tr')
        
        for row in rows:
            # Extract data cells
            cells = row.xpath('.//td/text()')
            if cells:
                results_per_page +=1
                
    #end outer for
    #TOTAL_RESULTS=47240
    print("Number of pages to scrape:" ,str((total_results//results_per_page) + 1))
    return (total_results//results_per_page) + 1# This is around 4,742+ pages
##################end def############################################

def get_scraped_data(num_of_pages_to_scrape):
    data = []
    counter_16 = 0; counter_19 = 0 #count the records that have different style of div in their address
    num_records = 0
    # Now scrape all webpages
    for page in range(1,num_of_pages_to_scrape+1):
        
        sleep(randint(2,10)) #sleep for random seconds to prevent from getting blocked
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

                # Extract data cells
                cells = row.xpath('.//td/text()')# print(len(cells)) works
                print("len(cells)=",len(cells))
                if cells:
                    print('Row Data:', cells,)
                    name, reg_num = cells[1], cells[2]
                    print("Found name:",name)
                    #data.append({'name': name, 'reg_num': reg_num})
                
                href='' 
                #print("type(row)=",type(row)) # type(row)= <class 'lxml.html.HtmlElement'>
                for e in row.xpath('.//a'):
                    #print(f"{e.tag} - {e.attrib}") #works
                    href = e.get("href")
                    #print("href=",href)
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
                
                
                address_tree = html.fromstring(response.content)
                print("address_tree=",address_tree)
                address_cells = address_tree.xpath("//div[@class='row']")
                print("len(address_cells)=",len(address_cells)) 
                num_records +=1
                
                if len(address_cells) == 16: #some recorde have these
                    counter_16 +=1
                    idx_to_use = 1
                    print("Adding name=",name)
                    
                    #for i in range(1,16):
                    #    for j in  range(0,70):
                    #        print("i=",i,";j=",j,";",address_cells[i].xpath("//div[@class='col-md-3 col-sm-3']/text()")[j].strip())
                        
                    #for j in  range(0,70):
                    #    print("j=",j,";",address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[j].strip())
                        
                    block_number= address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[25].strip()
                    bldg_name = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[29].strip()
                    street_name = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[33].strip()
                    locality = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[37].strip()
                    landmark = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[41].strip()
                    state = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[45].strip()
                    division = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[49].strip()
                    district = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[52].strip()
                    taluka = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[55].strip()
                    village = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[58].strip()
                    zip = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[61].strip()
                    tel = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[65].strip()
                    website = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[69].strip()
                    
                    data.append({
                        'debug_type': str(num_records)+': counter_16',
                        'name': name,
                        'reg_num': reg_num,
                        'block_number': block_number,
                        'bldg_name' : bldg_name,
                        'street_name' : street_name,
                        'locality' : locality,
                        'landmark' : landmark,
                        'state' : state,
                        'division' : division,
                        'district' : district,
                        'taluka' : taluka,
                        'village' : village,
                        'zip' : zip,
                        'tel' : tel,
                        'website' : website,
                    })
                    

                elif len(address_cells) == 19: #some recorde have these
                    counter_19 +=1
                    idx_to_use = 1
                    print("Adding name=",name)
                    #for i in range(1,16):
                    #       print("i=",i,";j=",j,";",address_cells[i].xpath("//div[@class='col-md-3 col-sm-3']/text()")[j].strip())
                    #for j in  range(0,80):
                    #    print("j=",j,";",address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[j].strip())
                            
                    block_number= address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[37].strip()
                    bldg_name = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[41].strip()
                    street_name = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[45].strip()
                    locality = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[49].strip()
                    landmark = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[53].strip()
                    state = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[57].strip()
                    division = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[60].strip()
                    district = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[63].strip()
                    taluka = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[66].strip()
                    village = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[69].strip()
                    zip = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[72].strip()
                    tel = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[76].strip()
                    website = address_cells[idx_to_use].xpath("//div[@class='col-md-3 col-sm-3']/text()")[79].strip()
                    
                    data.append({
                        'debug_type': str(num_records)+': counter_19',
                        'name': name,
                        'reg_num': reg_num,
                        'block_number': block_number,
                        'bldg_name' : bldg_name,
                        'street_name' : street_name,
                        'locality' : locality,
                        'landmark' : landmark,
                        'state' : state,
                        'division' : division,
                        'district' : district,
                        'taluka' : taluka,
                        'village' : village,
                        'zip' : zip,
                        'tel' : tel,
                        'website' : website,
                    })
                    
                else: #should never reach here
                    sys.exit()
                
                
                if len(data) == MAX_NUM_OF_RECORDS_TO_READ:
                    break
                print("############################PROCESSING NEXT RECORD########################")
            #end inner for
            
    #end outer for        

    print("******counter_16=",counter_16,"; counter_19=",counter_19)
    return data
#end def
            
if __name__=='__main__':
    num_of_pages_to_scrape = get_num_of_pages_to_scrape() #This is around 4,742+ pages
    print("num_of_pages_to_scrape=",num_of_pages_to_scrape)
    
    data = get_scraped_data(num_of_pages_to_scrape=NUM_OF_PAGES_TO_SCRAPE) #TODO During production change this.
    print("len(data)=",len(data))
    pprint.pp(data)
    
                
            
            
            
            
    
                

