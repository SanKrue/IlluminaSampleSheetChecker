#!/usr/bin/env python3
from SampleSheetLine import SampleSheetLine
from MISeqSampleSheetLine import MISeqSampleSheetLine
import cgi, os
import cgitb; cgitb.enable()

form = cgi.FieldStorage()


# Get filename here
fileitem = form['filename']

# Test if the file was uploaded
if fileitem.filename:
   # strip leading path from file name to avoid 
   # directory traversal attacks
   fn = os.path.basename(fileitem.filename)
   open('/tmp/' + fn, 'wb').write(fileitem.file.read()) # open temporary folder and store a copy of the file in it

   message = 'The file "<b>' + fn + '</b>" was uploaded successfully'
   
else:
   message = 'No file was uploaded'
   
# printing our message for file uploading   
print ("""\
Content-Type: text/html\n
<html>
<body>
   <p>%s</p>
</body>
</html>
""" % (message))
	 

# in case the file was successfully uploaded, the file would be proccess directly
if fileitem.filename:
	with open('/tmp/' + fn, "r") as file:
		firstrow = next(file)
		if firstrow[0:4] == "FCID": # if the file is a HISeq SampleSheet, it starts with "FCID,..."
			nwe = os.path.splitext(fileitem.filename) #filename without extension (.csv), nwe is a tuple (root, ext)
			name = nwe[0].split('-') #splits the filename (position 0 in the nwe tuple) after "-", name format: "Year-Month-Day-FCID"
			FCID = name[3]
			SampleSheetLine.ReadandProcessHISeq(file, FCID)
#		elif firstrow[0] == "[": # if the file is a MISeq SampleSheet, it starts with "[Header]"
		elif firstrow.rstrip('\n') == "[Header]": # if the file is a MISeq SampleSheet, it starts with "[Header]"
			MISeqSampleSheetLine.ReadandProcessMISeq(file)
		else:
			print("<p> Not a HISeq or MISeq SampleSheet </p>")
			
