===========================================
OSINT tool for security auditing with Python
===========================================


Install dependences from requeriments.txt
================================
pip install -r requeriments.txt


All scripts are compatible with python 3.5,except someones specified only compatible with 2.7

SHODAN
================================
<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/shodanSearch.png" alt="ShodanSearch"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/shodanSearch1.png" alt="ShodanSearch"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/shodanSearch2.png" alt="ShodanSearch"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/shodanSearch3.png" alt="ShodanSearch"/>

Google profile pics
================================
<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/googlePics.png" alt="GooglePics"/>


IP MAP position
================================
<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/ip_map_position.png" alt="ip_map_position"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/geoIp.png" alt="geoIp"/>


External/internal links
================================
<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/crawler_links.png" alt="crawler_links"/>


Maltego transforms
================================
<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/maltego_domains.png" alt="maltego_domains"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/maltego_emails.png" alt="maltego_emails"/>


Metadata
================================
Extra metada from images allocated in images folder

Required python 2.7

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/metadata.png" alt="metadata"/>


Panoramio
================================
Get images from panoramio and wikimapia from a specific location


TOR
================================
Connecting with TOR and ZERONET networks with deepify module


Youtube
================================
Get images from a youtube video


Builtwith
================================
Required python 2.7

Get information about tecnologies and libraries used from a specific web domain

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/built_with.png" alt="built_with"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/built_with3.png" alt="built_with"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/built_with2.png" alt="built_with"/>


Censys
================================
Get information about certificates,location,domains

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/censys.png" alt="censys_data"/>


Check social networks
================================
Check social profile networks for a specific username

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/social_networks.png" alt="socials_networks"/>


Check full Contact API
================================
It provides an API for obtain social networks profiles associated with an email address.

If we have an email address we can obtain information related with this person,
in this example we are obtaining social networks profiles from guido van rosum.

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/full_contact.png" alt="full_contact"/>


Check IP details
================================
Get location information for a ip address

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/ip_details.png" alt="ip_details"/>


Check Linkedin profile
================================
Get linkedin profile given company name

site:linkedin.com/company "name"


GitHub repositories
================================
Get github repositories from a specific account name

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/github_repositories.png" alt="github_repositories"/>


Pattern data
================================
We can make a search in twitter with a specific tag and get words relationed with this search

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/pattern_data1.png" alt="pattern_data"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/pattern_data2.png" alt="pattern_data"/>


Virus total
================================
Virtus total provides API for gather information about malware
in a specific ip/domain. It return a json document 
where we can parse information about detected_urls.

We can search by ip address or domain

In order to retrieve a report on a given IP address
you must perform an HTTP GET request to the following URL:

http://www.virustotal.com/vtapi/v2/ip-address/report

It shows info about subdomains analyzed,ip address resolution,files detection..

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/virus_total.png" alt="virus_total"/>


Twitter
================================
osint_twitter
--------------------
Get trending topics and streaming for targetTerms = ['python', 'pydata','pycones']

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/streamer.png" alt="streamer"/>

twitter_locations
-----------------------
Get information about specific twitter account

Obtain twitter locations from a specific target

It generates twitter_locations.json with the locations detected


<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/twitter.png" alt="twitter"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/twitter2.png" alt="twitter"/>

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/twitter3.png" alt="twitter"/>

twitter_timeline
---------------------
Get photos for a specific twitter account

<img src="https://github.com/jmortega/osint_tools_security_auditing/blob/master/images/twitter4.png" alt="twitter"/>
