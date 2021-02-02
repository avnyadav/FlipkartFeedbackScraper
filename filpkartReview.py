import requests
from bs4 import BeautifulSoup as bs
from urllib.request import urlopen as ureq

def feedback(product_name):
    searchString=product_name
    response = []
    flipkart_url = "https://www.flipkart.com/search?q=" + searchString
    uClient = ureq(flipkart_url)
    flipkart_page = uClient.read()
    uClient.close()
    flipkart_html = bs(flipkart_page, "html.parser")
    bigboxes = flipkart_html.findAll("div", {"class": "_2pi5LC col-12-12"})
    for i in range(3, 9):
        productLink = "https://www.flipkart.com" + bigboxes[i].div.div.div.a['href']
        product_link = productLink.replace('/p/', '/product-reviews/')
        l = len("marketplace=FLIPKART")
        end_index = product_link.find("marketplace=FLIPKART") + l
        pl = []

        for i in range(1, 6):
            pl.append(product_link[:end_index] + '&page=' + str(i))
        loop_time = 6
        i = 0
        isPageNoCalculated = False
        while i < loop_time:
            prodRes = requests.get(product_link[:end_index] + '&page=' + str(i))
            i = i + 1
            prod_html = bs(prodRes.text, "html.parser")
            res = prod_html.find_all('div', {'class': '_6K-7Co'})
            rating = prod_html.find_all('div', {'class': '_3LWZlK _1BLPMq _3B8WaH'})
            name = prod_html.find_all('p', {'class': '_2sc7ZR _2V5EHH _1QgsS5'})
            product_name = prod_html.find_all('div', {'class': '_2s4DIt _1PEOhe'})[0].text
            page_no = prod_html.find_all('div', {'class': '_2MImiq _1Qnn1K'})
            if len(page_no) > 0 and isPageNoCalculated == False:
                page_detail = page_no[0].span.text
                loop_time = int(page_detail[page_detail.index("of ") + 3:])
                isPageNoCalculated = True
            for r in range(0, min([len(res), len(rating)])):
                response.append(
                    {"rating": rating[r].text, "comment": res[r].text, "name": name[r].text, "product Name": product_name,
                    "product searched": searchString})
    return response






