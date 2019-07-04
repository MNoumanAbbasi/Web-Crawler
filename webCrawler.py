#           author: Muhammad Nouman Abbasi
import os
import time
import requests
from bs4 import BeautifulSoup

# HELPER FUNCTIONS                        
def getDomainName(url):     # Extracts the domain from URL
    if "www." in url:
        return url.split("www.")[-1].split("/")[0]
    else:
        return url.split("://")[-1].split("/")[0]

def addSlashAtEnd(url):     # Adds / in end of link if not already
    if url[-1] != '/':
        return url + '/'
    else:
        return url

website = input("Enter the url to crawl: ")
website = addSlashAtEnd(website)
domain = getDomainName(website)
print("\nDomain: " + domain)
urls_crawled = []       # list storing webpages already crawled so no webpage gets crawaled twice
num_of_webpages_crawled = 0


def crawlWebsite(url):
    global num_of_webpages_crawled
    url = addSlashAtEnd(url)
    # print("Checking " + url)
    # BASE CASE FOR RECURSION
    if domain not in url:   # if url is not of the same website
        return
    if url in urls_crawled: # if webpage already crawled
        return

    # Getting the website
    print("Downloading webpage...\t" + url)
    try:
        r = requests.get(url)
    except requests.exceptions.RequestException as e:
        print(e, "\n\nIn short: Connection error. The program will now exit.")
        time.sleep(3)
        os._exit(1)

    # Writing to html file
    # outFile_name = r.url.split("/")[-2] + '.html'    # replacing \ in name (\ causes errors in name)
    outFile_name = str(num_of_webpages_crawled) + '.html'
    with open(outFile_name, "w", encoding="utf-8") as outFile:
        outFile.write(r.text)
    # Adding current url to list of urls_crawled
    urls_crawled.append(url)
    num_of_webpages_crawled += 1
    
    # Analyzing the webpage for more links
    soup = BeautifulSoup(r.text, 'html.parser')
    links = soup.find_all('a')           # Storing all links
    for link in links:
        result = link.get('href')
        if isinstance(result, str):         # if link is in fact a url (str) (error handling)
            # print('URLL:  ' + result)
            if "#" in result:
                result = website
            if '../' in result:             # removes unnecessary ../ 
                result = result.replace('../', '')
            if result == '/' or result == '#':  # removes unnecessary / and # links
                result = website
            if 'javascript:' in result or 'mailto:' in result:  # removes inline scripts links
                result = website
            if result[0] == '/':              # removes unnecessary //
                result = result[1:]
            if '://' not in result:         # internal link (without http://)
                result = website + result

            crawlWebsite(result)
    # End of for loop

 # MAIN
crawlWebsite(website)
print("ALL URLS CRAWLED")
for url in urls_crawled:
    print(url)
print("\nTotal number of URLS Crawled: " + str(num_of_webpages_crawled))
