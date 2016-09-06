#!/usr/bin/env python3

print ("""
<html>
<head>
<title>SampleSheet Checker</title>
</head>
<body>
<head><H1>SampleSheet Checker</H1></head>
	<p> Checks uploaded HiSeq or MiSeq SampleSheets for errors </p>
<body>
<form enctype="multipart/form-data" action="SampleSheetUpload.py" method="post">
<p>File: <input type="file" name="filename" accept=".csv"/></p>
<p><input type="submit" value="Upload" /></p>
</form>
</body>
</html>""")
