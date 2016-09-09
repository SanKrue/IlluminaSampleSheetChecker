#!/usr/bin/env python3
from HiSeqSampleSheetLine import HiSeqSampleSheetLine
from MiSeqSampleSheetLine import MiSeqSampleSheetLine
import cgi, os
import cgitb; cgitb.enable()
import base64

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
   
# printing our message for file uploading in hmtl format with bootstrap css style
print ("""
<html>
<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css">
<body>
   <p>%s</p>
</body>
</html>
""" % (message))

data_error = base64.b64encode(open('cgi-bin/error.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
error = '<img src="data:image/jpeg;base64,%s" width=25 hights=25>' % data_error
	 

# in case the file was successfully uploaded, the file will be proccess directly
if fileitem.filename:
	with open('/tmp/' + fn, "r") as file: # open the file in the temporary folder as "file"
		firstrow = next(file) # store the first row in the variable "firstrow"
		if firstrow[0:4] == "FCID": # if the file is a HISeq SampleSheet, it starts with "FCID,..."
			nwe = os.path.splitext(fileitem.filename) # filename without extension (.csv), "nwe" is a tuple (root, ext)
			name = nwe[0].split('-') # splits the filename (position 0 in the nwe tuple) after "-", 
									 # name format: "Year-Month-Day-FCID"
			FCID = name[3] # we need only the FCID, which is stored at position 3 in "name"
			HiSeqSampleSheetLine.ReadandProcessHiSeq(file, FCID) # call the HISeq function for processing the HISeq SampleSheet, 
															# the parameters are the "file" and the stored FCID 
															# (which we need for the FCID name check)
		elif firstrow.rstrip('\n')[0:8] == "[Header]": # if the file is a MISeq SampleSheet, it starts with "[Header]"
			MiSeqSampleSheetLine.ReadandProcessMiSeq(file) # call the MISeq function for processing the MISeq SampleSheet
		else:
			print("<div class=container><p><h4>%s Not a HISeq or MISeq SampleSheet. </h4>First word in the file should be  					   <b>FCID</b> (in a HiSeq SampleSheet) or <b>[Header]</b> (in a MiSeq SampleSheet)\
				   and not <b>%s</b>.</p> </div>" % (error, firstrow)) # in case there isn't "FCID" or "[Header]" found,
				    												   # the file is not a HISeq or MISeq file
			
