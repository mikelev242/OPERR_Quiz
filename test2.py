import urllib2, os, arcpy, xlwt

"""
To be honest, in my experience with python coding, I have no familiarity with retriving data from a REST service
While I tried my best to figure out a solution using various resources available, I could not get the code to run.
It runs into an error at the arcpy.JSONTo_Features_conversion line where I keep getting an error saying
the program is "unable to parse json features". I tried to debug the script, but having no experience reading
services I was unable to come to a solution. I added the last part of the script where I would write the table
produced from reading from the service to an excel file, where the data can then be edited there. I have in
the past shown the ability to learn new concepts, as much of my python experience was learned on my own and on the fly.
I am willing to learn how to read services and perfrom these specific data manipulation techniques if granted the
opportunity as through my performace in my major classes, i have shown the ability to be a good learner.
"""
#url of service
URL = "http://gpd01.cityofboston.gov:6080/arcgis/rest/services/all_injuries_yearly/MapServer/2"
#declare where clause and fields we want
where = "1=1"
outfields = "FID,Shape,Incident,Date,Mode,Count"

#write query
query = "?where={}&outFields={}&returnGeometry=true&f=json".format(where, outfields)

#retrieve your service and your query
service = URL + query
response = urllib2.urlopen(service)

myJSON = response.read()

foo = open("jsonOutput.json", "wb")
foo.write(myJSON)
foo.close()

arcpy.JSONToFeatures_conversion("jsonOutput.json", "test.shp")

#create workbook
excelworkbook = xlwt.Workbook()
sheet = excelworkbook.add_sheet(sheet)

#create colum heads
sheet.write(0,0, "Incident")
sheet.write(0,1, "Date")
sheet.write(0,2, "Mode")
sheet.write(0,3, "Count")

num=1
#parse through file and write excel sheet
for row in arcpy.da.SearchCursor("test.shp", ["Incident", "Date", "Mode", "Count"]):
    sheet.write(num, 0, row[0])
    sheet.write(num, 1, row[1])
    sheet.write(num, 2, row[2])
    sheet.write(num, 3, row[3])
    num = num+1

excelworkbook.save('BostonCrash2016.xls')
