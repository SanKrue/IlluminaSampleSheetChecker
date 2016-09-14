import operator
import base64

class MiSeqSampleSheetLine:
	# the objects in class MiSeqSampleSheetLine have to have 10 parameters, which were store in SampleSheet files
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
			   str(self.I5_index_ID) + ", " + str(self.index2)+ ", " + str(self.Sample_Project) + ", " + \
			   str(self.Description) + ")"
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

	# function that search for redundancy in a SampleSheet with index2, which means Sample_ID, I7_index_ID, index, I5_index_ID,
	# index2 are the same in two different lines of the file
	def SearchForRedundancy(self, otherSampleSheetLine):
	   if (self.Sample_ID, self.I7_index_ID, self.index, self.I5_index_ID, self.index2) == \
		   (otherSampleSheetLine.Sample_ID, otherSampleSheetLine.I7_index_ID, otherSampleSheetLine.index, \
			otherSampleSheetLine.I5_index_ID, otherSampleSheetLine.index2):
		   return False
	   else:
		   return True
		   
	# function that search for redundancy in a SampleSheet without index2, which means Sample_ID, I7_index_ID and index are 
	# the same in two different lines of the file
	def SearchForRedundancy2(self, otherSampleSheetLine):
	   if (self.Sample_ID, self.I7_index_ID, self.index) == \
		   (otherSampleSheetLine.Sample_ID, self.I7_index_ID, otherSampleSheetLine.index):
		   return False
	   else:
		   return True
		   
	# functions which compare the different Indices (index and index2) respectively Sample_IDs in the in different
	# lines of the file; e.g. same index but different Sample_ID will give a False
	def CompareSampleIDandIndex(self, otherSampleSheetLine): # for index
		if ((self.Sample_ID != otherSampleSheetLine.Sample_ID) and(self.index == otherSampleSheetLine.index)):
			return False
		elif ((self.Sample_ID == otherSampleSheetLine.Sample_ID) and (self.index != otherSampleSheetLine.index)):
			return False
		else:
			return True
	
	def CompareSampleIDandIndex2(self, otherSampleSheetLine): # for index2 if necessary
		if ((self.Sample_ID != otherSampleSheetLine.Sample_ID) and (self.index2 == otherSampleSheetLine.index2)): 
			return False
		elif ((self.Sample_ID == otherSampleSheetLine.Sample_ID) and (self.index2 != otherSampleSheetLine.index2)):
			return False
		else:
			return True

	# functions which compare the different Indices (index and index2) respectively Index_IDs in the in different
	# lines of the file; e.g. same index but different I7_index_ID will give a False
	def CompareIndex(self, otherSampleSheetLine): # for index
		if ((self.I7_index_ID != otherSampleSheetLine.I7_index_ID) and \
			(self.index == otherSampleSheetLine.index)):
			return False
		elif ((self.I7_index_ID == otherSampleSheetLine.I7_index_ID) and \
			(self.index != otherSampleSheetLine.index)):
			return False
		else:
			return True

	def CompareIndex2(self, otherSampleSheetLine): # for index2 if necessary
		if ((self.I5_index_ID != otherSampleSheetLine.I5_index_ID) and \
			(self.index2 == otherSampleSheetLine.index2)):
			return False
		elif ((self.I5_index_ID == otherSampleSheetLine.I5_index_ID) and \
			(self.index2 != otherSampleSheetLine.index2)):
			return False
		else:
			return True

	# function which calculate the Hamming Distance between two Indices with the same Sample_ID and gives a warning,
	# if it is smaller than 2, e.g. TGAACCTT and TGAACCTG
	def HammingDistanceForindex(self, otherSampleSheetLine): # for index
		if (self.Sample_ID == otherSampleSheetLine.Sample_ID):
			index1 = self.index 
			index2 = otherSampleSheetLine.index
			ne = operator.ne
			diffs = sum(list(map(ne, index1, index2)))
			if diffs < 2:
				return False
			else:
				return True
		return True
	
	def HammingDistanceForindex2(self, otherSampleSheetLine): # for index2 if necessary
		if (self.Sample_ID == otherSampleSheetLine.Sample_ID):
			index1 = self.index2
			index2 = otherSampleSheetLine.index2
			ne = operator.ne
			diffs = sum(list(map(ne, index1, index2)))
			if diffs < 2:
				return False
			else:
				return True
		return True
	
	# main function, read and process a MISeq SampleSheet	
	def ReadandProcessMiSeq(self): # parameter is only the file (here represented as "self")
		sampleSheet = []
		for item in (self):
			if "[Data]" in item: # ignore everything above "[Data]"
				break
		for item in (self): # process everything after "[Data]"
			line = item.strip()  # remove whitespace from beginning or end of the line
			if(len(line) > 0):  # length of the line should be >0
				splitLine = line.split(",")  # the items will split with the ',' as separator, because we have a .csv file
				if (len(splitLine) > 8): # if the file contains index and index2
					sampleSheetLineElement = MiSeqSampleSheetLine(splitLine[0], splitLine[1], splitLine[2], splitLine[3], \
														 splitLine[4], splitLine[5], splitLine[6], splitLine[7], \
														 splitLine[8], splitLine[9])  # getting all items as MiSeqSampleSheetLine
																					  # objects by calling them with their column 																						  # number starting with 0
					sampleSheet.append(sampleSheetLineElement) # putting all objects in the created list "Sample Sheet"
				else: # if the file contains only the first index, I5_index_ID and index2 are initialized as "None"
					sampleSheetLineElement2 = MiSeqSampleSheetLine(splitLine[0], splitLine[1], splitLine[2], splitLine[3], \
														 splitLine[4], splitLine[5], None, None, \
														 splitLine[6], splitLine[7])  # getting all items as MiSeqSampleSheetLine
																					  # objects by calling them with their column 																						  # number starting with 0
					sampleSheet.append(sampleSheetLineElement2) # putting all objects in the created list "Sample Sheet"
				
		length = len(sampleSheet)
		
		# count samples in the sample sheet 
		samples = 0
		for i in range(length-1): # length-1, because in length is the header included
			samples +=1
		# bootstrap css style for the entire output
		print("<link rel=stylesheet href=https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css>")
		print("<div class=container>")
		print("<p><h4>Number of samples in file: <strong>%i</strong> </h4></p>" % (samples))
		print("</div>")
		
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
		Redundancy2Test = []
		CompareSampleIDandIndexTest = []
		CompareSampleIDandIndex2Test = []
		CompareI7_IndexTest = []
		CompareIndexTest = []
		CompareI5_IndexTest = []
		CompareIndex2Test = []
		HammingDistanceForindexTest = []
		HammingDistanceForindex2Test = []
		
		# two for-loops with i as first line number and j as second line number to compare each line one by one with another
		# line. It will increment the counter and append our defined warning or error message to the specific list, if the query 		    # will get a False from the function defined in the MiSeqSampleSheetLine class
		for i in range(length):
			for j in range(i + 1, length):
				if not sampleSheet[i].index2 == None: # in case the MiSeq SampleSheet contains a second index
					if not (sampleSheet[i].SearchForRedundancy(sampleSheet[j])):
						RedundancyMessage = "<p> Redundancy in line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
						counter += 1
						RedundancyTest.append(RedundancyMessage)
					if not sampleSheet[1].I5_index_ID == "": # if the column I5_index_ID has an entry, we can compare IDs
						if not (sampleSheet[i].CompareIndex2(sampleSheet[j])):
							CompareIndex2Message = "<p> ID or Index2 duplicate, difference in the other parameter in \
													line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 				str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
							counter += 1
							CompareIndex2Test.append(CompareIndex2Message)
					else: # if the column I5_index_ID has no entry, we compare Sample_IDS
						if not (sampleSheet[i].CompareSampleIDandIndex2(sampleSheet[j])):
							CompareSampleIDandIndex2Message = "<p> SampleID or Index2 duplicate, difference in the other \
														  parameter in line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 				      str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
							counter += 1
							CompareSampleIDandIndex2Test.append(CompareSampleIDandIndex2Message)
					if not (sampleSheet[i].HammingDistanceForindex2(sampleSheet[j])):
						HammingDistanceindex2Message = "<p> Distance too small in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
						counter += 1
						HammingDistanceForindex2Test.append(HammingDistanceindex2Message)
				else: # if the file contains only the first index, I5_index_ID and index2 are initialized as "None"
					if not (sampleSheet[i].SearchForRedundancy2(sampleSheet[j])): # we use the second Redundany function
						Redundancy2Message = "<p> Redundancy in line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
						counter += 1
						Redundancy2Test.append(Redundancy2Message)
	
				if not (sampleSheet[i].HammingDistanceForindex(sampleSheet[j])): # we always want to calculate Hamming Dinstance
																				 # for the first index
					HammingDistanceindexMessage = "<p> Distance too small in line %s and %s:<br>%s<br>%s</p>" \
										  % (str(i + 20), str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
					counter += 1
					HammingDistanceForindexTest.append(HammingDistanceindexMessage)
				if not sampleSheet[1].I7_index_ID == "": # if the column I7_index_ID has an entry, we can compare IDs
					if not (sampleSheet[i].CompareIndex(sampleSheet[j])):
							CompareIndexMessage = "<p> ID or Index duplicate, difference in the other parameter in \
											line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 		str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
							counter += 1
							CompareIndexTest.append(CompareIndexMessage)
				else: # if the column I7_index_ID has no entry, we compare Sample_IDS
					if not (sampleSheet[i].CompareSampleIDandIndex(sampleSheet[j])):
						CompareSampleIDandIndexMessage = "<p> SampleID or Index duplicate, difference in the other parameter in \
													line %s and %s:<br>%s<br>%s</p>" % (str(i + 20), \
									 				str(j + 20), str(sampleSheet[i]), str(sampleSheet[j]))
						counter += 1
						CompareSampleIDandIndexTest.append(CompareSampleIDandIndexMessage)
						
		if counter == 0: # if the counter is 0, everything is ok and the Successful Testing Messages will be shown
			print("<div class=container>")
			print("<br><head><h3><strong>SampleSheet Checker Result:</strong></h3></head>")	
			print("<br><head><h4>%s Hamming Distance Test for Index </h4></head>" % (check)) # HammingDistance Test for index
			print("<br><head><h4>%s Redundancy Test </h4></head>" % (check)) # Redundancy/Redundancy2 Test
			if not sampleSheet[1].I7_index_ID == "":	
				print("<br><head><h4>%s Matching Test for Index </h4></head>" % (check)) # CompareIndex Test
			else:
				print("<br><head><h4>%s SampleID/Index Matching Test </h4></head>" % (check)) # CompareSampleIDandIndex Test
			if not sampleSheet[i].index2 == None:
				print("<br><head><h4>%s Hamming Distance Test for Index2 </h4></head>" % (check)) # HammingDistance Test for 																									  # index2
				if not sampleSheet[1].I5_index_ID == "":
					print("<br><head><h4>%s Matching Test for Index2 </h4></head>" % (check)) # CompareIndex2 Test
				else:
					print("<br><head><h4>%s SampleID/Index2 Matching Test </h4></head>" % (check)) # CompareSampleIDandIndex2 																									   # Test 
			print("</div>")
				
				
			
		else: # if we had errors or warnings, a specific message will be shown to find the lane and entry with an error/warning
			print("<div class=container>")
			print("<br><head><h3><strong>SampleSheet Checker Result:</strong></h3></head>")
			if HammingDistanceForindexTest != []:
				print ("<br><head><h4>%s Hamming Distance Test for Index:</h4></head> %s" % (warning, \
						"".join(HammingDistanceForindexTest))) 
			else:
					print("<br><head><h4>%s Hamming Distance Test for Index </h4></head>" % (check))
			if not sampleSheet[1].I7_index_ID == "": # compare I7_index_IDs
				if CompareIndexTest != []:
					print ("<br><head><h4>%s Matching Test for Index: </h4></head> %s" % (error, "".join(CompareIndexTest)))
				else:
					print("<br><head><h4>%s Matching Test for Index </h4></head>" % (check))
			else:
				if CompareSampleIDandIndexTest != []: # compare Sample_IDs
					print("<br><head><h4>%s SampleID/Index Matching Test: </h4></head> %s" % (error, \
							  "".join(CompareSampleIDandIndexTest)))
				else:
					print("<br><head><h4>%s SampleID/Index Matching Test </h4></head>" % (check))
			if not sampleSheet[i].index2 == None: # in case the MiSeq SampleSheet contains a second index
				if RedundancyTest != []:
					print("<br><head><h4>%s Redundancy Test: </h4></head> %s" % (warning, "".join(RedundancyTest)))
				else:
					print("<br><head><h4>%s Redundancy Test </h4></head>" % (check))
				if HammingDistanceForindex2Test != []:
					print ("<br><head><h4>%s Hamming Distance Test for Index2:</h4></head> %s" % (warning, \
							"".join(HammingDistanceForindex2Test))) 
				else:
					print("<br><head><h4>%s Hamming Distance Test for Index2 </h4></head>" % (check))
				if not sampleSheet[1].I5_index_ID == "": # compare I5_index_IDs
					if CompareIndex2Test != []:
						print ("<br><head><h4>%s Matching Test for Index2: </h4></head> %s" % \
							(error, "".join(CompareIndex2Test)))
					else:
						print("<br><head><h4>%s Matching Test for Index2 </h4></head>" % (check))
				else: # compare Sample_IDs
					if CompareSampleIDandIndex2Test != []:
						print("<br><head><h4>%s SampleID/Index2 Matching Test: </h4></head> %s" % (error, \
							  "".join(CompareSampleIDandIndex2Test)))
					else:
						print("<br><head><h4>%s SampleID/Index2 Matching Test </h4></head>" % (check))
			else: # if the file contains only the first index, we use the Redundancy2 Test
				if Redundancy2Test != []:
					print("<br><head><h4>%s Redundancy Test: </h4></head> %s" % (warning, "".join(Redundancy2Test)))
				else:
					print("<br><head><h4>%s Redundancy Test </h4></head>" % (check))
			print("</div>")
			
				


