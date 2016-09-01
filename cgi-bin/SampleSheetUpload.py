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
	 

# in case the file was successfully uploaded, the file will be proccess directly
if fileitem.filename:
	with open('/tmp/' + fn, "r") as file: # open the file in the temporary folder as "file"
		firstrow = next(file) # store the first row in the variable "firstrow"
		if firstrow[0:4] == "FCID": # if the file is a HISeq SampleSheet, it starts with "FCID,..."
			nwe = os.path.splitext(fileitem.filename) # filename without extension (.csv), "nwe" is a tuple (root, ext)
			name = nwe[0].split('-') # splits the filename (position 0 in the nwe tuple) after "-", 
									 # name format: "Year-Month-Day-FCID"
			FCID = name[3] # we need only the FCID, which is stored at position 3 in "name"
			SampleSheetLine.ReadandProcessHISeq(file, FCID) # call the HISeq function for processing the HISeq SampleSheet, 
															# the parameters are the "file" and the stored FCID 
															# (which we need for the FCID name check)
		elif firstrow.rstrip('\n') == "[Header]": # if the file is a MISeq SampleSheet, it starts with "[Header]"
			MISeqSampleSheetLine.ReadandProcessMISeq(file) # call the MISeq function for processing the MISeq SampleSheet
		else:
			print("<p> Not a HISeq or MISeq SampleSheet </p>") # in case there isn't "FCID" or "[Header]" found, the file is
															   # not a HISeq or MISeq file
			
