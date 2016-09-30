#!/usr/bin/env python

import sys

import argparse
import json
import os
import logging
import geoip2
import geoip2.database
import dns.resolver
import requests
import re

def checkIpDetails(query=None):
    ''' 
        Method that obtain ip details:
        {
            "as": "AS8560 1\u00261 Internet AG",
            "city": "",
            "country": "Germany",
            "countryCode": "DE",
            "isp": "1\u00261 Internet AG",
            "lat": 51,
            "lon": 9,
            "org": "1\u00261 Internet AG",
            "query": "217.160.251.126",
            "region": "",
            "regionName": "",
            "status": "success",
            "timezone": "",
            "zip": ""
        }      
    '''
    try:    
        apiURL = "http://ip-api.com/json/" + query


        # Accessing the ip-api.com RESTful API
        data = requests.get(apiURL)

        # Reading the text data onto python structures
        apiData = json.loads(data.text)
        
        # json structure to be returned
        jsonData = []
        
        if apiData["status"] == "success":
            for key in apiData:
                value = apiData[key]
                if value != "":
                    aux = {}
                    if key == "city":
                        aux["type"] = "location.city" 
                        aux["value"] = value
                        # Appending to the list of results                        
                        jsonData.append(aux)
                    elif key == "country":
                        aux["type"] = "location.country" 
                        aux["value"] = value
                        # Adding a new attribute
                        att ={}
                        att["value"] = apiData["countryCode"]
                        att["attributes"] = []
                        aux["attributes"] = [att]
                        # Appending to the list of results
                        jsonData.append(aux)
                    elif key == "isp":
                        aux["type"] = "isp"
                        aux["value"] = value
                        # Appending to the list of results                        
                        jsonData.append(aux)                        
                    elif key == "lat":
                        aux["type"] = "location.geo"
                        aux["value"] = str(apiData["lat"]) + ", " + str(apiData["lon"])
                        # Appending to the list of results                        
                        jsonData.append(aux)
                    elif key == "region":
                        aux["type"] = "location.province"
                        aux["value"] = value
                        # Adding a new attribute
                        att ={}
                        att["value"] = apiData["regionName"]                      
                        aux["attributes"] = [att]
                        # Appending to the list of results                        
                        jsonData.append(aux)
                    elif key == "timezone":
                        aux["type"] = "location.timezone"
                        aux["value"] = value
                        # Appending to the list of results                        
                        jsonData.append(aux)                        
                    elif key == "zip":
                        aux["type"] = "location.postalcode"
                        aux["value"] = value
                        # Appending to the list of results                        
                        jsonData.append(aux)                        
                    elif key == "query":
                        aux["type"] = "ipv4"
                        aux["value"] = value
                        # Appending to the list of results                        
                        jsonData.append(aux)                        
                        
        return jsonData
    except:
        # No information was found, then we return a null entity
        return {}   


def getGeo(domain):
    ip = ip_resolver(domain)
    response = ''
    if not os.path.exists('GeoLite2-City.mmdb'):
        msg = "[*] GeoLite2-City.mmdb is not found ..."+logging.error(msg)
    else:
        try:
            reader = geoip2.database.Reader('GeoLite2-City.mmdb')
            response = reader.city(ip)
        except Exception as e:
            print (e)
            msg = "[*] AddressNotFoundError for ip: %s" % (ip)
            logging.error(msg)
    
    return response

def ip_resolver(domain):
    ip = ''
    c_name = ''
    resolver = dns.resolver.Resolver()
    resolver.timeout = 1
    try:
        answers = resolver.query(domain)
        ip = str(answers[0]).split(": ")[0]
        c_name = answers.canonical_name
    except Exception as e:
        msg = '[*] No IP Addressed: Timeout, NXDOMAIN, NoAnswer or NoNameservers'
        logging.info(msg)
    return ip


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Makes a search onto ip-api.com.', prog='checkIPDetails.py', epilog="", add_help=False)
    # Adding the main options
    general = parser.add_mutually_exclusive_group(required=True)
    general.add_argument('-d', '--domain', metavar='<ip_or_domain>', action='store', help='query to be resolved by ip-api.com.')        
    args = parser.parse_args()        
    
    print(json.dumps(checkIpDetails(args.domain), indent=2))
    
    try:
        response = getGeo(args.domain)
        if response is not None:
            if response.country is not None:
                print('\nCountry:'+response.country.name)
            if response.city is not None:       
                print('\nCity:'+response.city.name)
            if response.location is not None:       
                print('\nLatitude'+str(response.location.latitude))
                print('\nLongitude'+str(response.location.longitude))
    except Exception as e:
        pass
        
    ip_resolver(args.domain)
