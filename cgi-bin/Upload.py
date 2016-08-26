#!/usr/bin/env python3

print ("""
<html>
<head>
<title>SampleSheet Test</title>
</head>
<body>
<H1>SampleSheet Test</H1>
<body>
<form enctype="multipart/form-data" 
                     action="SampleSheetUpload.py" method="post">
<p>File: <input type="file" name="filename" accept=".csv"/></p>
<p><input type="submit" value="Upload" /></p>
</form>
</body>
</html>""")
