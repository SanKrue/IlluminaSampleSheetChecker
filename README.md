# SampleSheet Checker
Checks HiSeq or MiSeq SampleSheets for errors (e.g. redundancy, duplications in indices or SampleIDs)

### Requirements
Installation of a version of Python 3

### Installation instructions
1. Download the cgi-bin folder and store it in your favorite directory
2. Open a terminal window and switch to the directory where the cgi-bin folder is stored
3. Now you have to make the files executable, therefor type: `chmod +x cgi-bin/*.py`
4. Start a Python 3 HTTP server with cgi tag in the directory, therefor type: `python3 -m http.server --cgi`  
   Note: the terminal window is now running the server and is not available for further interactions
5. Now you can open your favorite web browser an go to `http://localhost:8000/cgi-bin/Upload.py`  
   If you can't open the page, please check the port number in the terminal window (sometimes it is 8080) and change the number
   in your browser
   
##### To disconnect from server:
Type `Ctrl+C` in the terminal window after you have done your work with the SampleSheet Checker

### SampleSheet Checker Tests

#### For HiSeq SampleSheets:
| Test Name | Check |
| --------- | ----- |
| FCID Name Test | FCID in the filename and in the file are the same |
| Redundancy Test | duplicate rows |
| Matching Test for Index in same lane | duplicate indices in the same lane |
| Matching Test for SampleIDs in same lane | duplicate SampleIDs in the same lane |
| Matching Test for different lanes | same SampleID but a difference in another parameter (e.g. Index) in different lanes |
| Hamming Distance Test for Indices | Hamming Distance between two indices greater than one |

#### For MiSeq SampleSheets:
| Test Name | Check | Two versions (for SampleSheets with one or two indices) |
| --------- | ----- | :------------------------------------------: |
| Hamming Distance Test for Index/Index2 | Hamming Distance between two indices greater than one | :heavy_check_mark: |
| Redundancy Test | duplicate rows | :heavy_check_mark: |
| Matching Test for Index | duplicate Index with different I7IndexIDs | |
| Matching Test for Index2 | duplicate Index2 with different I5IndexIDs | |
| SampleID/Index Matching Test | Same SampleID and different indices or vice versa | :heavy_check_mark: |

### Additional informations
- the SampleSheet Checker works with *.csv files with ten columns in HiSeq files and ten or eight columns in MiSeq files
  Note: In files with eigth columns, the columns "I5IndexID" and "Index2" are initialized with "None", because here it is
  considered that the files have only one Index (but in the MiSeq class it is defined, that a MiSeq object gets ten parameters)
- for a correct result the columns should be in the same order as in the examples in the Testfiles folder
- the cgi-bin folder contains four *.py files  
  1. Upload.py for the CG Interface in the browser
  2. SampleSheetUpload.py for uploading the file and store it in a temporary folder; this file contains also the function which  	  checks the kind of SampleSheet and call the relevant function for a HiSeq or MiSeq file
  3. HiSeqSampleSheetLine.py for HiSeq SampleSheets, with the class definition and all other functions for a HiSeq SampleSheet
  4. MiSeqSampleSheetLine.py for MiSeq SampleSheets, with the class definition and all other functions for a MiSeq SampleSheet  
- it is defined that a HiSeq SampleSheet has "FCID" and a MiSeq SampleSheet "\[Header]" as the first word in the first line;
  if your SampleSheets have different first words, you have to change this in SampleSheetUpload.py, because on the basis of this
  words it will be decided which kind of file was uploaded
- in SampleSheetUpload.py it is also defined, that the relevant data of a MiSeq file begin after the word "\[Data]" (see the MiSeq
  example in the Testfiles folder); if this is different in your MiSeq files, you have to change this also in the script

