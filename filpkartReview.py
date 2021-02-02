import  requests
from bs4 import BeautifulSoup as bs
from urllib.request import  urlopen as ureq

searchString=""
def getFLipkartpage(url):
    try:
        page = ureq(url).read()

        return page
    except Exception as e:
        raise Exception("Not able to retrive flipkart page")


def getBigBoxes(html_page):
    try:
        boxes = html_page.find_all("a", {"class": "IRpwTa"})
        if len(boxes) > 0:
            return boxes
        else:
            raise Exception("no boxes found to search for comment")
    except Exception as e:
        raise Exception("Exception occured in getBigBoxesfunction" + str(e))


def generateURLForProduct(boxes):
    try:
        url_list = []

        for i in boxes:
            productLink = "https://www.flipkart.com" + i["href"]
            product_link = productLink.replace('/p/', '/product-reviews/')
            l = len("marketplace=FLIPKART")
            end_index = product_link.find("marketplace=FLIPKART") + l
            url_list.append(product_link[:end_index] + '&page=')
        return url_list
    except Exception as e:
        if len(url_list) > 0:
            return url_list
        else:
            raise Exception("not able to generate URL for product" + str(e))


def getFeebackofProduct(url):
    loop_time = 6
    i = 1
    isPageNoCalculated = False
    feedback = []
    while i < loop_time:
        prodRes = requests.get(url + str(i))
        i = i + 1
        # print(prodRes.text)
        prod_html = bs(prodRes.text, "html.parser")
        res = prod_html.find_all('div', {'class': '_6K-7Co'})
        rating = prod_html.find_all('div', {'class': '_3LWZlK _1BLPMq _3B8WaH'})
        name = prod_html.find_all('p', {'class': '_2sc7ZR _2V5EHH _1QgsS5'})

        product_name = prod_html.find_all('div', {'class': '_2s4DIt _1PEOhe'})
        if len(product_name) > 0:
            product_name = product_name[0].text
        page_no = prod_html.find_all('div', {'class': '_2MImiq _1Qnn1K'})
        if len(page_no) > 0 and isPageNoCalculated == False:
            page_detail = page_no[0].span.text
            loop_time = int(page_detail[page_detail.index("of ") + 3:])
            isPageNoCalculated = True
            if loop_time > 10:
                loop_time = 10
            print(loop_time)
        for r in range(0, min([len(res), len(rating)])):
            feedback.append(
                {"rating": rating[r].text, "comment": res[r].text, "name": name[r].text, "product Name": product_name,
                 "product searched": searchString})
    return feedback


def feedback(product_name):
    global searchString
    searchString=product_name
    flipkart_url = "https://www.flipkart.com/search?q=" + product_name
    flipkart_page = getFLipkartpage(flipkart_url)
    flipkart_html = bs(flipkart_page, "html.parser")
    bigboxes = getBigBoxes(flipkart_html)
    urls = generateURLForProduct(bigboxes)
    return getFeebackofProduct(urls[0])

