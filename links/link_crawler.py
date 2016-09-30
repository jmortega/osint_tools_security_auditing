#!/usr/bin/env python

# This program is optimized for Python 3.5.

import argparse
import sys
import requests
import re
processed = []

def search_links(url, depth, search):
    # Process http links that are not processed yet
    url_is_processed = (url in processed)
    if (url.startswith("http://") and (not url_is_processed)):
        processed.append(url)
        path = "/"
        urlparts = url.split("/")
        if (len(urlparts) > 1):
            host = urlparts[0]
            path = url.replace(host, "", 1)
    
        # Start crawling
        print("Crawling URL path:%s%s " %(host, path))
        req = requests.get(host+path,verify=False)
        
        # find the links
        contents = req.text
        all_links = re.findall('href="(.*?)"', contents)
        if (search in contents):
            print("Found " + search + " at " + url)
            print("-----------------------------------")
            print(" ==> %s: processing %s links" %(str(depth),str(len(all_links))))
        
            for href in all_links:
                # Find relative urls
                print('link found '+href)
                # Recurse links
                if (depth > 0):
                    search_links(href, depth-1, search)
                else:
                    print("Skipping link: %s ..." %url)
                        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Webpage link crawler')
    parser.add_argument('--url', action="store", dest="url",required=True,type=str)
    parser.add_argument('--query', action="store", dest="query",required=True)
    parser.add_argument('--depth', action="store", dest="depth",default=2)
    given_args = parser.parse_args()
    try:
        if given_args.url.startswith("http://") == True:
            target = given_args.url
        else:   
            target = "http://" + given_args.url
        search_links(target,given_args.depth,given_args.query)
    except KeyboardInterrupt:
        print("Aborting search by user request.")