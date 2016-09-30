import sys

try:
    import deepify
except:
    print "deepify library not found, please install it before proceeding\n"
    print "pip install deepify\n"
    sys.exit()

# Check that you have the Tor Browser running!
from deepify.tor import Tor


url = "http://3g2upl4pq6kufc4m.onion/"
# Creating the wrapper instance
torwrapper = Tor()
data = torwrapper.getResponse(url)
print data