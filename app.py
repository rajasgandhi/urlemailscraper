import requests
import os
from flask import Flask, render_template, request, jsonify
import re
from requests_html import AsyncHTMLSession
import asyncio
from pyppeteer import launch

app = Flask(__name__)

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

def logic(urls):
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
    else:
    domain = str(domains)
    if (domain.startswith("https://")):
        domain = "http://" + domain[7:]
    if (not domain.startswith("http://")):
        domain = "http://" + domain
    driver.get(domain)
    emails = re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", driver.find_element_by_tag_name('body').text)
  
    return emails'''

    url = str(urls)
    '''if (url.startswith("https://")):
        url = "http://" + url[7:]
    if (not url.startswith("http://")):
        url = "http://" + url'''
    
    new_loop=asyncio.new_event_loop()
    asyncio.set_event_loop(new_loop)
    session = AsyncHTMLSession()
    browser = await launch() 
        '''ignoreHTTPSErrors':True, 
        'headless':True, 
        'handleSIGINT':False, 
        'handleSIGTERM':False, 
        'handleSIGHUP':False
    )'''
    session._browser = browser
    resp_page = await session.get(url)
    await resp_page.html.arender()
    return re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", resp_page.html.html)
    

    '''r = session.get("http://profoundbiz.com/contact")
    #session.browser
    r.html.render()
    return re.findall("([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)", r.html.html)'''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=os.environ.get('PORT', 5000))
