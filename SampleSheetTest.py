from SampleSheet import SampleSheetLine
import argparse

# defining filename as the first argument which will committed in the command line
parser = argparse.ArgumentParser()
parser.add_argument('filename')
args = parser.parse_args()


with open(args.filename, "r") as file:
    next(file)  # ignore the first line
    sampleSheet = []
    fwc = filter(lambda row: row[0] != '#', file)  # fcw=file without comments --> ignore lines which start with '#'
    for item in fwc:  # for each line in file
        line = item.strip()  # remove whitespace from beginning or end of the line
        if(len(line) > 0):  # length of the line should be >0
            splitLine = line.split(",")  # the items will split with the ',' as separator, because we have a .csv file
            sampleSheetLineElement = SampleSheetLine(splitLine[0], splitLine[1], splitLine[2], splitLine[3], \
                                                     splitLine[4], splitLine[5], splitLine[6], splitLine[7], \
                                                     splitLine[8], splitLine[9])  # getting all items as SampleSheetLine
            # objects by calling them with their column number starting with 0
            sampleSheet.append(sampleSheetLineElement)  # putting all objects in the created list "Sample Sheet"
    length = len(sampleSheet)
    # two for-loops with i as first line number and j as second line number to compare each line one by one with another
    # line. It will print a warning or error, if the query will get a false from the function defined in the SampleSheet
    # class
    for i in range(length):
        for j in range(i + 1, length):
            if not(sampleSheet[i].SearchForRedundancy(sampleSheet[j])):
                print("\nWarning: Redundancy in line " + str(i + 2) + " and " + str(j + 2) + ":\n" + \
                               str(sampleSheet[i]) + "\n" + str(sampleSheet[j]))
            if not(sampleSheet[i].CompareIndexInLane(sampleSheet[j])):
                print("\nError: Same Index but different SampleIDs in line " + str(i + 2) + " and " + str(j + 2) \
                      + ":\n" + str(sampleSheet[i]) + "\n" + str(sampleSheet[j]))
            elif not(sampleSheet[i].CompareIndexInLane(sampleSheet[j])):
                print("\nError: Same SampleID but different Indices in line " + str(i + 2) + " and " + str(j + 2) \
                      + ":\n" + str(sampleSheet[i]) + "\n" + str(sampleSheet[j]))
            if not(sampleSheet[i].CompareSampleIDInLanes(sampleSheet[j])):
                print("\nWarning: Same SampleID, but difference in another parameter. Line " + str(i + 2) + " and " \
                      + str(j + 2) + ":\n" + str(sampleSheet[i]) + "\n" + str(sampleSheet[j]))
            if not(sampleSheet[i].HammingDistanceForIndices(sampleSheet[j])):
                print("Distance too small in line " + str(i + 2) + " and " + str(j + 2) + \
                      ":\n" + str(sampleSheet[i]) + "\n" + str(sampleSheet[j]))




