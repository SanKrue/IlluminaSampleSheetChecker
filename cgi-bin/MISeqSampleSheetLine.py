import operator
import base64

class MISeqSampleSheetLine:
	# the objects in class MISeqSampleSheetLine have to have 10 parameters, which were store in SampleSheet files
	def __init__(self, Sample_ID, Sample_Name, Sample_Plate, Sample_Well, I7_index_ID, index, I5_index_ID, index2, \
			Sample_Project, Description):
		self.l = [Sample_ID, Sample_Name, Sample_Plate, Sample_Well, I7_index_ID, index, I5_index_ID, index2, Sample_Project,\
				 Description]
		self.Sample_ID = Sample_ID
		self.Sample_Name = Sample_Name
		self.Sample_Plate = Sample_Plate
		self.Sample_Well = Sample_Well
		self.I7_index_ID = I7_index_ID
		self.index = index
		self.I5_index_ID = I5_index_ID
		self.index2 = index2
		self.Sample_Project = Sample_Project
		self.Description = Description
	# a representation of the objects, which are here a kind of tuples in an array
	def __repr__(self):
		return "(" + str(self.Sample_ID) + ", " + str(self.Sample_Name) + ", " + str(self.Sample_Plate) + \
			   ", " + str(self.Sample_Well) + ", " + str(self.I7_index_ID) + ", " + str(self.index) + ", " + \
			   str(self.I5_index_ID) + ", " + str(self.index2)+ ", " + str(self.Sample_Project) + ", " + str(self.Description) + ")"
	# functions for getting the items in the SampleSheet
	def getSample_Name(self):
		return self.Sample_Name
	def getSample_Plate(self):
		return self.Sample_Plate
	def getSample_ID(self):
		return self.Sample_ID
	def getSample_Well(self):
		return self.Sample_Well
	def getindex(self):
		return self.index
	def getDescription(self):
		return self.Description
	def getI7_index_ID(self):
		return self.I7_index_ID
	def getI5_index_ID(self):
		return self.I5_index_ID
	def getindex2(self):
		return self.index2
	def getSample_Project(self):
		return self.Sample_Project

	# function that search for redundancy in the SampleSheet, which means Sample_ID, I7_index_ID, index, I5_index_ID,
	# index2 are the same in two different lines of the file
	def SearchForRedundancy(self, otherSampleSheetLine):
	   if (self.Sample_ID, self.I7_index_ID, self.index, self.I5_index_ID, self.index2) == \
		   (otherSampleSheetLine.Sample_ID, otherSampleSheetLine.I7_index_ID, otherSampleSheetLine.index, \
			otherSampleSheetLine.I5_index_ID, otherSampleSheetLine.index2):
		   return False
	   else:
		   return True

	# functions which compare the different Indices (index and index2) respectively Index_Ids in the in different
	# lines of the file;e.g. same index but different I7_index_ID will give a False
	def CompareI7_Index(self, otherSampleSheetLine):
		if ((self.I7_index_ID == otherSampleSheetLine.I7_index_ID) and \
			(self.index != otherSampleSheetLine.index)):
			return False
		else:
			return True

	def Compareindex(self, otherSampleSheetLine):
		if ((self.I7_index_ID != otherSampleSheetLine.I7_index_ID) and \
			(self.index == otherSampleSheetLine.index)):
			return False
		else:
			return True

	def CompareI5_Index(self, otherSampleSheetLine):
		if ((self.I5_index_ID == otherSampleSheetLine.I5_index_ID) and \
			(self.index2 != otherSampleSheetLine.index2)):
			return False
		else:
			return True

	def Compareindex2(self, otherSampleSheetLine):
		if ((self.I5_index_ID != otherSampleSheetLine.I5_index_ID) and \
			(self.index2 == otherSampleSheetLine.index2)):
			return False
		else:
			return True

	# function which calculate the Hamming Distance between two Indices with the same I7_index_ID and gives a warning,
	# if it is smaller than 2, e.g. TGAACCTT and TGAACCTG
	def HammingDistanceForindex(self, otherSampleSheetLine):
		if (self.I7_index_ID == otherSampleSheetLine.I7_index_ID):
			index1 = self.index2
			index2 = otherSampleSheetLine.index2
			ne = operator.ne
			diffs = sum(list(map(ne, index1, index2)))
			if diffs < 2:
				return False
			else:
				return True
		return True
	
	#mainfunction, read and process a MISeq SampleSheet	
	def ReadandProcessMISeq(self):
		sampleSheet = []
		for item in (self):
			if "[Data]" in item:
				break
		for item in (self):
			line = item.strip()  # remove whitespace from beginning or end of the line
			if(len(line) > 0):  # length of the line should be >0
				splitLine = line.split(",")  # the items will split with the ',' as separator, because we have a .csv file
				sampleSheetLineElement = MISeqSampleSheetLine(splitLine[0], splitLine[1], splitLine[2], splitLine[3], \
														 splitLine[4], splitLine[5], splitLine[6], splitLine[7], \
														 splitLine[8], splitLine[9])  # getting all items as MISeqSampleSheetLine
				# objects by calling them with their column number starting with 0
				sampleSheet.append(sampleSheetLineElement) # putting all objects in the created list "Sample Sheet"
		length = len(sampleSheet)
		
		# three icons for check, error and warning should be directly embeded in the file, so they should be encoded with base64
		data_check = base64.b64encode(open('cgi-bin/check.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
		check = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_check

		data_error = base64.b64encode(open('cgi-bin/error.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
		error = '<img src="data:image/jpeg;base64,%s" width=25 hights=25>' % data_error

		data_warning = base64.b64encode(open('cgi-bin/warning.jpeg', 'rb').read()).decode('utf-8').replace('\n', '')
		warning = '<img src="data:image/jpeg;base64,%s" width=30 hights=30>' % data_warning
		
		# we create a counter and lists for each test, so we can append the specific error messages in one list
		counter = 0
		RedundancyTest = []
		CompareI7_IndexTest = []
		CompareindexTest = []
		CompareI5_IndexTest = []
		Compareindex2Test = []
		HammingDistanceForindexTest = []
		# two for-loops with i as first line number and j as second line number to compare each line one by one with another
		# line. It will print a warning or error, if the query will get a false from the function defined in the SampleSheet
		# class
		for i in range(length):
			for j in range(i + 1, length):
				if not (sampleSheet[i].SearchForRedundancy(sampleSheet[j])):
					RedundancyMessage = "<p> Redundancy in line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter += 1
					RedundancyTest.append(RedundancyMessage)
				if not (sampleSheet[i].CompareI7_Index(sampleSheet[j])):
					CompareI7_IndexMessage = "<p> Same I7_ID but different Indices in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter +=1
					CompareI7_IndexTest.append(CompareI7_IndexMessage)
				if not (sampleSheet[i].Compareindex(sampleSheet[j])):
					CompareindexMessage = "<p> Same Index but different I7_IDs in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter += 1
					CompareindexTest.append(CompareindexMessage)
				if not (sampleSheet[i].CompareI5_Index(sampleSheet[j])):
					CompareI5_IndexMessage = "<p> Same I5_ID but different Indices in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter += 1
					CompareI5_IndexTest.append(CompareI5_IndexMessage)
				if not (sampleSheet[i].Compareindex2(sampleSheet[j])):
					Compareindex2Message = "<p> Same Index but different I5_IDs in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter += 1
					Compareindex2Test.append(Compareindex2Message)
				if not (sampleSheet[i].HammingDistanceForindex(sampleSheet[j])):
					HammingDistanceindexMessage = "<p> Distance too small in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter += 1
					HammingDistanceForindexTest.append(HammingDistanceindexMessage)
					
		if counter == 0: # if the counter is 0, everything is ok and the Successful Testing Messages will be shown
			print("<head><h3><br>SampleSheetTest Result:</h3></head>")
			print("<head><h4>%s Redundancy Test </h4></head>" % (check))
			print("<head><h4>%s Matching Test for I7_ID </h4></head>" % (check))
			print("<head><h4>%s Matching Test for first Index </h4></head>" % (check))
			print("<head><h4>%s Matching Test for I5_ID </h4></head>" % (check))
			print("<head><h4>%s Matching Test for second Index </h4></head>" % (check))
			print("<head><h4>%s Hamming Distance Test for Indices </h4></head>" % (check))
		else: # if we had errors or warnings, a specific message will be shown to find the lane and entry with an error/warning
			print("<head><h3><br>SampleSheetTest Result:</h3></head>")
			if RedundancyTest != []:
				print("<head><h4>%s Redundancy Test: </h4></head> %s" % (warning, "".join(RedundancyTest)))
			else:
				print("<head><h4>%s Redundancy Test </h4></head>" % (check))
			if CompareI7_IndexTest != []:
				print ("<head><h4>%s Matching Test for I7_ID: </h4></head> %s" %  \
				(error, "".join(CompareI7_IndexTest)))
			else:
				print("<head><h4>%s Matching Test for I7_ID </h4></head>" % (check))
			if CompareindexTest != []:
				print ("<head><h4>%s Matching Test for first Index: </h4></head> %s" % \
				(error, "".join(CompareindexTest)))
			else:
				print("<head><h4>%s Matching Test for first Index </h4></head>" % (check))
			if CompareI5_IndexTest != []:
				print ("<head><h4>%s Matching Test for I5_ID: </h4></head> %s" %  \
				(error, "".join(CompareI5_IndexTest)))
			else:
				print("<head><h4>%s Matching Test for I5_ID </h4></head>" % (check))
			if Compareindex2Test != []:
				print ("<head><h4>%s Matching Test for second Index: </h4></head> %s" % \
				(error, "".join(Compareindex2Test)))
			else:
				print("<head><h4>%s Matching Test for second Index </h4></head>" % (check))
			if HammingDistanceForindexTest != []:
				print ("<head><h4>%s Hamming Distance Test for Indices:</h4></head> %s" % (warning, \
				"".join(HammingDistanceForindexTest))) 
			else:
				print("<head><h4>%s Hamming Distance Test for Indices </h4></head>" % (check))


