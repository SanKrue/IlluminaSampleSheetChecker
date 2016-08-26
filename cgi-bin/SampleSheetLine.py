import operator

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

    # function that search for redundancy in the SampleSheet, which means lane,  SampleID and Index are the
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

           

