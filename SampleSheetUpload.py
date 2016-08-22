#!/usr/bin/env python3
from SampleSheet import SampleSheetLine
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

   message = 'The file "' + fn + '" was uploaded successfully'
   	
   
else:
   message = 'No file was uploaded'
   
print ("""\
Content-Type: text/html\n
<html>
<body>
   <p>%s</p>
</body>
</html>
""" % (message,))

#the three icons for check, error and warning should be directly embeded in the file, so they should be encoded with base64
data_check = base64.b64encode(open('cgi-bin/check.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
check = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_check

data_error = base64.b64encode(open('cgi-bin/error.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
error = '<img src="data:image/jpeg;base64,%s" width=25 hights=25>' % data_error

data_warning = base64.b64encode(open('cgi-bin/warning.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
warning = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_warning

# in case the file was successfully uploaded, the file would be proccess directly
if fileitem.filename:
	with open('/tmp/' + fn, "r") as file:
		next(file)  # ignore the first line
		sampleSheet = []
		fwc = filter(lambda row: row[0] != '#', file)  # fcw=file without comments --> ignore lines which start with '#'
		for item in fwc:  # for each line in file
			line = item.strip()  # remove whitespace from beginning or end of the line
			if(len(line) > 0):  # length of the line should be >0
				splitLine = line.split(",")  # the items will split with the ',' as separator, because we have 								     # a .csv file
				sampleSheetLineElement = SampleSheetLine(splitLine[0], splitLine[1], splitLine[2], splitLine[3], \
                                                     splitLine[4], splitLine[5], splitLine[6], splitLine[7], \
                                                     splitLine[8], splitLine[9])# getting all items as SampleSheetLine
            									# objects by calling them with their column 											# number starting with 0
				sampleSheet.append(sampleSheetLineElement)  # putting all objects in the created list "Sample 										    # Sheet"
		length = len(sampleSheet)
		failure = False #variable which turned into True, if the program will find an error or warning
    		# two for-loops with i as first line number and j as second line number to compare each line one by one 		# with another line. It will print a warning or error, if the query will get a false from the function defined in 			# the SampleSheet class	
		for i in range(length):
			for j in range(i + 1, length):
				if not(sampleSheet[i].SearchForRedundancy(sampleSheet[j])):
					failure = True
					print ("""\
					<html>
					<head><h4>Redundancy Test:</h4></head>
					<body>
   						<p> %s Redundancy in line %s and %s:<br>%s<br>%s</p>
					</body>
					</html>
					""" % (warning, str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),))
				if not(sampleSheet[i].CompareIndexInLane(sampleSheet[j])):
					failure = True
					print ("""\
					<html>
					<head><h4>Matching Test for same lane:</h4></head>
					<body>
   						<p> %s Same Index but different SampleIDs in line %s and %s:<br>%s<br>%s</p>
					</body>
					</html>
					""" % (error, str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),))
				elif not(sampleSheet[i].CompareIndexInLane(sampleSheet[j])):
					failure = True
					print ("""\
					<html>
					<head><h4>Matching Test for same lane:</h4></head>
					<body>
   						<p> %s Same SampleID but different Indices in line %s and %s:<br>%s<br>%s</p>
					</body>
					</html>
					""" % (error, str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),))
				if not(sampleSheet[i].CompareSampleIDInLanes(sampleSheet[j])):
					failure = True
					print ("""\
					<html>
					<head><h4>Matching Test for different lanes:</h4></head>
					<body>
   						<p> %s Same SampleID but different Indices in line %s and %s:<br>%s<br>%s</p>
					</body>
					</html>
					""" % (error, str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),))
				if not(sampleSheet[i].HammingDistanceForIndices(sampleSheet[j])):
					failure = True
					print ("""\
					<html>
					<head><h4>Hamming Distance Test for Indices:</h4></head>
					<body>
   						<p> %s Distance too small in line %s and %s:<br>%s<br>%s</p>
					</body>
					</html>
					""" % (warning, str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),))
		if not failure:
			print ("""\
			<html>
			<head><h4>File successfully tested:</h4></head>
			<body>
				<p> %s No Error or Warning</p>
			</body>			
			</html>
			""" % (check,))
					
