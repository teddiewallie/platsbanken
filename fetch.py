import urllib.request
import helpers
import view

#
# Fetch adfiles from api
#
def fetch(args):
    modified = helpers.getAdFileMetaModified(True) 

    if args.update_today == False:
        modified = helpers.getAdFileMetaModified(False)

    url = 'https://jobstream.api.jobtechdev.se/stream?date=' + modified
    with urllib.request.urlopen(url) as stream:
        newdata = helpers.jsonLoad(stream)
        if len(newdata) == 0:
            view.nofetch()
            return

        olddata = helpers.getAdFile()

        dictionary = {}

        for o in olddata:
            dictionary[o['id']] = o

        total = len(newdata)
        counter = 0

        while len(newdata) > 0:
            o = newdata.pop(0)
            counter = counter + 1
            view.adcounter(counter, total)

            if not helpers.isRemoved(o):
                dictionary[o['id']] = o

        helpers.writeToAdFile(list(dictionary.values()))

