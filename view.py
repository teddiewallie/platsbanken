#
# Formatted list row
#
def listRow(ad):
    print(ad['publication_date'][:10] + ' ' + ad['id'] + ' ' + ad['headline'])

#
# No ads to show.
#
def noads():
    print("No ads to show.")

#
# Show a single ad.
#
def onead(ad):
    print(thisAd['headline'])
    print(thisAd['description']['text'])

#
# Show many ads.
#
def manyads(ads):
    for ad in ads:
        listRow(ad)

#
# Show the ad counter while fetching.
#
def adcounter(counter, total):
    print(f"adding and updating ads: {counter}/{total}", end='\r', flush=True)
    
    if counter == total:
        print()

#
# Show the list of filter names.
#
def names(names):
    print(names)
