import requests
import json
import urllib
import argparse

services = ['YouTube', 'Hypemachine', 'Yahoo', 'Linkagogo', 'Coolspotters', 'Wikipedia', 'Twitter', 'gdgt', 'BlogMarks', 'LinkedIn', 'Ebay', 'Tumblr', 'Pinterest',   
                'yotify', 'Blogger', 'Flickr', 'FortyThreeMarks,Moof', 'HuffingtonPost', 'Wordpress', 'DailyMotion', 'LiveJournal', 'vimeo', 'DeviantArt', 'reddit',   
                'StumbleUpon', 'Answers', 'Sourceforge', 'Wikia', 'ArmChairGM', 'Photobucket', 'MySpace', 'Etsy,SlideShare', 'Fiverr', 'scribd', 'Squidoo', 'ImageShack',   
                'ThemeForest', 'soundcloud', 'Tagged', 'Hulu', 'Typepad', 'Hubpages', 'weebly', 'Zimbio', 'github', 'TMZ', 'WikiHow', 'Delicious', 'zillow', 'Jimdo', 'goodreads',   
                'Segnalo', 'Netlog', 'Issuu', 'ForumNokia', 'UStream', 'Gamespot', 'MetaCafe', 'askfm', 'hi5', 'JustinTV', 'Blekko', 'Skyrock', 'Cracked', 'foursquare', 'LastFM',   
                'posterous', 'steam', 'Opera', 'Dreamstime', 'Fixya', 'UltimateGuitar', 'docstoc', 'FanPop', 'Break', 'tinyurl', 'Kongregate', 'Disqus', 'Armorgames', 'Behance',   
                'ChaCha', 'CafeMom', 'Liveleak', 'Topix', 'lonelyplanet', 'Stardoll', 'Instructables', 'Polyvore', 'Proboards', 'Weheartit', 'Diigo', 'Gawker', 'FriendFeed',   
                'Videobash', 'Technorati', 'Gravatar', 'Dribbble', 'formspringme', 'myfitnesspal', '500px', 'Newgrounds', 'GrindTV', 'smugmug', 'ibibo', 'ReverbNation', 'Netvibes',   
                'Slashdot', 'Fool', 'Plurk', 'zedge', 'Discogs', 'YardBarker', 'Ebaumsworld', 'sparkpeople', 'Sharethis', 'Xmarks', 'Crunchbase', 'FunnyOrDie,Suite101', 'OVGuide',   
                'Veoh', 'Yuku', 'Experienceproject', 'Fotolog', 'Hotklix', 'Epinions', 'Hyves', 'Sodahead', 'Stylebistro', 'fark', 'AboutMe', 'Metacritic', 'Toluna', 'Mobypicture',   
                'Gather', 'Datpiff', 'mouthshut', 'blogtalkradio', 'Dzone', 'APSense', 'Bigstockphoto', 'n4g', 'Newsvine', 'ColourLovers', 'Icanhazcheezburger', 'Xanga',   
                'InsaneJournal', 'redbubble', 'Kaboodle', 'Folkd', 'Bebo', 'Getsatisfaction', 'WebShots', 'threadless', 'Active', 'GetGlue', 'Shockwave', 'Pbase']

				

def check_user_name(alias):
	
	print("\nComprobrando alias "+alias+" en 160 websites\n")
	
	for service in services:  
		try:    
			res1 = requests.get('http://checkusernames.com/usercheckv2.php?target=' + service + '&username=' + alias, headers={'X-Requested-With':'XMLHttpRequest'}).text
			if 'notavailable' in res1: 
				print (alias + " -> " + service) 
		except Exception as e:
			print(e) 


if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Makes a search on social networks.', prog='check_social_networks.py', epilog="", add_help=False)
	# Adding the main options
	general = parser.add_mutually_exclusive_group(required=True)
	general.add_argument('-a', '--alias', metavar='<alias>', action='store', help='query to be resolved by checkusernames.com.')        
	args = parser.parse_args()        
	check_user_name(args.alias)