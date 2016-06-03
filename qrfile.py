#!/usr/bin/env python
from qrcode import QRCode,constants
from base64 import b64encode
from zlib import compress
from urllib import quote as urlencode
from hashlib import md5

def qrstring(s):
	qr = QRCode(error_correction=constants.ERROR_CORRECT_L, box_size=25,border=0)
	qr.add_data(s)
	qr.make()
	return qr

def qrimage(s):
	qr = qrstring(s)
	return qr.make_image()

def qrimagefile(s, fileName):
	qrimage(s).save(fileName, 'PNG')
	return fileName

def md5_str(s):
	x = md5()
	x.update(s)
	return x.hexdigest()

def qrfile(filepath, filehash, tmppath="tmp/"):
	data = b64encode(compress(open(filepath, 'r').read(), 9))
	template = 'http://qrfile.kilobyt.es/import/%s/%s/%s/?data=%s'
	chunk = 0
	files = []
	while True:
		datapiece = data[chunk*1024:chunk*1024+1024]
		thisqr = template % (filehash[0:8], hex(chunk)[2:], md5_str(datapiece), urlencode(datapiece))
		f = open('./urls.txt', 'a'); f.write(thisqr+"\n"); f.close()
		img = qrimage(thisqr)
		img.save(tmppath+"qr%s.png" % str(chunk), 'PNG')
		files.append(tmppath+"qr%s.png" % str(chunk))
		#print "Stored %s of %s" % (chunk*1024, len(data))
		chunk+=1
		if len(datapiece)<1024:
				break
	return files

if __name__ == "__main__":
	from sys import argv
	print qrfile(argv[1])