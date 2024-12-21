import json
import datetime
import urllib.request
import os

today = datetime.date.today()
yesterday = today - datetime.timedelta(days=1)

today = today.strftime('%Y-%m-%d')
yesterday = yesterday.strftime('%Y-%m-%d')

adfile = 'platsbanken.json'
filterfile = 'filters.json'


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

def isRemoved(ad):
    return 'removed' in ad and ad['removed'] == True

def fetch():
    modified = datetime.date.today().strftime('%Y-%m-%dT%H:%M:%S')
    
    if args.update_today == False:
        modified = datetime.datetime.fromtimestamp(os.path.getmtime(adfile))
        modified = modified.strftime('%Y-%m-%dT%H:%M:%S')

    url = 'https://jobstream.api.jobtechdev.se/stream?date=' + modified
    with urllib.request.urlopen(url) as stream:
        newdata = json.load(stream)
        if len(newdata) == 0:
            print('No new ads')
            return

        olddata = openJson(adfile)

        dictionary = {}

        for o in olddata:
            dictionary[o['id']] = o

        total = len(newdata)
        counter = 0

        while len(newdata) > 0:
            o = newdata.pop(0)
            counter = counter + 1
            print(f"adding and updating ads: {counter}/{total}", end='\r', flush=True)

            if not isRemoved(o):
                dictionary[o['id']] = o

        dumpJson(adfile, list(dictionary.values()))
        print()

#
# Formatted list row
#
def listRow(ad):
    return ad['publication_date'][:10] + ' ' + ad['id'] + ' ' + ad['headline']

#
# Sort list by date
#
def sortListByDate(unsortedList):
    return unsortedList.sort(key=lambda ad: ad['publication_date'])

