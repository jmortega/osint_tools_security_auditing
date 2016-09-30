#!/usr/bin/env python

import sys

import argparse
import json
import os
import logging
import requests
import re


def google_linkedin_page(name):
    """
    Uses a google query to find a possible LinkedIn page related to name (usually self.domain)
    Google query is "site:linkedin.com/company name", and first result is used
    """
    request = 'http://google.com/search?num=10&q=site:linkedin.com/company%20"' + name + '"'
    
    try:
        google_search = requests.get(request)
        google_results = re.findall('<cite>(.+?)<\/cite>', google_search.text)
        for url in google_results:
            if 'linkedin.com/company/' in url:
                return re.sub('<.*?>', '', url)

    except requests.ConnectionError as e:
        logging.warning(e)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses a google query to find a possible LinkedIn page related to name.', prog='checkLinkedLinProfile.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved.')        
    args = parser.parse_args()       
    
    print(google_linkedin_page(args.domain))
