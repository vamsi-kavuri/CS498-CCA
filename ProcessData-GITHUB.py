#!/usr/bin/python

import sys
import string
import re
import subprocess
import os
from decimal import Decimal

FilePath = sys.argv[1]
FileName = sys.argv[2]
InputFile = sys.argv[1] + sys.argv[2]
#FinalOutputFile = sys.argv[3]
LocationtoHDFUtils = "<LOCATION TO HDF EXECUTABLES>/HDF4/hdf4/bin/"
LongTempFile = "<LOCATION OF TEMPORARY FILE>/LongTemp"
LatTempFile = "/<LOCATION OF TEMPORARY FILE>/LatTemp"
MoleTempFile = "/<LOCATION OF TEMPORARY FILE>/MoleTemp"

#split the file name so that you can get the date and set a date for ACSCI standard date form
year = FileName.split(".")[1]
month = FileName.split(".")[2]
day = FileName.split(".")[3]

#temp = (FileName.split(".")[1],FileName.split(".")[2],FileName.split(".")[3])
s = ""
myDate = "%s-%s-%s" % (year,month,day) 

#The following is used primary to create a list of OS level commands
#Run the following commands against the file and produce a file
#/hdp dumpsds -s -d -n "mole_fraction_of_carbon_dioxide_in_free_troposphere" ../NEWDATA.hdf
# Location of the Utiliy
#Location of the Airs Data
#Sample File name we are going to use
#AIRS.2011.06.06.L3.CO2Std_IR008.v5.9.14.0.X13086110809.hdf
commandStringMole = LocationtoHDFUtils + "hdp dumpsds -s -d -n \"mole_fraction_of_carbon_dioxide_in_free_troposphere\""
commandStringLong = LocationtoHDFUtils + "hdp dumpsds -s -d -n \"Longitude\""
commandStringLat = LocationtoHDFUtils + "hdp dumpsds -s -d -n \"Latitude\""
FinalMoleCommand = "%s %s > %s" % (commandStringMole,InputFile,MoleTempFile)
FinalLongCommand = "%s %s > %s" % (commandStringLong,InputFile,LongTempFile)
FinalLatCommand = "%s %s > %s" % (commandStringLat,InputFile,LatTempFile)
os.system(FinalMoleCommand)
os.system(FinalLongCommand)
os.system(FinalLatCommand)

#OPen each one of the files and read into the list
#Latittude
LongData = list()
with open (LongTempFile) as LongF:
   LongData = LongF.read().splitlines()
with open (MoleTempFile) as MoleF:
   MoleData = MoleF.read().splitlines()
with open (LatTempFile) as LatF:
   LatData = LatF.read().splitlines()

#First check the length of the lists...they should be the same
# IF not the same ERROR out with file name. 
# This is important becuase if these numbers do not match the the matrix from the HDF file has been interpretted
# incorrectly.  
if len(LongData) == len(MoleData) and len(MoleData) == len(LatData):
    myError = 0#Do nothing
else:
    print "There was an error in the lengths of the data"
    exit()

#Iterate therough the data now and then print out the final listing of data

myIterrator = 0
logvalues = list()
while myIterrator < len(LongData):
   LogValues = LongData[myIterrator].split()
   MoleValues = MoleData[myIterrator].split()
   LatValues = LatData[myIterrator].split()
   myIterrator2 = 0
   while myIterrator2 < len(LogValues):
      # This will convert the mole fraction to a Parts Per Million
      molFrac = Decimal(MoleValues[myIterrator2]) * 1000000
      print "%s,%s,%s,%s,%s" % (myDate,LogValues[myIterrator2],LatValues[myIterrator2],MoleValues[myIterrator2],molFrac)
      myIterrator2 += 1
   myIterrator +=1

#Temporary Data Clean up. 
MoleRMCommand = "rm %s" % (MoleTempFile)
LongRMCommand = "rm %s" % (LongTempFile)
LatRMCommand = "rm %s" % (LatTempFile)
os.system(MoleRMCommand)
os.system(LongRMCommand)
os.system(LatRMCommand)
