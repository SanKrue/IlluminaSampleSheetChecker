#!/usr/bin/env python3

print ("""
<!DOCTYPE html>
<html>
<head>
<title>SampleSheet Checker</title>
<link rel=stylesheet href=https://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css>
</head>
<body>
<div class="container">
<H2>SampleSheet Checker</H2>
	<p> SampleSheet Checker is a tool for checking a sample sheet, which is used for the assignment of the generated data with an Illumina HiSeq or MiSeq Sequencing System. The application contains several compare functions, which will search for redundancy or e.g. a duplicate Index in different Sample IDs. </p>
	<p> For further information, please read <a href=https://github.com/SanKrue/SampleSheetChecker/blob/master/README.md>SampleSheet Checker - README</a> </p>
</div>
<div class=container>
<div class=panel-body>
	<strong>Upload a prepared sample sheet</strong>
	<form enctype="multipart/form-data" action="SampleSheetUpload.py" method="post">
	<p><input type="file" name="filename" accept=".csv"/></p>
	<strong>Validate the file </strong>
	<p><input type="submit" value="Submit" /></p>
</form>
</div>
</div>
</body>
</html>""")
