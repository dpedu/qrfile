#!/usr/bin/env python
from qrfile import qrfile,qrimagefile
from pdffile import pdffile
from sys import argv,exit
from os import unlink
import os.path
from json import dumps
from hashlib import md5
from datetime import datetime
from urllib import quote as urlencode
from os.path import getsize

if not len(argv)==3:
	print "Specify an input file and output pdf like: ./run.py wallet.dat output.pdf"
	exit(0)

# Calculate file hash
filehash = md5()
f = open(argv[1], 'r')
while True:
	data = f.read(1024*1024)
	if not data:
		break
	filehash.update(data)
filehash=filehash.hexdigest()

# create info-qr
fileInfo = {
	"name":argv[1],
	"hash":filehash,
	"date":str(datetime.now()),
	"size":getsize(argv[1]),
	"pieces":0
}

# Covert file to many QR codes
files = qrfile(argv[1], fileInfo["hash"])

# Insert pieces info now that we have it
fileInfo["pieces"] = len(files)

# Create info QR code
infoUrl = 'http://qrfile.kilobyt.es/import/?data='+urlencode(dumps(fileInfo))
f = open('./urls.txt', 'a'); f.write(infoUrl+"\n\n\n"); f.close()
qrimagefile(infoUrl, 'tmp/info.png')
print infoUrl

# Embed QR codes indo PDF
#      img list, output name, original file name, info qr
pdffile(files, argv[2], os.path.basename(argv[1]), 'tmp/info.png')

# Delete temp files
for item in files:
	unlink(item)
unlink('tmp/info.png')
