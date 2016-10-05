import tweepy
from tweepy import *
import pytz
import json
import argparse

# Consumer keys and access tokens, used for OAuth 
consumer_key = 'cRz70QuhNCGvFMlFHy3ARekMY'
consumer_secret = 'WBdhkig3nZ5DTFZS0UKN0k2HnmwgbQ39xQRN6kWzeE2DfvYztg'
access_token = '201832916-lLrZ1Qw4D5zQZii0k3RgOxuY0ymnyJfPkQSXu1sc'
access_token_secret = 'YLKNQfqIfgN9PK8IwYBd3TsSI3fkl1pfXgUkM3aP9Xgl8'

def getTimezoneNameFromReported(tzReported):
            allTimezones = pytz.all_timezones
            for timezone in allTimezones:
                        if tzReported.lower() in timezone.lower():
                                    return True, timezone
            return False, tzReported

def getCenterOfPolygon(coord):
            lat_list = []
            lon_list = []
            for j in coord:
                        lon_list.append(j[0])
                        lat_list.append(j[1])
            lon_list.sort()
            lat_list.sort()
            lat = float(lat_list[0]) + ((float(lat_list[len(lat_list) - 1]) - float(lat_list[0])) / 2)
            lon = float(lon_list[0]) + ((float(lon_list[len(lon_list) - 1]) - float(lon_list[0])) / 2)
            return lon, lat

def buildLocationFromTweet(tweet, finalDateTimeObj):

            loc = {}
            loc['username'] = tweet.user.screen_name
            loc['text'] = tweet.text
            loc['date'] = finalDateTimeObj
            
            if tweet.coordinates and tweet.place:
                        if tweet.coordinates['type'] == 'Point':
                                    loc['latitude'] = tweet.coordinates['coordinates'][1]
                                    loc['longitude'] = tweet.coordinates['coordinates'][0]
                                    loc['place'] = tweet.place.name
                                    loc['accuracy'] = 'high'
                        elif tweet.coordinates.type == 'PolyGon':
                                    c = getCenterOfPolygon(tweet.coordinates['coordinates'])
                                    loc['latitude'] = c[1]
                                    loc['longitude'] = c[0]
                                    loc['place'] = tweet.place.name
                                    loc['accuracy'] = 'low'
                        return loc
            elif tweet.place and not tweet.coordinates:
                        if tweet.place.bounding_box.type == 'Point':
                                    loc['latitude'] = tweet.place.bounding_box.coordinates[1]
                                    loc['longitude'] = tweet.place.bounding_box.coordinates[0]
                                    loc['place'] = tweet.place.name
                                    loc['accuracy'] = 'high'
                        elif tweet.place and tweet.place.bounding_box.type == 'Polygon':
                                    c = getCenterOfPolygon(tweet.place.bounding_box.coordinates[0])
                                    loc['latitude'] = c[1]
                                    loc['longitude'] = c[0]
                                    loc['place'] = tweet.place.name
                                    loc['accuracy'] = 'low'
                        return loc
            else:
                        return {}

if __name__ == '__main__':
    
            # OAuth process, using the keys and tokens
            auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
            auth.set_access_token(access_token, access_token_secret)
     
            # Creation of the actual interface, using authentication
            api = tweepy.API(auth)
     
            parser = argparse.ArgumentParser(description='Twitter obtain locations')
                
            # Main arguments
            parser.add_argument("-target", dest="target", help="twitter target", required=True)
            
            parsed_args = parser.parse_args()       

            # Obtain the user object
            userObject = api.get_user(screen_name=parsed_args.target)
     
            print('Name: ' + userObject.name.encode('utf-8'))
            print('Location: ' + userObject.location)
            print('Friends: ' + str(userObject.friends_count))

    
            print ('Account was created on {0}'.format(userObject.created_at.strftime('%Y-%m-%d %H:%M:%S %z')))
            
            if userObject.statuses_count:
                        print('\n\nThe user has tweeted {0} times ( including retweets ).'.format(str(userObject.statuses_count)))
            if userObject.name:
                        print('\n\nSelf-reported real name: {0}'.format(userObject.name.encode('utf-8')))
            if userObject.description:
                        print('\n\nDescription: {0}'.format(userObject.description.encode('utf-8')))
            if userObject.location:
                        print('\n\nSelf-reported location: {0}'.format(userObject.location.encode('utf-8')))
            if userObject.time_zone:
                        conversionResult, formalTimezoneName = getTimezoneNameFromReported(userObject.time_zone)
                        if conversionResult:
                                    print('\n\nSelf-reported time zone: {0}'.format(formalTimezoneName))
                        else:
                                    print('\n\nSelf-reported time zone: {0}'.format(userObject.time_zone))
            if userObject.geo_enabled:
                        print('\n\nUser has enabled the possibility to geolocate their tweets.')
            else:
                        print('\n\nUser has disabled the possibility to geolocate their tweets.')
            if userObject.followers_count:
                        print('\n\nThe user has {0} followers.'.format(str(userObject.followers_count)))
            if userObject.friends_count:
                        print('\n\nThe user is following {0} users.'.format(str(userObject.friends_count)))
            if userObject.listed_count:
                        print('\n\nThe user is listed in {0} public lists.'.format(str(userObject.listed_count)))
        

            
            
            
            tweets = Cursor(api.user_timeline, count=100, screen_name=parsed_args.target,exclude_replies=True, include_rts=True).items()
            timestamps = []
            repliedTo = []
            retweeted = []
            clientApplications = []
            mentioned = []
            hashtags = []
            locations_list=[]
            
            twitter_results = []
            
            for j in tweets:
                        finalDateTimeObj = pytz.utc.localize(j.created_at)
                        if conversionResult:
                                    createdUtcTimezone = pytz.utc.localize(j.created_at)
                                    try:
                                                userTimezone = pytz.timezone(formalTimezoneName)
                                                createdUserTimezone = userTimezone.normalize(createdUtcTimezone.astimezone(userTimezone))
                                                timestamps.append(createdUserTimezone)
                                                finalDateTimeObj = createdUserTimezone
                                    except Exception as e:
                                                pass
                        else:
                                    timestamps.append(pytz.utc.localize(j.created_at))
                        if j.in_reply_to_screen_name:
                                    repliedTo.append(j.in_reply_to_screen_name)
                        if hasattr(j, 'retweeted_status'):
                                    retweeted.append(j.retweeted_status.user.name)
                        if j.source:
                                    clientApplications.append(j.source)
                        if j.entities:
                                    if hasattr(j, 'entities.user_mentions'):
                                                for mention in j.entities.user_mentions:
                                                            mentioned.append(mention.screen_name)
                                    if hasattr(j, 'hashtags'):
                                                for hashtag in j.entities.hashtags:
                                                            hashtags.append(hashtag.text)
                                    loc = buildLocationFromTweet(j, finalDateTimeObj)
                                    if loc:
                                                locations_list.append(loc)            
    
            if len(repliedTo) > 0:
                        print('\n\nUser has replied to the following users : ')
                        print(repliedTo)
                                    
            if len(retweeted) > 0:
                        print('\n\nUser has retweeted the following users : ')
                        for ret in retweeted:
                                    print(ret.encode('ascii', 'ignore'))
                        
            if len(mentioned) > 0:
                        print('\n\nUser has mentioned the following users : ')
                        print(mentioned)                        
     
            if len(clientApplications) > 0:
                        print('\n\nUser has been using the following clients : ')
                        print(clientApplications)   
                                    
            if len(hashtags) > 0:
                        print('\n\nUser has used the following hashtags : ')
                        print(hashtags) 
            
            if len(locations_list) > 0:
                        print('\n\Tweets have the following locations : ')
                        for location in locations_list:
                                    print("--------------Tweet location detected------------")
                                    print("\nUsername:"+location['username'].encode('utf-8').decode('utf-8'))
                                    print("\nLongitude:"+str(location['longitude']))
                                    print("\nLatitude:"+str(location['latitude']))
                                    print("\nText:"+location['text'].encode('utf-8'))
                                    print("\nPlace:"+location['place'].encode('utf-8').decode('utf-8'))
                                    print("-------------------------------------------------")
                                    
                                    tweetData= {}
                                    
                                    tweetData['username'] = location['username'].encode('utf-8').decode('utf-8')
                                    tweetData['longitude'] = str(location['longitude'])
                                    tweetData['latitude'] = str(location['latitude'])
                                    tweetData['text'] = location['text'].encode('utf-8')
                                    tweetData['date'] = str(finalDateTimeObj)
                                    tweetData['place'] = location['place'].encode('utf-8').decode('utf-8')
                                    twitter_results.append(tweetData)                                    
            else:
                        print('\nNo Tweets found locations : ')  
                                    
            
            outfile = open('twitter_locations.json','wb')
                                
            for twitter_result in twitter_results:
                        line = json.dumps(twitter_result,sort_keys=True, indent=4) + "\n"
                        outfile.write(line)            