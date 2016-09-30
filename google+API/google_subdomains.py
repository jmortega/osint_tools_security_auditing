#!/usr/bin/env python


import sys

import argparse
import os
import logging
import requests
import re
import time
from random import randint, choice

class GoogleDomainResult(object):
    """
    Holds Google results for each domain.
    Keyword arguments:
    urls -- dict with key=protocol value=set of pathnames of urls for this domain
            Example - {'http://':{'/','/home','/test/asd.html'}}
    count -- Integer for how many times this was found in google
    """
    def __init__(self):
        self.urls = {}
        self.count = 0

    def add_url(self, g_protocol, g_pathname):
        self.urls.setdefault(g_protocol, set()).add(g_pathname)
        self.count += 1
        
def google_subdomains(name):
    """
    This method uses google dorks to get as many subdomains from google as possible
    Returns a dictionary with key=str(subdomain), value=GoogleDomainResult object
    """

    google_results = {}
    results_in_last_iteration = -1

    while len(google_results) > results_in_last_iteration:

        time.sleep(randint(0, 4) + randint(0, 1000) * 0.001)

        # Make this funct keep iterating until there are new results
        results_in_last_iteration = len(google_results)

        #Order google_results by .count, as we want only the top 8 subs with more results
        list_of_sub_ordered_by_count = sorted(google_results, key = lambda sub: google_results[sub].count, reverse=True)

        google_results = _update_google_results(
            _google_subdomain_lookup(
                name,
                [sub for sub in list_of_sub_ordered_by_count if sub != name],
                100,
                0
            ),
            google_results
        )

        logging.debug('New subdomain(s) found: ' + str(len(google_results)-len(list_of_sub_ordered_by_count)))
        [logging.debug(sub + ' - ' + str(google_results[sub].count)) for sub in sorted(google_results, key = lambda sub: google_results[sub].count, reverse=True)]

    logging.debug('Finished google lookups with '+str(len(google_results))+' subdomains discovered.')

    return google_results

def _update_google_results(new_google_results, results_dictionary):
    """Internal generator that manages multiple _google_subdomain_lookup"""
    for url in new_google_results:
        # Removing html tags from inside url (sometimes they use <b> or <i> for ads)
        url = re.sub('<.*?>', '', url)

        # Follows Javascript pattern of accessing URLs
        g_host = url
        g_protocol = ''
        g_pathname = ''

        temp = url.split('://')

        # If there is g_protocol e.g. http://, ftp://, etc
        if len(temp) > 1:
            g_protocol = temp[0] + '://'
            g_host = temp[1:]
        else:
            g_protocol = 'http://'

        temp = ''.join(g_host).split('/')

        # if there is a pathname after host
        if len(temp) > 1:
            g_pathname = ''.join(['/', '/'.join(temp[1:])])
            g_host = temp[0]

        # if there is a port specified
        temp = g_host.split(':')
        if len(temp) > 1:
            g_host = temp[0]
            g_pathname = ''.join([':', temp[1], g_pathname])
            logging.debug('Found host ' + g_host + ' with port ' + temp[1] + '. New pathname is ' + g_pathname)

        results_dictionary.setdefault(g_host, GoogleDomainResult()).add_url(g_protocol, g_pathname)

    return results_dictionary

def _google_subdomain_lookup(domain, subs_to_avoid=(), num=100, counter=0):
    """
    Reaches out to google using the following query:
    site:*.domain -site:subdomain_to_avoid1 -site:subdomain_to_avoid2 -site:subdomain_to_avoid3...
    Returns list of unique subdomain strings
    """
    request = ''.join([
        'http://google.com/search?&num=',
        str(num),
        '&start=',
        str(counter),
        '&q=',
        'site%3A%2A%2E',
        domain,
    ])
    
    logging.info('Subs removed from next query: ' + ', '.join(subs_to_avoid[:8]))

    if subs_to_avoid:
        for subdomain in subs_to_avoid[:8]:
            request = ''.join([request, '%20%2Dsite%3A', str(subdomain)])

    try:
        # Content within cite had url shortening features where '/.../' would appear in the middle of the url
        #return re.findall('<cite>(.+?)<\/cite>', requests.get(request).text)

        return re.findall('<h3 class\=\"r\"><a href=\"/url\?q\=(.+?)\&amp', requests.get(request).text)
        
    except requests.ConnectionError as e:
        logging.warning(e)
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Uses a google query to find subdomains.', prog='checkLinkedLinProfile.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved.')        
    args = parser.parse_args()       
    
    subdomains_as_hosts = set([])
    
    results = google_subdomains(args.domain)
    for sub_str, google_results in results.items():#python 2 iteritems()
        urls = google_results.urls
        for key, value in urls.items():#python 2 iteritems()
            for url in value:
                print(url)
        