#!/usr/bin/env python

import sys

import argparse
import json
import os
import logging
import requests
import re

def get_fullcontact(email,json):
       api_key = 'a82ad9009f6b1b1'
       base_url = 'https://api.fullcontact.com/v2/person.json'
       payload = {'email':email, 'apiKey':api_key}
       resp = requests.get(base_url, params=payload)
       
       if json is not None:
	      f = open(json,'w')
	      f.write(resp.text.encode('ascii', 'ignore'))              

       if resp.status_code == 200:
              # parse contact information
              if 'contactInfo' in resp.json():
                     try:
                            first_name = resp.json()['contactInfo']['givenName']
                            last_name = resp.json()['contactInfo']['familyName']
                            middle_name = None
                     except KeyError:
                            first_name, middle_name, last_name = self.parse_name(resp.json()['contactInfo']['fullName'])
                     
                     name = ' '.join([x for x in (first_name, middle_name, last_name) if x])
                     print('%s - %s' % (name, email))
                     # parse company information for title
                     title = None
                     if 'organizations' in resp.json():
                            for occupation in resp.json()['organizations']:
                                   if 'current' in occupation:
                                          if 'title' in occupation:
                                                 title = '%s at %s' % (occupation['title'], occupation['name'])
                                   else:
                                          title = 'Employee at %s' % occupation['name']
                                   print(title)
                     # parse demographics for region
                     region = None
                     if 'demographics' in resp.json() and 'locationGeneral' in resp.json()['demographics']:
                            region = resp.json()['demographics']['locationGeneral']
                            print(region)
                     # parse profile information
                     if 'socialProfiles' in resp.json():
                            for profile in resp.json()['socialProfiles']:
                            # set the username to 'username' or 'id' and default to email if they are unknown
                                   username = email
                                   for key in ['username', 'id']:
                                          if key in profile:
                                                 username = profile[key]
                                                 break
                                   resource = profile['typeName']
                                   url = profile['url']
                                   print('%s - %s' % (resource, url))
                     
                     print('Confidence: %d%%' % (resp.json()['likelihood']*100,))

       else:
              print('%s - %s' % (email, resp.json()['message']))


if __name__ == "__main__":
       parser = argparse.ArgumentParser(description='Makes a search on fullcontact api.', prog='checkFullContactAPI.py', epilog="", add_help=False)
       # Adding the main options
       parser.add_argument('-e', '--email', metavar='<email>', action='store', help='query to be resolved by fullcontact.com.')
       parser.add_argument('-j', '--json', metavar='<json>', action='store', help='save results in json file.',required=False)  
       args = parser.parse_args()        
       get_fullcontact(args.email,args.json)