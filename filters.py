import helpers
import view

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
occupationInj = lambda ad, value: ad['occupation_group']['concept_id'] == value
municipalInj = lambda ad, value: ad['workplace_address']['municipality_concept_id'] == value
keywordInj = lambda ad, value: value in ad['description']['text']
datecheckInj = lambda ad, value: ad['publication_date'][:10] == value

#
# filter municipality
#
def filtermunicipality(municipalities, ads):
    curatedList = []

    if len(municipalities) == 0:
        return ads

    for m in municipalities:
        curatedList.extend(filt(ads, municipalInj, m))

    return curatedList

#
# filter occupation
#
def filteroccupation(occupations, ads):
    curatedList = []

    if len(occupations) == 0:
        return ads

    for o in occupations:
        curatedList.extend(filt(ads, occupationInj, o))

    return curatedList

#
# filter keywords
#
def filterkeywords(keywords, isPromiscous, ads):
    if len(keywords) == 0:
        return ads

    curatedList = []
    if isinstance(keywords, str):
        keywords = keywords.split()

    if(isPromiscous):
        for word in keywords:
            curatedList.extend(filt(ads, keywordInj, word))
    else:
        curatedList = ads
        for word in keywords:
            curatedList = filt(curatedList, keywordInj, word)

    return curatedList

#
# Get filter by name
#
def getFilterByName(name):
    filters = helpers.getFilterFile()

    for f in filters:
        if f['name'] == name:
            return f
    return None

#
# Crunch one filter
#
def crunchFilter(args):
    f = ""
    if type(args) == str:
        f = getFilterByName(args)
    else:
        f = getFilterByName(args.filter)

    raw = helpers.getAdFile()
    curatedList = []

    curatedList = filtermunicipality(f['concept_ids']['workplace_address__municipality'], raw)
    curatedList = filteroccupation(f['concept_ids']['occupation_group'], curatedList)
    curatedList = filterkeywords(
            f['keywords']['list'],
            f['keywords']['promiscous'],
            curatedList)

    if len(curatedList) == 0:
        view.noads()
        return

    if type(args) != str and args.recent == True:
        yesterday = helpers.getYesterdayAsString('%Y-%m-%d')
        today = helpers.getTodayAsString('%Y-%m-%d')
        yesterdayAds = filt(curatedList, datecheckInj, yesterday)
        todayAds = filt(curatedList, datecheckInj, today)
        curatedList = yesterdayAds + todayAds

    if type(args) != str and args.today == True:
        today = helpers.getTodayAsString('%Y-%m-%d')
        todayAds = filt(curatedList, datecheckInj, today)
        curatedList = todayAds

    helpers.sortAdsByDate(curatedList)

    if type(args) == str:
        return curatedList
    else:
        view.manyads(curatedList)

