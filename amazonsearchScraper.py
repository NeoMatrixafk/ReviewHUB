import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from requests_html import HTMLSession, HTML
from typing import List, Tuple, Any, Dict


class amazonScraper:

    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                          'AppleWebKit/ 537.36 (KHTML, like Gecko) '
                          'Chrome/116.0.0.0 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }
        with open('amazon_search_url.txt', 'r') as file:
            self.search_url = file.read()
        self.base_url = f'https://www.amazon.in'
        self.base_backurl = f'ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber='
        self.session = HTMLSession()
        options = Options()
        options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=options)

    def iterate_over_search(self) -> List[dict]:
        searchProducts = []
        self.driver.get(self.search_url)
        time.sleep(2)
        page_content = HTML(html=self.driver.page_source)
        if self.has_products(page_content):
            newsearchProducts = self.get_products_from_search(page_content)
            print("New Product Found!")
            print(newsearchProducts)
            searchProducts += newsearchProducts
        else:
            print("No Products Found!")

        return searchProducts

    def has_products(self, page_content: HTML) -> bool:
        if page_content.find('div[data-component-type=s-search-result]'):
            return True
        return False

    def get_products_from_search(self, page_content: int) -> list[dict[str, Any]]:
        searchProducts = []
        for tag in page_content.find('div[data-component-type=s-search-result]'):
            name = tag.find('div > div > div.puis-card-container > div > div > div:nth-child(2) > div > div > div:nth-child(1) > h2 > a > span', first=True).text
            imagelink = tag.find('div > div > div.puis-card-container > div > div > div > div >div:nth-child(2) > div > span > a > div > img', first=True).attrs['src']
            ogproductlink = tag.find('div > div > div.puis-card-container > div > div > div > div >div:nth-child(2) > div > span > a', first=True).attrs['href']
            second_slash_index = ogproductlink.find('/', ogproductlink.find('/') + 1)
            og1productlink = ogproductlink[:second_slash_index] + "/product-reviews" + ogproductlink[second_slash_index + 3:]
            productlink = self.base_url + og1productlink + self.base_backurl

            searchProducts.append({

                'Product Name': name,
                'Image Link': imagelink,
                'Product Link': productlink


            })

        return searchProducts


if __name__ == '__main__':

    scraper = amazonScraper()
    all_products = scraper.iterate_over_search()
    print("Search List updated.")

    with open('amazonproducts.json', 'w') as f:
        json.dump(all_products, f)
