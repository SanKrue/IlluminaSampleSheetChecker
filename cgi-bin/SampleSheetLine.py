import operator
from collections import defaultdict
import base64

class SampleSheetLine:
	# the objects in class SampleSheetLine have to have 10 parameters, which were store in SampleSheet files
	def __init__(self, Fcid, Lane, SampleID, SampleRef, Index, Description, Control, Recipe, Operator, SampleProject):
		self.l = [Fcid, Lane, SampleID, SampleRef, Index, Description, Control, Recipe, Operator, SampleProject]
		self.Fcid = Fcid
		self.Lane = Lane
		self.SampleID = SampleID
		self.Index = Index
		self.SampleRef = SampleRef
		self.Description = Description
		self.Control = Control
		self.Recipe = Recipe
		self.Operator = Operator
		self.SampleProject = SampleProject
	# a representation of the objects, which are here a kind of tuples in an array
	def __repr__(self):
		return "(" + str(self.SampleID) + ", " + str(self.Index) + ", " + str(self.Fcid) + ", " + str(self.Lane) + \
			   ", " + str(self.SampleRef) + ", " + str(self.Description) + ", " + str(self.Control) + ", " + \
			   str(self.Recipe) + ", " + str(self.Operator)+ ", " + str(self.SampleProject) + ")"
	# functions for getting the items in the SampleSheet
	def getFcid(self):
		return self.Fcid
	def getLane(self):
		return self.Lane
	def getSampleID(self):
		return self.SampleID
	def getSampleRef(self):
		return self.SampleRef
	def getIndex(self):
		return self.Index
	def getDescription(self):
		return self.Description
	def getControl(self):
		return self.Control
	def getRecipe(self):
		return self.Recipe
	def getOperator(self):
		return self.Operator
	def getSampleProject(self):
		return self.SampleProject

	# function that search for redundancy in the SampleSheet, which means lane, SampleID and Index are the
	# same in two different lines of the file
	def SearchForRedundancy(self, otherSampleSheetLine):
	   if (self.Lane, self.SampleID, self.Index) == \
		   (otherSampleSheetLine.Lane, otherSampleSheetLine.SampleID, otherSampleSheetLine.Index):
		   return False
	   else:
		   return True

	# function that compare the Indices in the same lane in different lines of the file;
	# same Indices but different SampleIDs in the same lane will give a False
	def SameIndexInLane(self, otherSampleSheetLine):
		if ((self.Lane == otherSampleSheetLine.Lane) and \
			(self.Index == otherSampleSheetLine.Index)  and \
			(self.SampleID != otherSampleSheetLine.SampleID)):
			return False
		else:
			return True
			
	# function that compare the SampleIDs in the same lane in different lines of the file;
	# same SampleID but different Index in the same lane will give a False		
	def SameSampleIDInLane(self, otherSampleSheetLine):
		if ((self.Lane == otherSampleSheetLine.Lane) and \
			(self.Index != otherSampleSheetLine.Index)  and \
			(self.SampleID == otherSampleSheetLine.SampleID)):
			return False
		else:
			return True

	# function that compare parameters in different lanes, so the function will take two different lanes and have a look
	# for same SampleID, but difference in another parameter, e.g. SampleProject Number
	def CompareSampleIDInLanes(self, otherSampleSheetLine):
		if ((self.Lane != otherSampleSheetLine.Lane) and \
			(self.SampleID == otherSampleSheetLine.SampleID)) and \
			((self.Index != otherSampleSheetLine.Index) or \
			(self.Fcid != otherSampleSheetLine.Fcid) or \
			(self.SampleRef != otherSampleSheetLine.SampleRef) or \
			(self.Description != otherSampleSheetLine.Description) or \
			(self.Control != otherSampleSheetLine.Control) or \
			(self.Recipe != otherSampleSheetLine.Recipe) or \
			(self.Operator != otherSampleSheetLine.Operator) or \
			(self.SampleProject != otherSampleSheetLine.SampleProject)):
			return False
		else:
			return True

	# function which calculate the Hamming Distance between two Indices in the same lane and gives a warning, if it
	# is smaller than 2, e.g. AACGTG and ACCGTG
	def HammingDistanceForIndices(self, otherSampleSheetLine):
		if (self.Lane == otherSampleSheetLine.Lane):
			index1 = self.Index
			index2 = otherSampleSheetLine.Index
			ne = operator.ne
			diffs = sum(list(map(ne, index1, index2)))
			if diffs < 2:
				return False
			else:
				return True
		return True

	# check, if the FCID in the filename and inside the file are identical	
	def CompareFCIDinNameandFile(self,FCID): 
		if (str(self.Fcid) != FCID):
			return False
		else:
			return True
			
	# main function, read and process a HISeq SampleSheet
	def ReadandProcessHISeq(self, FCID): # parameters are the file (here represented as "self") and the FCID from the filename, 
										 # which we get in our main skript 
		sampleSheet = []
		fwc = filter(lambda row: row[0] != '#', self)  # fcw = file without comments --> ignore lines which start with '#'
		for item in fwc:  # for each line in file
			line = item.strip()  # remove whitespace from beginning or end of the line
			if(len(line) > 0):  # length of the line should be >0
				splitLine = line.split(",")  # the items will split with the ',' as separator, because we have 									 			 # a .csv file
				sampleSheetLineElement = SampleSheetLine(splitLine[0], splitLine[1], splitLine[2], splitLine[3], \
													 splitLine[4], splitLine[5], splitLine[6], splitLine[7], \
													 splitLine[8], splitLine[9])# getting all items as SampleSheetLine
																				# objects by calling them with their column 																				# number starting with 0
				sampleSheet.append(sampleSheetLineElement)  # putting all objects in the created list "Sample Sheet"
				
		length = len(sampleSheet)
		
		# we want to create an overview how many samples are in each lane and display the result in a small table at the beginning
		# therefor we create a dictionary where each lane number is the key, which gets one value (the number of samples
		# in this lane)
		lanes = defaultdict(int) # group a sequence of key-value pairs into a dictionary of ints, for every new key a function
								 # in the datatyp "defaultdict" creates automatically an entry and returns an int (the value, 0) 
		for i in range(length):
			lanes[int(sampleSheet[i].Lane)] += 1 # for every entry with the same key (the Lanes), the value will be incremented
		keys = list(lanes.keys()) # list of lane numbers
		values = list(lanes.values()) # list of nnumber of samples
		

		# html style for creating the table with two rows "lane" and "no. samples" and as many columns as lanes
		print("<style> table, td, th { padding: 5px; border: 1px solid black; border-collapse: collapse;} </style>")
		print("<table> <caption><br><b>Number of samples in lane</b></caption>")
		print("<tr><th>lane</th>")
		for j in range(len(lanes)):
			print ("<td>%i</td>" % (keys[j]))
		print("</tr><tr><th>no. samples </th></th>")
		for j in range(len(lanes)):
			print ("<td>%i</td>" % (values[j]))
		print("</tr> </table>")
		
		# three icons for check, error and warning should be directly embeded in the file, so they should be encoded with base64
		data_check = base64.b64encode(open('cgi-bin/check.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
		check = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_check

		data_error = base64.b64encode(open('cgi-bin/error.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
		error = '<img src="data:image/jpeg;base64,%s" width=25 hights=25>' % data_error

		data_warning = base64.b64encode(open('cgi-bin/warning.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
		warning = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_warning
		
		# we create a counter and lists for each test, so we can append the specific error messages in one list
		counter = 0
		FCIDTest = []
		RedundancyTest = []
		SameIndexInLanesTest = []
		SameSampleIDInLaneTest = []
		CompareSampleIDInLanesTest = []
		HammingDistanceForIndicesTest = []
		# two for-loops with i as first line number and j as second line number to compare each line one by one with another 			# line. It will increment the counter and append our defined warning or error message to the specific list, if the query 		    # will get a false from the function defined in the SampleSheetLine class			
		for i in range(length):
			if not (sampleSheet[i].CompareFCIDinNameandFile(FCID)): # checking FCID in filename and FCID inside the file in 																	# each line
				counter +=1
				FCIDMessage = "<p> FCID in filename: %s <br> FCID in file (line %s): %s </p>" % (FCID, str(i + 2), \
								str(sampleSheet[i].Fcid))
				FCIDTest.append(FCIDMessage)
			for j in range(i + 1, length): # starting with the compare line (i) one by one with another line (j) tests		
				if not(sampleSheet[i].SearchForRedundancy(sampleSheet[j])):
					counter +=1
					RedundancyMessage = "<p> Redundancy in line %s and %s:<br>%s<br>%s</p>" % (str(i + 2), \
									 str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]))
					RedundancyTest.append(RedundancyMessage)
				if not(sampleSheet[i].SameIndexInLane(sampleSheet[j])):
					counter +=1
					SameIndexMessage = "<p> Same Index but different SampleIDs in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]))
					SameIndexInLanesTest.append(SameIndexMessage)
				if not(sampleSheet[i].SameSampleIDInLane(sampleSheet[j])):
					counter +=1
					SameSampleIDInLaneMessage = "<p> Same SampleID but different Indices in line %s and %s:<br>%s<br>%s</p>" \
										   % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]))   
					SameSampleIDInLaneTest.append(SameSampleIDInLaneMessage)
				if not(sampleSheet[i].CompareSampleIDInLanes(sampleSheet[j])):
					counter +=1
					CompareSampleIDMessage = "<p> Same SampleID, but difference in another parameter. Line %s and %s:\
											<br>%s<br>%s</p>" % (str(i + 2), str(j + 2), str(sampleSheet[i]), \
											str(sampleSheet[j]))
					CompareSampleIDInLanesTest.append(CompareSampleIDMessage)
				if not(sampleSheet[i].HammingDistanceForIndices(sampleSheet[j])):
					counter +=1
					HammingDistanceMessage = "<p> Distance too small in line %s and %s:<br>%s<br>%s</p>" \
								 		  % (str(i + 2), str(j + 2), str(sampleSheet[i]), str(sampleSheet[j]))
					HammingDistanceForIndicesTest.append(HammingDistanceMessage)
					
		if counter == 0: # if the counter is 0, everything is ok and the Successful Testing Messages will be shown
			print("<head><h3><br>SampleSheetTest Result:</h3></head>")
			print("<head><h4>%s FCID Name Test </h4></head>" % (check))
			print("<head><h4>%s Redundancy Test </h4></head>" % (check))
			print("<head><h4>%s Matching Test for Index in same lane </h4></head>" % (check))
			print("<head><h4>%s Matching Test for SampleIDs in same lane </h4></head>" % (check))
			print("<head><h4>%s Matching Test for different lanes </h4></head>" % (check))
			print("<head><h4>%s Hamming Distance Test for Indices </h4></head>" % (check))
		else: # if we had errors or warnings, a specific message will be shown to find the lane and entry with an error/warning
			print("<head><h3><br>SampleSheetTest Result:</h3></head>")
			if FCIDTest != []:
				print("<head><h4>%s FCID Name Test: </h4></head> %s" % (warning, "".join(FCIDTest)))
			else:
				print("<head><h4>%s FCID Name Test </h4></head>" % (check))			
			if RedundancyTest != []:
				print("<head><h4>%s Redundancy Test: </h4></head> %s" % (warning, "".join(RedundancyTest)))
			else:
				print("<head><h4>%s Redundancy Test </h4></head>" % (check))
			if SameIndexInLanesTest != []:
				print ("<head><h4>%s Matching Test for Index in same lane: </h4></head> %s" %  \
				(error, "".join(SameIndexInLanesTest)))
			else:
				print("<head><h4>%s Matching Test for Index in same lane </h4></head>" % (check))
			if SameSampleIDInLaneTest != []:
				print ("<head><h4>%s Matching Test for SampleIDs in same lane: </h4></head> %s" % \
				(error, "".join(SameSampleIDInLaneTest)))
			else:
				print("<head><h4>%s Matching Test for SampleIDs in same lane </h4></head>" % (check))
			if CompareSampleIDInLanesTest != []:
				print ("<head><h4>%s Matching Test for different lanes: </h4></head> %s" % (error, \
				"".join(CompareSampleIDInLanesTest)))
			else:
				print("<head><h4>%s Matching Test for different lanes </h4></head>" % (check))
			if HammingDistanceForIndicesTest != []:
				print ("<head><h4>%s Hamming Distance Test for Indices:</h4></head> %s" % (warning, \
				"".join(HammingDistanceForIndicesTest))) 
			else:
				print("<head><h4>%s Hamming Distance Test for Indices </h4></head>" % (check))


