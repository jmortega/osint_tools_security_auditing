import requests
from bs4 import BeautifulSoup
import sys
import time
import argparse

def maltego_domain(domain):
	
	f = open('maltego_domains.mtz','w')
	f.write('<MaltegoMessage>\n')
	f.write('<MaltegoTransformResponseMessage>\n')
	f.write('<Entities>\n')
	
	print("<MaltegoMessage>")
	print("<MaltegoTransformResponseMessage>")
	print("<Entities>")

	response = requests.get(domain).text
	soup = BeautifulSoup(response,'html.parser')
	for line in soup.find_all('a'):
		try:
			newline = line.get('href')
			if newline[:4] == "http":
				f.write('<Entity Type=\"maltego.Domain\">\n')
				f.write('<Value>'+str(newline)+'</Value>\n')
				f.write('</Entity>\n')
				print("<Entity Type=\"maltego.Domain\">") 
				print("<Value>"+str(newline)+"</Value>")
				print("</Entity>")
			elif newline[:1] == "/":
				combline = domain+newline
				f.write('<Entity Type=\"maltego.Domain\">\n')
				f.write('<Value>'+str(combline)+'</Value>\n')
				f.write('</Entity>\n')				
				print("<Entity Type=\"maltego.Domain\">")
				print("<Value>"+str(combline)+"</Value>")
				print("</Entity>")
		except Exception as e:
			pass
		
	f.write('</Entities>\n')
	f.write('</MaltegoTransformResponseMessage>\n')
	f.write('</MaltegoMessage>\n')
	print("</Entities>")	
	print("</MaltegoTransformResponseMessage>")
	print("</MaltegoMessage>")

if __name__ == "__main__":
	parser = argparse.ArgumentParser(description='Makes a maltego file', prog='maltego.py', epilog="", add_help=False)
	# Adding the main options
	general = parser.add_mutually_exclusive_group(required=True)
	general.add_argument('-d', '--domain', metavar='<domain>', action='store', help='query to be resolved.')        
	args = parser.parse_args()
	
	maltego_domain(args.domain)