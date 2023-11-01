from flask import Flask, render_template, request, redirect
import subprocess
import webbrowser
from flask_cors import CORS


app = Flask(__name__, template_folder='templates')
CORS(app)


@app.route('/flipkart_search', methods=['GET', 'POST'])
def getFlipkartSearchTerm():
    if request.method == 'POST':
        if 'flipkart_search_query' in request.form:
            flipkart_query = request.form['flipkart_search_query'].strip()
            search_term = flipkart_query.replace(' ', '+')
            search_url = f'https://www.flipkart.com/search?q={search_term}'
            with open('flipkart_search_url.txt', 'w') as file:
                file.write(search_url)
            subprocess.call(['python', 'flipkartsearchScraper.py'])

    return redirect('http://localhost:63342/MiniProject/flipkart_search_list.html')


@app.route('/flipkart_save_product_link', methods=['POST'])
def flipkart_save_product_link():
    if request.method == 'POST':
        data = request.get_json()
        product_link = data.get('productLink')

        with open('flipkart_product_link.txt', 'w') as file:
            file.write(product_link)

        subprocess.call(['python', 'flipkartreviewScraper.py'])
        webbrowser.open('http://localhost:63342/MiniProject/templates/flipkart_reviews_list.html')

    return redirect('http://localhost:63342/MiniProject/flipkart_search_list.html')


@app.route('/amazon_search', methods=['GET', 'POST'])
def getAmazonSearchTerm():
    if request.method == 'POST':
        if 'amazon_search_query' in request.form:
            amazon_query = request.form['amazon_search_query'].strip()
            search_term = amazon_query.replace(' ', '+')
            search_url = f'https://www.amazon.in/s?k={search_term}'
            with open('amazon_search_url.txt', 'w') as file:
                file.write(search_url)
            subprocess.call(['python', 'amazonsearchScraper.py'])

    return redirect('http://localhost:63342/MiniProject/amazon_search_list.html')


@app.route('/amazon_save_product_link', methods=['POST'])
def amazon_save_product_link():
    if request.method == 'POST':
        data = request.get_json()
        product_link = data.get('productLink')

        with open('amazon_product_link.txt', 'w') as file:
            file.write(product_link)

        subprocess.call(['python', 'amazonScraper.py'])
        webbrowser.open('http://localhost:63342/MiniProject/templates/amazon_reviews_list.html')

    return redirect('http://localhost:63342/MiniProject/amazon_search_list.html')


if __name__ == '__main__':
    app.run(debug=True)
