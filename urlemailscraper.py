import requests
import urllib.request
from bs4 import BeautifulSoup as bs
import json
import os
from lxml import html
from flask import Flask, render_template, request, jsonify
import re
from selenium import webdriver

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html')

@app.route("/output", methods=["POST"])
def output():
    domains=request.form['url']
    
    return render_template('output.html', emails = logic(domains))

@app.route("/api", methods=['GET'])
def api():
    domains=request.args.get('domain')
    apikey=request.args.get('apikey')
    if apikey is None:
        return jsonify("Invalid Response", "Make sure API key is present!")
    else:
        return jsonify(logic(domains))

def logic(domains):
    chrome_options = webdriver.ChromeOptions()
    chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-dev-shm-usage")
    chrome_options.add_argument("--no-sandbox")
    driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    emails1=[]
    if ',' in domains:
        domains1=domains.split(',')
        for domain in domains1:
            driver.get(str(domain))
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
            for email in emails:
                emails1.append(email)
    else:
        domains1 = domains
        driver.get(str(domains1))
        emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
        for email in emails:
            emails1.append(email)
  
    return emails1

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
