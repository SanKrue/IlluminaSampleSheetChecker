# IlluminaSampleSheetChecker
Checks HiSeq or MiSeq SampleSheets for errors (e.g. redundancy, duplications in indices or SampleIDs)

### Requirements
Installation of a version of Python 3.X

### Installation instructions
1. Download the cgi-bin folder and store it in your favorite directory
2. Open a terminal window and switch to the directory where the cgi-bin folder is stored
3. Now you have to make the files executable, therefor type: `chmod +x cgi-bin/*.py`
4. Start a Python3 HTTP server with cgi tag in the directory, therefor type: `python3 -m http.server --cgi`
Note: the terminal window is now running the server and is not available for further interactions
5. Now you can open your favorite web browser an go to `http://localhost:8000/cgi-bin/Upload.py`
If you can't open the page, please check the port number in the terminal window (sometimes it is 8080) and your browser

##### To disconnect from server:
Type `Ctrl+C` in the terminal window after you have done your work with the IlluminaSampleSheetChecker

### Tests included

#### For HiSeq SampleSheets:
| Test Name | Check |
|-----------|-------|
| FCID Name Test | FCID in the filename and in the file are the same |
| Redundancy Test | duplicate rows |
| Matching Test for Index in same lane | duplicate indices in the same lane |
| Matching Test for SampleIDs in same lane | duplicate SampleIDs in the same lane |
| Matching Test for diffenret lanes | same SampleID but a diffenrece in another parameter (e.g. Index) in different lanes |
| Hamming Distance Test for Indices | Hamming Distance between two indices greater than one |

#### For MiSeq SampleSheets:
| Test Name | Check | Two versions (for SampleSheets with one or two indices) |
|-----------|-------| ------------------------------------------ |
| Hamming Distance Test for Index/Index2 | Hamming Distance between two indices greater than one | :heavy_check_mark: |
| Redundancy Test | duplicate rows | :heavy_check_mark: |
| Matching Test for Index | duplicate index with different I7IndexIDs | |
| Matching Test for Index2 | duplicate index2 with different I5IndexIDs | |
| SampleID/Index Matching Test | Same SampleID and different indices or vice versa | :heavy_check_mark: |
