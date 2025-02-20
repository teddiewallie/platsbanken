from fastapi import FastAPI
from fastapi.responses import HTMLResponse

import view
import helpers
import fetch
import filters

app = FastAPI()

@app.get("/platsbanken/", response_class=HTMLResponse)
def get_root():
    return helpers.getTextFile("index.html")

@app.get("/platsbanken/filter")
def get_filters():
    theseFilters = helpers.getFilterFile()
    names = ""
    for f in theseFilters:
        names = names + f['name'] + " "
    return {"names": names.strip()}

@app.get("/platsbanken/filter/{filter_name}")
def get_filter(filter_name: str):
    theseFilters = helpers.getFilterFile()
    names = ""
    for f in theseFilters:
        names = names + f['name'] + " "

    if filter_name not in names:
        return {"error": "filter name not found"}
    
    return filters.crunchFilter(filter_name)

