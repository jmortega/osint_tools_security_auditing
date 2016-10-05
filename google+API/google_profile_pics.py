import requests
import json
import argparse

def obtain_google_pics(target):
	
	GOOGLE_API_KEY = "AIzaSyDDnc-68uaF-E4gzvJslt1fppiUl9dyTrc"
	
	token = ""
	loops = 0
		
	while loops < 10:
		api_response = requests.get("https://www.googleapis.com/plus/v1/people?query="+target+"&key="+GOOGLE_API_KEY+"&maxResults=50&pageToken="+token)
		
		json_response = api_response.json()
		token = json_response['nextPageToken']
		if len(json_response['items']) == 0:
			break
		
		for result in json_response['items']:
			name = result['displayName']
			print(name.encode('utf-8'))
			image = result['image']['url'].split('?')[0]
			f = open('images/'+name+'.jpg','wb+')
			f.write(requests.get(image).content)
			f.close()
		loops+=1
	

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='gets profile pics.', prog='google_profile_pics.py', epilog="", add_help=False)
	# Adding the main options
	general = parser.add_mutually_exclusive_group(required=True)
	general.add_argument('-t', '--target', metavar='<target>', action='store', help='target to be resolved.')
	args = parser.parse_args()
	    
	obtain_google_pics(args.target)
	    