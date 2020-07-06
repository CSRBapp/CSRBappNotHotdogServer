# vim: set ts=8 sts=8 sw=8 tw=0 noet:

import sys

sys.path.append("CSRBbin/pyCSRB/")
from CSRBfuseAPI import *
import time
#from PIL import Image
import os

sys.path.append("hotdog-or-not-hotdog/")
# import the "hotdog-or-not-hotdog" classifier
# NOTE: this is based on on https://github.com/VPanjeta/hotdog-or-not-hotdog, modified to run with OpenCV2 and as a function
from label_dog import *

# open the local CSRB Channel to receive activity execution requests from remote CSRBnodes
h = CSRBmessageOpen(os.path.expanduser("~/CSRBVFS/MESSAGE/00000000000000000000000000000000/5EF25423F787C644"));

while True:
	ret,m = CSRBmessageReceive(h)

	if ret < 0:
		break

	if m is None:
		#print("EMPTY")
		time.sleep(0.1)
		continue

	print("Received message: " + str(m))

	# calculate the number of Objects used to store the image file
	fileBlocks = math.ceil(m.header.params[1].num / 32768)

	# open the block of Objects from the REMOTE CSRBnode's CSRBdb, as a virtual local file
	localFile = os.path.expanduser("~/CSRBVFS/OBJECTBLOCK/" + \
		str(m.header.params[0].id) + "/" + \
		str(m.header.params[1].id) + m.header.params[1].numHexBlocks(32768))

	print("File: " + localFile)

	print("FileSize: " + str(m.header.params[1].num))
	print("FileBlocks: " + str(fileBlocks))

	# pass the local file to the image classifier
	try:
		r = label_dog(localFile)
		print(r)
	except:
		print("IMAGE DETECTION FAILED")
		r = [0, 0]

	#im = Image.open(localFile)
	#im.show()
	#os.system("qiv " + localFile + " &")

	# open a CSRB Channel to the remote CSRBnode's address and Channel ID
	rh = CSRBmessageOpen(os.path.expanduser("~/CSRBVFS/MESSAGE/" +
		str(m.header.params[0].id) + "/" +
		format(m.header.params[0].num, '0>16X')))
	if rh == None:
		continue

	# assemble a simple Message with the image recognition result
	rm = CSRBprotocolMessage()
	rm.header.params[0].num = r[1]

	# send the Message to the CSRBnode that requested the activity
	CSRBmessageSend(rh, rm)

	# clean-up
	CSRBmessageClose(rh)

	# rinse, repeat

# cleanup
CSRBmessageClose(h)

