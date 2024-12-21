import json
import os
import datetime

adfile = 'platsbanken.json'
filterfile = 'filters.json'

#
# Get today as datetime
#
def getToday():
    return datetime.date.today()

#
# Get yesterday as datetime
#
def getYesterday():
    return today - datetime.timedelta(days=1)

#
# Get raw data from json file
#
def openJson(name):
    f = open(name, 'r')
    data = json.load(f)
    f.close()
    return data

#
# Write raw data to json file
#
def dumpJson(name, dump):
    f = open(name, 'w')
    json.dump(dump, f)
    f.close()

#
# Get the adfile
#
def getAdFile():
    return openJson(adfile)

#
# Write to the adfile
#
def writeToAdFile(ads):
    dumpJson(adfile, ads)

#
# Get the filter file
#
def getFilterFile():
    return openJson(filterfile)

#
# Check if ad is removed
#
def isRemoved(ad):
    return 'removed' in ad and ad['removed'] == True

#
# json load, just so we don't have to import json anywhere else
#
def jsonLoad(stream):
    return json.load(stream)

#
# Get modified
#
def getAdFileMetaModified(forToday):
    if forToday:
        return datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S')

    modified = datetime.datetime.fromtimestamp(os.path.getmtime(adfile))
    return modified.strftime('%Y-%m-%dT%H:%M:%S')

#
# Sort ads by date
#
def sortAdsByDate(ads):
    return ads.sort(key=lambda ad: ad['publication_date'])


