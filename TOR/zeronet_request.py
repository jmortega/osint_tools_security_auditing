import sys

import deepify
except:
    print "deepify library not found, please install it before proceeding\n"
    print "pip install deepify\n"
    sys.exit()

# Check that you have the Zeronet service running
from deepify.zeronet import Zeronet

url = "1HeLLo4uzjaLetFx6NH3PMwFP3qbRbTf3D"
# Creating the wrapper instance
zeronetwrapper = Zeronet()
data = zeronetwrapper.getResponse(url)
print data