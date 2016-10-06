import os
import logging
import requests
import re
import argparse

def get_place(place):
       api_key = 'a82ad9009f6b1b1'
       base_url = 'https://api.fullcontact.com/v2/address/locationEnrichment.json'
       payload = {'place':place, 'apiKey':api_key}
       resp = requests.get(base_url, params=payload)
       
       if resp.status_code == 200:
	      
	      print(resp.text.encode('ascii', 'ignore'))
	      f = open('place.json','w')
	      f.write(resp.text.encode('ascii', 'ignore'))              

if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Makes a search on fullcontact api.', prog='checkLocationByPlace.py', epilog="", add_help=False)
       # Adding the main options
       parser.add_argument('-p', '--place', metavar='<place>', action='store', help='query to be resolved by fullcontact.com.')
       args = parser.parse_args()        
       get_place(args.place)