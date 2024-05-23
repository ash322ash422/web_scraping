from lxml import etree
import cssselect

html_data = '''
<div id="root">
  <div id="products">
    <div class="product">
      <div id="product_name">Dark Red Energy Potion</div>
      <div id="product_price">$4.99</div>
      <div id="product_rate">4.7</div>
      <div id="product_description">Bring out the best in your gaming performance.</div>
    </div>
  </div>
</div>
'''

# Parse the HTML data using lxml
root = etree.fromstring(html_data)

# Navigate through the document
for parent in root:
    print(f"Parent tag: {parent.tag}")
    for child in parent:
        print(f"Child tag: {child.tag}")
        for grandchild in child:
            print(f"Grandchild tag: {grandchild.tag}, Attribute: {grandchild.attrib}, Text: {grandchild.text}")

print("################################################")

html_data = '<div type="product_rate" review_count="774">4.7</div>'

# Parse the HTML data using lxml
element = etree.fromstring(html_data)

# Get a specific attribute value
print(element.get("review_count")) # output=> "774"
print("------------------------------------------------")
html_data = '''
<div id="products">
  <div class="product">
    <div id="product_name">Dark Red Energy Potion</div>
    <div class="pricing">
      <div>Price with discount: $4.99</div>
      <div>Price without discount: $11.99</div>
    </div>
    <div id="product_rate" review_count="774">4.7 out of 5</div>
    <div id="product_description">Bring out the best in your gaming performance.</div>
  </div>
</div>
'''

# Parse the HTML data using lxml
root = etree.fromstring(html_data)

# Iterate over the product div elements 
for element in root.xpath("//div/div//div"):
    print(element.text)

print("**********************************************")
html_data = '''
<div id="products">
  <div class="product">
    <div id="product_name">Dark Red Energy Potion</div>
    <div class="pricing">
      <div>Price with discount: $4.99</div>
      <div>Price without discount: $11.99</div>
    </div>
    <div id="product_rate" review_count="774">4.7 out of 5</div>
    <div id="product_description">Bring out the best in your gaming performance.</div>
  </div>
</div>
'''

# Parse the HTML data using lxml
root = etree.fromstring(html_data)

# parse elements
name = root.xpath("//div[@id='product_name']/text()")[0]
discount_price = root.xpath("//div[contains(text(), 'with discount')]/text()")[0]
review_count = root.xpath("//div[@id='product_rate']/@review_count")[0]
desc = root.xpath("//div/div/div[4]/text()")[0]
print("name=",name,"; discount_price=",discount_price,"; review_count=",review_count,"; desc=",desc)
print("%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%")

html_data = '''
<div id="products">
  <div class="product">
    <div id="product_name">Dark Red Energy Potion</div>
    <div class="pricing">
      <div>Price with discount: $4.99</div>
      <div>Price without discount: $11.99</div>
    </div>
    <div id="product_rate" review_count="774">4.7 out of 5</div>
    <div id="product_description">Bring out the best in your gaming performance.</div>
  </div>
</div>
'''

# Parse the HTML data using lxml
root = etree.fromstring(html_data)

# get all the div elements
div_elements = root.cssselect("div div div")

# match by a specific text value
discount_price = [element for element in div_elements if "without discount" in element.text][0].text
print("discount_price=", discount_price)

# match by an attribute value
rate = [element for element in div_elements if element.get("id") == "product_rate"][0].text
print("rate=",rate)

"""
Parent tag: div
Child tag: div
Grandchild tag: div, Attribute: {'id': 'product_name'}, Text: Dark Red Energy Potion
Grandchild tag: div, Attribute: {'id': 'product_price'}, Text: $4.99
Grandchild tag: div, Attribute: {'id': 'product_rate'}, Text: 4.7
Grandchild tag: div, Attribute: {'id': 'product_description'}, Text: Bring out the best in your gaming performance.
################################################
774
------------------------------------------------
Dark Red Energy Potion


Price with discount: $4.99
Price without discount: $11.99
4.7 out of 5
Bring out the best in your gaming performance.
**********************************************
name= Dark Red Energy Potion ; discount_price= Price with discount: $4.99 ; review_count= 774 ; desc= Bring out the best in your gaming performance.
%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
discount_price= Price without discount: $11.99
rate= 4.7 out of 5

"""