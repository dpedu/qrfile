#!/usr/bin/env python
from PyPDF2 import PdfFileWriter, PdfFileReader
from reportlab.pdfgen import canvas
from StringIO import StringIO

# width  595 units
# height 841 units

def pdffile(imagelist, outputfilename, originalFileName, infoFile):
	positions=[
		[5,330],
		[300, 330],
		[5,5],
		[300,5]
	]
	
	# number of QR codes
	totalPieces = len(imagelist)
	currentPiece=1
	
	# PDF document is created here
	pdf = PdfFileWriter()
	
	while len(imagelist)>0:
		# Get the first 4 images from the array
		tmpImageList = []
		while len(tmpImageList)<len(positions):
			try:
				tmpImageList.append(imagelist.pop(0))
			except IndexError:
				break
		
		# Start making a page
		imgTemp = StringIO()
		imgDoc = canvas.Canvas(imgTemp)
		
		# 4 qr's per page, so per each position
		for pos in positions:
			# Get the image name
			try:
				img = tmpImageList.pop(0)
			except IndexError:
				break
			# Draw the QR
			imgDoc.drawImage(img, 0+pos[0], 0+pos[1], 290, 290)
			# Draw the label
			imgDoc.drawString(0+pos[0],0+pos[1]+300, "%s :: %s of %s "%(originalFileName, currentPiece, totalPieces))
			# Increment # of pieces drawn
			currentPiece+=1
		
		# Add logo
		#imgDoc.drawImage('lib/qr_app_info.png', 5, 686, 150, 150)
		
		# Add info code
		imgDoc.drawImage(infoFile, 5, 676, 150, 150)
		
		imgDoc.setFont("Helvetica-Bold", 12)
		imgDoc.drawString(47,830, "SCAN ME")
		
		# Add instructions
		imgDoc.setFont("Helvetica-Bold", 18)
		imgDoc.drawString(170,820, "What is this?")
		imgDoc.drawString(170,754, "Instructions:")
		
		imgDoc.setFont("Helvetica", 12)
		imgDoc.drawString(170, 800, "The images below are pieces of a file encoded into QR codes scannable by")
		imgDoc.drawString(170, 788, "smartphones. Scan the smaller QR code to the right for details about retrieving")
		imgDoc.drawString(170, 776, "this file.")
		imgDoc.drawString(170, 734, "1) Scan the image to the right and press Import.")
		imgDoc.drawString(170, 722, "2) Scan in all available data QR codes.")
		imgDoc.drawString(170, 710, "3) Download your file!")
		
		# Save the page
		imgDoc.save()
		
		# Add page to master doc
		page = PdfFileReader(StringIO(imgTemp.getvalue())).getPage(0)
		pdf.addPage(page)
		#break
	
	# Export master doc
	pdf.write(file(outputfilename,"w"))
