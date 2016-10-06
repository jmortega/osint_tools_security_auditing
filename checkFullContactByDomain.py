#!/usr/bin/env python

import sys

import argparse
import json
import os
import logging
import requests
import re
import argparse

def get_fullcontact(domain,json):
       api_key = 'a82ad9009f6b1b1'
       base_url = 'https://api.fullcontact.com/v2/company/lookup.json'
       payload = {'domain':domain, 'apiKey':api_key}
       resp = requests.get(base_url, params=payload)
       
       if resp.status_code == 200:
	      
	      print(resp.text.encode('ascii', 'ignore'))
	      
	      if json is not None:
		     f = open(json,'w')
		     f.write(resp.text.encode('ascii', 'ignore'))              




if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Makes a search on fullcontact api.', prog='checkFullContactByDomain.py', epilog="", add_help=False)
       # Adding the main options
       parser.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved by fullcontact.com.')
       parser.add_argument('-j', '--json', metavar='<json>', action='store', help='save results in json file.',required=False)  
       args = parser.parse_args()        
       get_fullcontact(args.domain,args.json)