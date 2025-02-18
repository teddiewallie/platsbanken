from fastapi import FastAPI

import argparse
import view
import helpers
import fetch
import filters

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
parser.add_argument('-r', '--recent', action='store_true')
parser.add_argument('--init')

args = parser.parse_args()

if args.update == True:
    fetch.fetch(args)

if args.filter != None:
    filters.crunchFilter(args)

if args.query != None:

    keywords = args.query
    raw = helpers.getAdFile()

    curatedList = filters.filterkeywords(keywords, False, raw)
    helpers.sortAdsByDate(curatedList)

    if len(curatedList) == 0:
        view.noads()
        exit(0)

    view.manyads(curatedList)

if args.all:
    raw = helpers.getAdFile()
    helpers.sortAdsByDate(raw)
    view.manyads(raw)

if args.id != None:
    raw = helpers.getAdFile()
    thisAd = None
    for ad in raw:
        if ad['id'] == args.id:
           thisAd = ad 
           break
    view.onead(ad)


if args.filternames == True:
    theseFilters = helpers.getFilterFile()
    names = ""
    for f in theseFilters:
        names = names + f['name'] + " "
    view.names(names)

