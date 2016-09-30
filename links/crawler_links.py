import requests
import argparse
import time
import json
import gzip
import csv
import codecs

from bs4 import BeautifulSoup

import sys


# parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d","--domain",required=True,help="The domain to target ie. cnn.com")
args = vars(ap.parse_args())

domain = args['domain']

# list of available indices
#http://index.commoncrawl.org

index_list = ["2016-36"]

#
# Searches the Common Crawl Index for a domain.
#
def search_domain(domain):

    record_list = []
    
    print("[*] Trying target domain: %s" % domain)
    
    for index in index_list:
        
        print("[*] Trying index %s" % index)
        
        cc_url  = "http://index.commoncrawl.org/CC-MAIN-%s-index?" % index
        cc_url += "url=%s&matchType=domain&output=json" % domain
        print(cc_url)
        response = requests.get(cc_url)
        
        if response.status_code == 200:
            
            records = response.content.splitlines()
            
            for record in records:
                record_list.append(json.loads(record.decode('utf-8')))
            
            print("[*] Added %d results." % len(records))
            
    
    print("[*] Found a total of %d hits." % len(record_list))
    
    return record_list

#
# Download Page
#
def download_page(url):

    response = requests.get('http://'+url)
    
    print(response)
  
    return response.text

#
# Extract links from the HTML  
#
def extract_external_links(html_content,link_list):

    try:
        parser = BeautifulSoup(html_content,'html.parser')

        links = parser.find_all("a")

        if links:
        
            for link in links:
                href = link.attrs.get("href")
            
                if href is not None:
                
                    if domain not in href:
                        if href not in link_list and href.startswith("http"):
                            print("[*] Discovered external link: %s" % href)
                            link_list.append(href)

        return link_list
    
    except Exception as e:
        print(e)
        pass



record_list = [domain]
link_list   = []
search_domain_list   = []

for record in record_list:
    
    html_content = download_page(record)
    
    print("[*] Retrieved %d bytes for %s" % (len(html_content),record))
    
    link_list = extract_external_links(html_content.encode('ascii', 'ignore'),link_list)
    

print("[*] Total external links discovered: %d" % len(link_list))

with codecs.open("%s-links.csv" % domain,"w",encoding="utf-8") as output:

    fields = ["URL"]
    
    logger = csv.DictWriter(output,fieldnames=fields)
    logger.writeheader()
    
    for link in link_list:
        logger.writerow({"URL":link})
        
    search_domain_list = search_domain(domain)

    for link in search_domain_list:
        logger.writerow({"URL":link['url']})
