import json
from requests_html import HTMLSession, HTML
from typing import List, Tuple, Any, Dict


class flipkartScraper:

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
        with open('flipkart_search_url.txt', 'r') as file:
            self.search_url = file.read()
        self.session = HTMLSession()

    def iterate_over_search(self) -> List[dict]:
        searchProducts = []
        r = self.session.get(f'{self.search_url}', headers=self.headers)
        if self.has_products(r.html):
            newsearchProducts = self.get_products_from_search(r.html)
            print("New Product Found!")
            print(newsearchProducts)
            searchProducts += newsearchProducts
        else:
            print("No Products Found!")

        return searchProducts

    def has_products(self, page_content: HTML) -> bool:
        if page_content.find('div._13oc-S'):
            return True
        return False

    def get_products_from_search(self, page_content: int) -> list[dict[str, Any]]:
        searchProducts = []
        for tag in page_content.find('div._13oc-S'):
            name = tag.find('div.CXW8mj > img', first=True).attrs['alt']
            link = tag.find('div.CXW8mj > img', first=True).attrs['src']
            productlink = tag.find('a._1fQZEK', first=True).attrs['href']
            ogproductlink = "https://www.flipkart.com" + productlink
            index = ogproductlink.find("FLIPKART")
            if index != -1:
                shorturl = ogproductlink[:index + len("FLIPKART")]
            else:
                shorturl = ogproductlink

            parts = shorturl.split("/")
            if len(parts) >= 5:
                parts[4] = parts[4].replace("p", "product-reviews")
                newproductlink = "/".join(parts)
            else:
                newproductlink = shorturl

            print(newproductlink)

            searchProducts.append({

                'Product Name': name,
                'Image Link': link,
                'Product Link': newproductlink

            })

        return searchProducts


if __name__ == '__main__':

    scraper = flipkartScraper()
    all_products = scraper.iterate_over_search()
    print("Search List updated.")

    with open('flipkartproducts.json', 'w') as f:
        json.dump(all_products, f)
