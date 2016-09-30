import argparse
import requests
import json
import os

youtube_key = "AIzaSyDMxNuNUYgaHnhiSV8ldhv2fmv9ffsG2Hc"

ap = argparse.ArgumentParser()
ap.add_argument("-v","--videoID",    required=True,help="The videoID of the YouTube video. For example: https://www.youtube.com/watch?v=VIDEOID")
args = vars(ap.parse_args())

video_id    = args['videoID']

#
# Retrieve the video details based on videoID
#
def youtube_video_details(video_id):

    api_url  = "https://www.googleapis.com/youtube/v3/videos?part=snippet%2CrecordingDetails&"
    api_url += "id=%s&" % video_id
    api_url += "key=%s" % youtube_key
    
    response = requests.get(api_url,verify=False)
    
    if response.status_code == 200:
        
        results = json.loads(response.content)
        print(json.dumps(results,sort_keys=True,indent=2))
        return results

    return None


print("[*] Retrieving video ID: %s" % video_id)
video_data = youtube_video_details(video_id)

thumbnails = video_data['items'][0]['snippet']['thumbnails']

print ("[*] Thumbnails retrieved. Now submitting to TinEye.")

url_list = []

# add the thumbnails from the API to the list
for thumbnail in thumbnails:
    
    url_list.append(thumbnails[thumbnail]['url'])
    

print(url_list)

if not os.path.exists("images"):
    os.makedirs("images")

for url in url_list:

    filename=url.split('/')[-1]
    response = requests.get(url,verify=False)
    if response.status_code == 200:
        f = open('images/'+filename, 'wb')
        f.write(response.content)
        f.close() 
        
# build the manual URLS
for count in range(4):
    
    url = "http://img.youtube.com/vi/%s/%d.jpg" % (video_id,count)
    
    url_list.append(url)
    filename=url.split('/')[-1]
    response = requests.get(url)
    if response.status_code == 200:
        f = open('images/'+filename, 'wb')
        f.write(response.content)
        f.close()    
