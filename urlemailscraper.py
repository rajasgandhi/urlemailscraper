import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import json
import os
from lxml import html
from flask import Flask, render_template, request
import re
from selenium import webdriver

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html')

@app.route("/output", methods=["POST"])
def output():
    '''user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

    session_requests = requests.session()

    result = session_requests.get(request.form['url'], headers={'User-Agent': user_agent})
    tree = html.fromstring(result.text)

    soup = bs(result.text, "html.parser")

    text = soup.text

    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", text)'''
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get(request.form['url'])

    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)

    return render_template('output.html', emails = emails)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))