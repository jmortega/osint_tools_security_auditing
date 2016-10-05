import requests
import re
import sys
import argparse

def maltego_emails(domain):
	response = requests.get(domain).text
	regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

	print("<MaltegoMessage>")
	print("<MaltegoTransformResponseMessage>")
	print("	<Entities>")
	emails = re.findall(regex, response)
	for email in emails:
		print("<Entity Type=\"maltego.EmailAddress\">")
		print("<Value>"+str(email[0])+"</Value>")
		print("</Entity>")
	print("</Entities>")
	print("</MaltegoTransformResponseMessage>")
	print("</MaltegoMessage>")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Makes a maltego file', prog='maltego_emails.py', epilog="", add_help=False)
	# Adding the main options
	general = parser.add_mutually_exclusive_group(required=True)
	general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved.')        
	args = parser.parse_args()
	
	maltego_emails(args.domain)