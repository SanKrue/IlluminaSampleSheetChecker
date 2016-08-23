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

#three icons for check, error and warning should be directly embeded in the file, so they should be encoded with base64
data_check = base64.b64encode(open('cgi-bin/check.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
check = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_check

data_error = base64.b64encode(open('cgi-bin/error.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
error = '<img src="data:image/jpeg;base64,%s" width=25 hights=25>' % data_error

data_warning = base64.b64encode(open('cgi-bin/warning.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
warning = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_warning

def ShowMessage(self): #function for showing errors and warnings as string 
	for item in self:
		messageString = "".join(self)
	return messageString

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
            																	# objects by calling them with their column 																				# number starting with 0
				sampleSheet.append(sampleSheetLineElement)  # putting all objects in the created list "Sample Sheet"
		length = len(sampleSheet)
		counter = 0
		RedundancyTest = []
		SameIndexInLanesTest = []
		SameSampleIDInLaneTest = []
		CompareSampleIDInLanesTest = []
		HammingDistanceForIndicesTest = []
		# two for-loops with i as first line number and j as second line number to compare each line one by one with another line. It 			# will print a warning or error, if the query will get a false from the function defined in the SampleSheet class			
		for i in range(length):
			for j in range(i + 1, length):
				if not(sampleSheet[i].SearchForRedundancy(sampleSheet[j])):
					counter +=1
					RedundancyMessage = "<p> Redundancy in line %s and %s:<br>%s<br>%s</p>" % (str(i + 2), \
									 str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),)
					RedundancyTest.append(RedundancyMessage)
				if not(sampleSheet[i].SameIndexInLane(sampleSheet[j])):
					counter +=1
					SameIndexMessage = "<p> Same Index but different SampleIDs in line %s and %s:<br>%s<br>%s</p>" \
    								      % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),)
					SameIndexInLanesTest.append(SameIndexMessage)
				if not(sampleSheet[i].SameSampleIDInLane(sampleSheet[j])):
					counter +=1
					SameSampleIDInLaneMessage = "<p> Same SampleID but different Indices in line %s and %s:<br>%s<br>%s</p>" \
    								       % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),)   
					SameSampleIDInLaneTest.append(SameSampleIDInLaneMessage)
				if not(sampleSheet[i].CompareSampleIDInLanes(sampleSheet[j])):
					counter +=1
					CompareSampleIDMessage = "<p> Same SampleID, but difference in another parameter. Line %s and %s:<br>%s<br>%s</p>"\
											   % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),)
					CompareSampleIDInLanesTest.append(CompareSampleIDMessage)
				if not(sampleSheet[i].HammingDistanceForIndices(sampleSheet[j])):
					counter +=1
					HammingDistanceMessage = "<p> Distance too small in line %s and %s:<br>%s<br>%s</p>" \
								 		  % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]),)
					HammingDistanceForIndicesTest.append(HammingDistanceMessage)
		if counter == 0: #if the counter is 0, everything is ok and the Successful Testing Messages will be shown
			print("<head><h4>%s Redundancy Test </h4></head>" % (check, ))
			print("<head><h4>%s Matching Test for Index in same lane </h4></head>" % (check, ))
			print("<head><h4>%s Matching Test for SampleIDs in same lane </h4></head>" % (check, ))
			print("<head><h4>%s Matching Test for different lanes </h4></head>" % (check, ))
			print("<head><h4>%s Hamming Distance Test for Indices </h4></head>" % (check, ))
		else: #if we had errors or warnings, a specific message will be shown to find the lane and entry with an error/warning
			if RedundancyTest != []:
				print("<head><h4>%s Redundancy Test: </h4></head> %s" % (warning, ShowMessage(RedundancyTest),))
			else:
				print("<head><h4>%s Redundancy Test </h4></head>" % (check, ))
			if SameIndexInLanesTest != []:
				print ("<head><h4>%s Matching Test for Index in same lane: </h4></head> %s" %  \
				(error, ShowMessage(SameIndexInLanesTest),))
			else:
				print("<head><h4>%s Matching Test for Index in same lane </h4></head>" % (check, ))
			if SameSampleIDInLaneTest != []:
				print ("<head><h4>%s Matching Test for SampleIDs in same lane: </h4></head> %s" % \
				(error, ShowMessage(SameSampleIDInLaneTest),))
			else:
				print("<head><h4>%s Matching Test for SampleIDs in same lane </h4></head>" % (check, ))
			if CompareSampleIDInLanesTest != []:
				print ("<head><h4>%s Matching Test for different lanes: </h4></head> %s" % (error, \
				ShowMessage(CompareSampleIDInLanesTest),))
			else:
				print("<head><h4>%s Matching Test for different lanes </h4></head>" % (check, ))
			if HammingDistanceForIndicesTest != []:
				print ("<head><h4>%s Hamming Distance Test for Indices:</h4></head> %s" % (warning, \
				ShowMessage(HammingDistanceForIndicesTest),)) 
			else:
				print("<head><h4>%s Hamming Distance Test for Indices </h4></head>" % (check, ))
						
