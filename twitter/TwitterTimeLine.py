# -*- encoding: utf-8 -*-

import twitter
import sqlite3
import csv
import json
import argparse

def getTimeLine(target):
    apiTwitter = twitter.Api(consumer_key="cRz70QuhNCGvFMlFHy3ARekMY",
                         consumer_secret="WBdhkig3nZ5DTFZS0UKN0k2HnmwgbQ39xQRN6kWzeE2DfvYztg",
                         access_token_key="201832916-lLrZ1Qw4D5zQZii0k3RgOxuY0ymnyJfPkQSXu1sc",
                         access_token_secret="YLKNQfqIfgN9PK8IwYBd3TsSI3fkl1pfXgUkM3aP9Xgl8")


    timeline = apiTwitter.GetUserTimeline(screen_name=target)

    print("\nStatus:",timeline[0])


    print("\nFriends:")
    accountFriends = [account.name for account in apiTwitter.GetFriends(screen_name=target)]
    
    for friend in accountFriends:
        print(friend.encode('ascii', 'ignore').decode('utf-8'))

    print("\nTweets: ")
    query = apiTwitter.GetSearch("#"+target, count=100)

    twitter_results = []

    for result in query:
        tweet = {}
        print("Tweet: %s " %(result.text.encode('ascii', 'ignore').decode('utf-8')))
        tweet['text'] = result.text.encode('ascii', 'ignore').decode('utf-8')
        print("Creation date: %s " %(result.created_at))
        tweet['date'] = result.created_at.encode('ascii', 'ignore').decode('utf-8')
        print("Favs count: %d" %(result.favorite_count))
        tweet['favorite_count'] = result.favorite_count
        print("Language: %s" %(result.lang))
        tweet['lang'] = result.lang.encode('ascii', 'ignore').decode('utf-8')
        print("Retweets count: %d" %(result.retweet_count))
        tweet['retweet_count'] = result.retweet_count
        print("Account: %s" %( result.user.screen_name ))
        tweet['account'] = result.user.screen_name.encode('ascii', 'ignore').decode('utf-8')
        print("\n")
        twitter_results.append(tweet)
    
    connection = sqlite3.connect('db.sqlite3')
    print("Database db.sqlite3 created succesfully")
    cursor = connection.cursor()

    connection.execute("create table if not exists  TwitterMessages(id integer primary key autoincrement, message varchar(140), account varchar(20),favs integer,retweets integer,langTweet varchar(5), dateMessages varchar (30) );")

    query = apiTwitter.GetSearch("#"+target, count=100)

    insert = "insert into TwitterMessages(message, dateMessages, favs, langTweet, retweets, account) values(?,?,?,?,?,?)"
    
    for result in query:
            cursor.execute(insert, (result.text, result.created_at, result.favorite_count, result.lang, result.retweet_count, result.user.screen_name))

    connection.commit()

    outfile = open('twitter.json','wb')

    with open('twitter.json', 'w') as file:
        for twitter_result in twitter_results:
            json.dump(twitter_result, file, ensure_ascii=False,indent=4)
            

	
    with open('twitter.csv' ,'w') as csvfile:
        twitter_writer = csv.writer(csvfile)
        for result in twitter_results:
            twitter_writer.writerow([str(result['text']),str(result['date']),str(result['favorite_count']),str(result['lang']),str(result['retweet_count'])])
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Twitter timeline from an account')
    # Main arguments
    parser.add_argument("-target", dest="target", help="twitter target", required=True)
    parsed_args = parser.parse_args()       
    # Obtain the user timeline
    getTimeLine(parsed_args.target)