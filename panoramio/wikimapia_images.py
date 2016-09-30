import requests
import json
import os
import math
import bs4

wikimapia_key    = "91EFB435-ABB94D7F-7F65AE6F-082A80F0-43E6FABF-44053871-3B03A846-5A5DD16B"
search_name      = "Barcelona"
southwest_corner = "41.36329488429618,2.1527066229464253"
northeast_corner = "41.36608094202317,2.157534599173232"
center           = "41.36468791315967,2.1551206110598287"
radius           = "254.40512553139257"

# we use the coordinates
lat_min,long_min        = southwest_corner.split(",")
lat_max,long_max        = northeast_corner.split(",")
center_lat, center_long = center.split(",") 



#
# Helper function to grab photos from Wikimapia results
#
def get_photos_from_result(search_results):

    photo_list = []
    
    for result in search_results['places']:
            
        # are there photos in this result?
        if len(result['photos']):
            
            for photo in result['photos']:
                photo_record = {}
                photo_record['latitude']       = result['polygon'][0]['y']
                photo_record['longitude']      = result['polygon'][0]['x']
                photo_record['photo_file_url'] = photo['big_url']
                
                # now we parse out the HTML
                link_html_object = bs4.BeautifulSoup(result['urlhtml'])
                link_location    = link_html_object.a['href']
                
                photo_record['photo_link']     = link_location
                
                photo_list.append(photo_record)    

    return photo_list

#
# Function responsible for sending requests to Wikimapia API
#
def send_wikimapia_request(page):
    
    api_url  = "http://api.wikimapia.org/?key=%s&function=place.search&q=&" % wikimapia_key
    api_url += "lat=%s&lon=%s&" % (center_lat,center_long)
    api_url += "page=%d&count=100&" % page  
    api_url += "category=&categories_or=&categories_and=&distance=%s&" % radius
    api_url += "format=json&pack=&language=en"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        
        search_results = json.loads(response.content.decode('utf-8'))
        
        return search_results
    
    return None

#
# Grab all photos from a Wikimapia area
#
def get_all_wikimapia_photos():
    photo_list = []
    page       = 1
    
    # send the intial request
    search_results = send_wikimapia_request(page)

    # if there was an error return nothing
    if search_results is None:
        print("[*] Error retrieving photos from Wikimapia")
        return

    # use our helper function to grab the photos 
    photo_list.extend(get_photos_from_result(search_results))
    
    print("[*] Retrieved %d photos..." % (len(photo_list)))
    
    # find the total number of pages
    total_pages = (int(search_results['found']) / 100) + 1
        
    # keep polling for new records
    while page <= total_pages:
        
        # increase our page count
        page += 1
        
        search_results = send_wikimapia_request(page)
        
        if search_results is not None:
            photo_list.extend(get_photos_from_result(search_results))
            
            print("[*] Retrieved %d photos...(Wikimapia)" % (len(photo_list)))
            

    # return all of our photos     
    return photo_list     
    

#
# Function responsible for sending requests to Panoramio API
#
def send_panoramio_request(start,end):

    api_url  = "http://www.panoramio.com/map/get_panoramas.php?set=full&"
    api_url += "from=%d&to=%d&" % (start,end)
    api_url += "minx=%s&miny=%s&maxx=%s&maxy=%s&" % (long_min,lat_min,long_max,lat_max)
    api_url += "size=medium&mapfilter=false"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        
        # convert to a dictionary
        search_results = json.loads(response.content.decode('utf-8'))
        
        return search_results

    # there was a problem
    return None


#
# Use the Panaramio API to get all pictures
#
def get_all_panoramio_pictures():

    photo_list   = []
    search_start = 0
    
    # send the intial request
    search_results = send_panoramio_request(search_start,search_start+50)

    # if there was an error return nothing
    if search_results is None:
        print("[*] Error retrieving photos.")
        return

    # add the current results to our list
    photo_list.extend(search_results['photos'])

    print("[*] Retrieved %d photos..." % (len(photo_list)))
    
    # while there are more photos to retrieve
    while search_results['has_more'] is True:
        
        # we increase the search count by 50
        search_start += 50
        
        search_results = send_panoramio_request(search_start,search_start+50)
        
        if search_results is not None:
            photo_list.extend(search_results['photos'])
            
            print("[*] Retrieved %d photos...(Panoramio)" % (len(photo_list)))
            

    # return all of our photos     
    return photo_list      
    
    
#
# Write out the list of photos
#
def write_photo_list(photo_list):

    fd = open("panoramio_%s.html" % (search_name),"w")
    fd.write("<html><head></head><body>")
    
    # walk through the list of photos and add them to our log file
    for photo in photo_list:
        
        # we have created a custom link so use it
        if 'photo_link' in photo:
            fd.write("<a href='%s' target='_blank'><img src='%s' border='0'></a><br/>\r\n" %
                                 (photo['photo_link'],photo['photo_file_url']))        
             
        else:
            
            # no custom link so create a Google Maps link
            fd.write("<a target='_blank' href='https://maps.google.com/?q=%f,%f'><img src='%s' border='0'></a><br/>\r\n" %
                                 (photo['latitude'],photo['longitude'],photo['photo_file_url']))        
        
    # close the html file
    fd.write("</body></html>")
    fd.close()
    
    return

full_list  = []

# grab Wikimapia photos
photo_list = get_all_wikimapia_photos()
full_list.extend(photo_list)

# grab Panoramio photos
photo_list = get_all_panoramio_pictures()
full_list.extend(photo_list)

print("[**] Total of %d pictures retrieved." % len(full_list))
write_photo_list(full_list)