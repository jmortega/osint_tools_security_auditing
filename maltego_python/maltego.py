import requests
from bs4 import BeautifulSoup
import sys
import time

tarurl = sys.argv[1]
if tarurl[-1] == "/":
	tarurl = tarurl[:-1]
print"<MaltegoMessage>"
print"<MaltegoTransformResponseMessage>"
print"	<Entities>"

response = requests.get(tarurl).text
soup = BeautifulSoup(response,'lxml')
for line in soup.find_all('a'):
	try:
		newline = line.get('href')
		if newline[:4] == "http":
			print"<Entity Type=\"maltego.Domain\">" 
			print"<Value>"+str(newline)+"</Value>"
			print"</Entity>"
		elif newline[:1] == "/":
			combline = tarurl+newline
			print"<Entity Type=\"maltego.Domain\">" 
			print"<Value>"+str(combline)+"</Value>"
			print"</Entity>"
	except Exception,e:
		pass
print"	</Entities>"
print"</MaltegoTransformResponseMessage>"
print"</MaltegoMessage>"