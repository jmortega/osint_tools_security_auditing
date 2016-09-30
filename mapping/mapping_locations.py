import argparse
import geopy
import json
import requests

from geopy.distance import vincenty

wikimapia_api_key = "91EFB435-ABB94D7F-7F65AE6F-082A80F0-43E6FABF-44053871-3B03A846-5A5DD16B"

ap = argparse.ArgumentParser()
ap.add_argument("-c","--city",required=True,help="Pass in a city name like: Barcelona")
args = vars(ap.parse_args())

print("[*] Attempting to resolve %s" % args['city'])

# find the location
geosearch  = geopy.GoogleV3()
geo_result = geosearch.geocode(args['city'])

# if we receive a result extract the coordinates
if geo_result is not None:
    
    latitude  = geo_result.latitude
    longitude = geo_result.longitude
    print(latitude)
    print(longitude)

    # send off a request to Wikimapia to get the city
    url = "http://api.wikimapia.org/?key=%s&function=place.getnearest&lat=%f&lon=%f&format=json&count=1&category=88" % (wikimapia_api_key,latitude,longitude)
    
    response = requests.get(url)
    
    if response.status_code == 200:
        
        nearest = json.loads(response.content.decode('utf-8'))
        
        if not len(nearest['places']):
            print("[!] Could not find Wikimapia entry. Sorry.")
        else:
            
            location = nearest['places'][0]['location']
            print(location)
            # bounding box is contained in location result
            # so let's measure the distance from the center to each corner
            
            distance_to_ne = vincenty((location['lat'],location['lon']),(location['north'],location['east'])).m
            distance_to_sw = vincenty((location['lat'],location['lon']),(location['south'],location['west'])).m
            
            # now take the greater of the two measurements
            if distance_to_ne > distance_to_sw:
                radius = distance_to_ne
            else:
                radius = distance_to_sw
                
            print("[*] Search radius of %f meters" % radius)
            
            # now we search for data within this calculated radius
            url = "http://api.wikimapia.org/?key=%s&function=place.search&lat=%f&lon=%f&category=203&count=100&format=json" % (wikimapia_api_key,location['lat'],location['lon'])
            
            data = []
            
            response    = requests.get(url)
            
            if response.status_code == 200:
                
                data_result = json.loads(response.content.decode('utf-8'))
                
                data.extend(data_result['places'])
                
                # we keep incrementing the number of pages
                page = 2
                
                while len(data) < int(data_result['found']):
                    page_url = "%s&page=%d" % (url,page)
                    
                    response = requests.get(page_url)
                    
                    if response.status_code == 200:
                        
                        data_result = json.loads(response.content.decode('utf-8'))
                        
                        data.extend(data_result['places'])

                    else:
                        print("[!] Error retrieving page %d results." % page)
                        break
                        
                    page += 1
                
                
                # now we have a list of all of the data we can store
                print("[*] Retrieved %d data" % len(data))
                
                # dump the data to a json file
                fd = open("data.json","w")
                fd.write(json.dumps(data))
                fd.close()
                
