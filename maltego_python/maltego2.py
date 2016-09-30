import requests
import re
import sys

tarurl = sys.argv[1]
response = requests.get(tarurl).text
regex = re.compile(("([a-z0-9!#$%&'*+\/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+\/=?^_`"
                    "{|}~-]+)*(@|\sat\s)(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?(\.|"
                    "\sdot\s))+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?)"))

print"<MaltegoMessage>"
print"<MaltegoTransformResponseMessage>"
print"	<Entities>"
emails = re.findall(regex, response)
for email in emails:
	print"		<Entity Type=\"maltego.EmailAddress\">"
	print"			<Value>"+str(email[0])+"</Value>"
	print"		</Entity>"
print"	</Entities>"
print"</MaltegoTransformResponseMessage>"
print"</MaltegoMessage>"