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
        self.pages = 3
        with open('flipkart_product_link.txt', 'r') as file:
            self.search_url = file.read()
        self.session = HTMLSession()

    def iterate_over_pages(self) -> List[dict]:
        reviews = []
        for i in range(1, self.pages + 1):
            print(f"Page: {i}")
            r = self.session.get(f'{self.search_url}&page={i}', headers=self.headers)
            if self.has_reviews(r.html):
                new_reviews = self.get_reviews_from_page(r.html)
                print("New reviews!")
                print(new_reviews)
                reviews += new_reviews
            else:
                print("No reviews!")

        return reviews

    def has_reviews(self, page_content: HTML) -> bool:
        if page_content.find('div._1AtVbE > div._27M-vq'):
            return True
        return False

    def get_reviews_from_page(self, page_content: int) -> list[dict[str, Any]]:

        reviews = []

        for tag in page_content.find('div._1AtVbE > div._27M-vq'):
            user = tag.find('p._2V5EHH', first=True).text
            title = tag.find('p._2-N8zT', first=True).text
            date = tag.find('div._3n8db9 > div > p:nth-child(5)', first=True).text
            review = tag.find('div.t-ZTKy > div > div', first=True).text

            reviews.append({
                'user': user,
                'title': title,
                'date': date,
                'review': review
            })

        return reviews


if __name__ == '__main__':

    scraper = flipkartScraper()
    all_reviews = scraper.iterate_over_pages()
    print("Search List Updated.")

    with open('templates/flipkartData.json', 'w') as f:
        json.dump(all_reviews, f)

