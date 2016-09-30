from bs4 import BeautifulSoup
import re
import datetime
import random
import requests
import argparse

pages = set()
random.seed(datetime.datetime.now())

# parse the command line arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d","--domain",required=True,help="The domain to target ie. cnn.com")
args = vars(ap.parse_args())

domain = args['domain']

#Retrieves a list of all Internal links found on a page
def getInternalLinks(bsObj, includeUrl):
    internalLinks = []
    #Finds all links that begin with a "/"
    for link in bsObj.findAll("a", href=re.compile("^(/|.*"+includeUrl+")")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in internalLinks:
                internalLinks.append(link.attrs['href'])
    return internalLinks
            
#Retrieves a list of all external links found on a page
def getExternalLinks(bsObj, excludeUrl):
    externalLinks = []
    #Finds all links that start with "http" or "www" that do
    #not contain the current URL
    for link in bsObj.findAll("a", href=re.compile("^(http|www)((?!"+excludeUrl+").)*$")):
        if link.attrs['href'] is not None:
            if link.attrs['href'] not in externalLinks:
                externalLinks.append(link.attrs['href'])
    return externalLinks

def splitAddress(address):
    addressParts = address.replace("http://", "").split("/")
    return addressParts

def crawlExternalLinks(startingPage):
    html = requests.get(startingPage).text
    bsObj = BeautifulSoup(html,"html.parser")
    externalLinks = getExternalLinks(bsObj, splitAddress(startingPage)[0])
    return externalLinks

def crawlInternalLinks(startingPage):
    html = requests.get(startingPage).text
    bsObj = BeautifulSoup(html,"html.parser")
    internalLinks = getInternalLinks(bsObj,splitAddress(startingPage)[0])
    return internalLinks
		
def crawlSite(startingSite):
    externalLinks = crawlExternalLinks(startingSite)
    internalLinks = crawlInternalLinks(startingSite)
    print("\nExternal links")
    print("-------------------")
    
    
    for external in externalLinks:
	    print(external)
	    
    print("\nInternal links")
    print("-------------------")    
    for internal in internalLinks:
	    print(internal)


if domain.startswith("http://") == True:
    target = domain
else:   
    target = "http://" + domain
    
crawlSite(target)