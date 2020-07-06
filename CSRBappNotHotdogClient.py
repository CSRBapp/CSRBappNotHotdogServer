# vim: set ts=8 sts=8 sw=8 tw=0 noet:

import time
import os
import sys
import shutil

sys.path.append("CSRBbin/pyCSRB/")
from CSRBfuseAPI import *

NODEID = sys.argv[1]
PROCESSORNODEID = sys.argv[2]
IMAGEFILENAME = sys.argv[3]
CSRBVFS = os.environ.get("CSRBVFS", "/mnt/CSRB")

# open the local CSRB Channel to receive the result
print("Opening Local CSRB Channel")
channelLocal = CSRBmessageOpen(CSRBVFS + "/MESSAGE/00000000000000000000000000000000/5EF25423F787C644");

# open the remote CSRB Channel to send the image processing command
print("Opening Remote CSRB Channel")
channelRemote = CSRBmessageOpen(CSRBVFS + "/MESSAGE/" + PROCESSORNODEID + "/5EF25423F787C644");

imageSize = os.stat(IMAGEFILENAME).st_size
imageSizeObjects = math.ceil(imageSize / 32768)
print("Image size: %u bytes, %u OBJECTs" % (imageSize, imageSizeObjects))

imageOBJECTBLOCK = "5EF25423F787C6445EF25423F787C644" + "{:08X}".format(imageSizeObjects)
print("Image's OBJECTBLOCK: %s" % imageOBJECTBLOCK)

print("Copying image [%s] to OBJECTBLOCK [%s]" % (IMAGEFILENAME, imageOBJECTBLOCK))
shutil.copyfile(IMAGEFILENAME, CSRBVFS + "/OBJECTBLOCK/00000000000000000000000000000000/" + imageOBJECTBLOCK)

print("Assembling CSRB message")
messageSend = CSRBprotocolMessage()
# set out local Message Channel to receive the response
messageSend.header.params[0].id.fromHexString(NODEID)
messageSend.header.params[0].num = int("5EF25423F787C644", 16)
# set the local OBJECTBLOCK address where the image is stored
messageSend.header.params[1].id.fromHexString("5EF25423F787C6445EF25423F787C644")
# set the size of the image
messageSend.header.params[1].num = imageSize;
print(messageSend)

print("Sending CSRB message")
CSRBmessageSend(channelRemote, messageSend)

print("Waiting for response CSRB message")
messageReceive = None
while messageReceive is None:
	time.sleep(0.250)
	ret, messageReceive = CSRBmessageReceive(channelLocal)
	if ret < 0:
		print("ERROR")
		sys.exit(1)

print("Received CSRB message")
print(messageReceive)

CSRBmessageClose(channelRemote)
CSRBmessageClose(channelLocal)

print("***")
if messageReceive.header.params[0].num == 1:
	print("HOTDOG")
else:
	print("NOT HOTDOG")
print("***")
