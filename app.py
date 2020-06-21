import requests
import os
from flask import Flask, render_template, request, jsonify
import re
from selenium import webdriver

app = Flask(__name__)

chrome_options = webdriver.ChromeOptions()
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")

@app.route("/")
@app.route("/index")
def main():
    return render_template('index.html')

@app.route("/output", methods=["POST"])
def output():
    domains=request.form['url']
    
    return render_template('output.html', emails = logic(domains), length=(len(logic(domains)) != 0))

@app.route("/api", methods=['GET'])
def api():
    domains=request.args.get('url')
    apikey=request.args.get('apikey')
    if apikey is None:
        return jsonify("Invalid Response", "Make sure API key is present!")
    else:
        return jsonify(logic(domains))

def logic(domains):
    driver=webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"),chrome_options=chrome_options)
    '''if ',' in domains:
        domains1=domains.split(',')
        for domain in domains1:
            domain = str(domain)
            if (domain.startswith("https://")):
                domain = "http://" + domain[7:]
            if (not domain.startswith("http://")):
                domain = "http://" + domain
            driver.get(domain)
            emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
            return emails
    else:'''
    domain = str(domains)
    if (domain.startswith("https://")):
        domain = "http://" + domain[7:]
    if (not domain.startswith("http://")):
        domain = "http://" + domain
    driver.get(domain)
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
  
    return emails

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
