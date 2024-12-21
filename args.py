import argparse
import filter.py as filters
import helpers.py as helpers

parser = argparse.ArgumentParser(
        prog='Platsbanken',
        description='Curate for me')

parser.add_argument('-f', '--filter')
parser.add_argument('-t', '--today', action='store_true')
parser.add_argument('-u', '--update', action='store_true')
parser.add_argument('-x', '--update_today', action='store_true')
parser.add_argument('-i', '--id')
parser.add_argument('-q', '--query')
parser.add_argument('-n', '--filternames', action='store_true')
parser.add_argument('-a', '--all', action='store_true')
parser.add_argument('-c', '--count')
parser.add_argument('-r', '--recent', action='store_true')
parser.add_argument('--init')

args = parser.parse_args()

if args.update == True:
    helpers.fetch()

if args.filter != None:
    filters.crunchFilter(getFilterByName(args.filter))

if args.query != None:
    keywords = args.query.split()
    raw = helpers.openJson(adfile)
    curatedList = raw
    for k in keywords:
        curatedList = filt(curatedList, keyword, k)
    helpers.sortListByDate(curatedList)
    for ad in curatedList:
        print(listRow(ad))

if args.all:
    raw = helpers.openJson(adfile)
    sortListByDate(raw)
    for ad in raw:
        print(listRow(ad))

if args.id != None:
    raw = helpers.openJson(adfile)
    thisAd = None
    for ad in raw:
        if ad['id'] == args.id:
           thisAd = ad 
    print(thisAd['headline'])
    print(thisAd['description']['text'])

if args.filternames == True:
    filt = openJson(filterfile)
    names = ""
    for f in filt:
        names = names + f['name'] + " "
    print(names)

