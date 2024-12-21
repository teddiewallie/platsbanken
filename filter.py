#
# Get filter by name
#
def getFilterByName(name):
    filters = openJson(filterfile)

    for f in filters:
        if f['name'] == name:
            return f
    return None

#
# Modular filter function
#
def filt(data, lamb, value):
    curatedList = []
    for idx, ad in enumerate(data):
        try:
            if lamb(ad, value) == True:
                curatedList.append(data[idx])
        except:
            continue
    return curatedList

#
# Lambdas to inject into the filter function
#
occupation = lambda ad, value: ad['occupation_group']['concept_id'] == value
municipal = lambda ad, value: ad['workplace_address']['municipality_concept_id'] == value
keyword = lambda ad, value: value in ad['description']['text']
datecheck = lambda ad, value: ad['publication_date'][:10] == value

#
# Crunch one filter
#
def crunchFilter(f):
    raw = openJson(adfile)
    curatedList = None

    if len(f['concept_ids']['workplace_address__municipality']) > 0:
        for m in f['concept_ids']['workplace_address__municipality']:
            curatedList = filt(raw, municipal, m)

        if len(curatedList) == 0:
            print('No ads to show.')
            return

    if len(f['concept_ids']['occupation_group']) > 0:
        for m in f['concept_ids']['occupation_group']:
            if curatedList == None:
                curatedList = filt(raw, occupation, m)
            else:
                curatedList = filt(curatedList, occupation, m)

    curatedWithKeywords = []

    if len(f['keywords']['list']) > 0:
        if curatedList == None:
            curatedList = []

        for idx, m in enumerate(f['keywords']['list']):
            if(f['keywords']['promiscous']):
                curatedWithKeywords = curatedWithKeywords + filt(curatedList, keyword, m)
            else:
                if idx == 0:
                    curatedWithKeywords = curatedList
                curatedWithKeywords = filt(curatedWithKeywords, keyword, m)
            if idx == len(f['keywords']['list']) - 1:
                curatedList = curatedWithKeywords

    if args.recent == True:
        yesterdayAds = filt(curatedList, datecheck, yesterday)
        todayAds = filt(curatedList, datecheck, today)
        curatedList = yesterdayAds + todayAds

    if args.today == True:
        todayAds = filt(curatedList, datecheck, today)
        curatedList = todayAds

    sortListByDate(curatedList)

    if args.count != None:
        counter = 0;
        reverse = list(reversed(curatedList))

        while counter < int(args.count) + 1:
            print(listRow(reverse[int(args.count) - counter]))
            counter = counter + 1
        
    else:
        if len(curatedList) == 0:
            print('No ads to show.')
            return
        for ad in curatedList:
            print(listRow(ad))


