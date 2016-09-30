#!/usr/bin/env python

# encoding=utf8
import sys

import argparse
import json
import os
import logging
import requests
import re

def StripTags(text):
    finished = 0
    while not finished:
        finished = 1
        start = text.find("<")
        if start >= 0:
            stop = text[start:].find(">")
            if stop >= 0:
                text = text[:start] + text[start+stop+1:]
                finished = 0
    return text

def getemails(domain):
    page_counter = 0
    try:
        while page_counter < 50 :
            results = 'http://www.google.com/search?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
            response = requests.get(results)
            text = response.text
            emails = (re.findall('([\w\.\-]+@'+domain+')',StripTags(text)))
            for email in emails:
                print(email)
            page_counter = page_counter +10
    except IOError:
        print ("Cannot connect to Google Web.")
        
    try:
        while page_counter < 50 :
            results = 'http://groups.google.com/groups?q='+str(domain)+'&hl=en&lr=&ie=UTF-8&start=' + repr(page_counter) + '&sa=N'
            response = requests.get(results)
            text = response.text
            emails = (re.findall('([\w\.\-]+@'+domain+')',StripTags(text)))
            for email in emails:
                print(email)
            page_counter = page_counter +10
    except IOError:
        print ("Cannot connect to Google Groups.")         


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Makes a search on google groups.', prog='checkFullContactAPI.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved by google groups.')        
    args = parser.parse_args()        
    getemails(args.domain)