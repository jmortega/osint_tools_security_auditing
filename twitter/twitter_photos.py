import requests
import requests_oauthlib
import os
import base64
import time
import json


api_key = 'acc_0da0ccc6a62385e'
api_secret = 'f24ac09e6fb32d560f70cc9974af8ef6'
image_url = 'https://imagga.com/static/images/tagging/wind-farm-538576_640.jpg'


custom_tags = set(["python"])


client_key    = "cRz70QuhNCGvFMlFHy3ARekMY"
client_secret = "WBdhkig3nZ5DTFZS0UKN0k2HnmwgbQ39xQRN6kWzeE2DfvYztg"
token         = "201832916-lLrZ1Qw4D5zQZii0k3RgOxuY0ymnyJfPkQSXu1sc"
token_secret  = "YLKNQfqIfgN9PK8IwYBd3TsSI3fkl1pfXgUkM3aP9Xgl8"

oauth = requests_oauthlib.OAuth1(client_key,client_secret,token,token_secret)

#
# Download Tweets from a user profile
#
def download_tweets(screen_name,max_id=None):
    
    api_url  = "https://api.twitter.com/1.1/statuses/user_timeline.json?"
    api_url += "screen_name=%s&" % screen_name
    api_url += "count=200"
    
    if max_id is not None:
        api_url += "&max_id=%d" % max_id

    # send request to Twitter
    response = requests.get(api_url,auth=oauth)
    
    if response.status_code == 200:
        print(response.content)
        
        tweets = json.loads(response.content.decode('utf-8'))
        
        return tweets
    
    else:
        
        print("[*] Twitter API FAILED! %d" % response.status_code)
    

    return None

#
# Takes a username and begins downloading all Tweets
#
def download_all_tweets(username):
    full_tweet_list = []
    max_id          = 0
    
    # grab the first 200 Tweets
    tweet_list   = download_tweets(username)
    
    # grab the oldest Tweet
    if tweet_list is None:
        return
    
    oldest_tweet = tweet_list[-1]
    
    # continue retrieving Tweets
    while max_id != oldest_tweet['id']:
    
        full_tweet_list.extend(tweet_list)

        # set max_id to latest max_id we retrieved
        max_id = oldest_tweet['id']         

        print("[*] Retrieved: %d Tweets (max_id: %d)" % (len(full_tweet_list),max_id))
    
        # sleep to handle rate limiting
        time.sleep(3)
        
        # send next request with max_id set
        tweet_list = download_tweets(username,max_id-1)
    
        # grab the oldest Tweet
        if len(tweet_list):
            oldest_tweet = tweet_list[-1]
        

    # add the last few Tweets
    full_tweet_list.extend(tweet_list)
        
    # return the full Tweet list
    return full_tweet_list



#
# Submits an uploaded file to the tagging API.
#
def tag_image(image_url):
    
        response = requests.get('https://api.imagga.com/v1/tagging?url=%s' % image_url,auth=(api_key, api_secret))

        result = response.json()
        
        print(result)
        
        tags = []
        
        for i in result['results'][0]['tags']:
    
            tags.append(i['tag'])
    
        tags = set(tags)
    
        matches = tags.intersection(custom_tags)
    
        if len(matches):
            print("[*] Image matches! => ")
            
            for match in matches:
                print (match)
            
            return True
    
        return False

               
#
# Wrapper function that kicks off the entire detection process.
#
def detect_tags(image_path,file_name):    

    print("[*] Trying image %s" % image_path)
    
    if image_path != None:
        
        result = tag_image(image_path)
        
        print(result)
    
        if result is False:
        
            return result
        
        else:
            
            print("[*] Image matches!")
            return True
        
        
full_tweet_list = download_all_tweets("jmortegac")

print("[*] Retrieved %d Tweets. Processing now..." % len(full_tweet_list))

if not os.path.exists("photos"):
    os.mkdir("photos")

photo_count = 0
match_count = 0

for tweet in full_tweet_list:
        
    if 'extended_entities' in tweet:
        if tweet['extended_entities'] is not None:
            if 'media' in tweet['extended_entities']:
                
                for media in tweet['extended_entities']['media']:
                    
                    print("[*] Downloading photo %s" % media['media_url'])

                    photo_count += 1
                    
                    response = requests.get(media['media_url'])

                    file_name = media['media_url'].split("/")[-1]
                    
                    # write out the file
                    fd = open("photos/%s" % file_name,"wb")
                    fd.write(response.content)
                    fd.close()
                    
                    # now test for tags!
                    result = detect_tags(media['media_url'],"photos/%s" % file_name)
                                        
                    if result != True:
                        os.remove("photos/%s" % file_name)
                    else:
                        match_count += 1
                        
print("[*] Finished! Checked %d photos and detected %d with tags." % (photo_count,match_count))