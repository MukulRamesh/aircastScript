import dateutil.parser
import requests
import dateutil
from pytimeparse import parse
import datetime
import json

cache = {}

def getOpenAQ(temporal, date_to, date_from):

    # temporal = "hour" # or "day"
    # date_to = "2023-11-20"
    # date_from = "2023-11-19"
    # limit = "1"

    dateTo =  min(datetime.datetime.today(), dateutil.parser.parse(date_to) + datetime.timedelta(days=2)).date()
    dateFrom = (dateutil.parser.parse(date_from) - datetime.timedelta(days=1)).date()

    if (temporal, dateTo, dateFrom) in cache:
        print("Got cached OpenAQ data!")
        return cache[(temporal, dateTo, dateFrom)]

    diff = dateTo - dateFrom

    limit = (diff.total_seconds() / parse(f"1 {temporal}")).__ceil__()

    url = f"https://api.openaq.org/v2/averages?temporal={temporal}&parameters_id=2&date_to={str(dateTo)}&date_from={str(dateFrom)}&locations_id=921018&spatial=location&limit={limit}&page=1"
    # url = "https://api.openaq.org/v2/locations?limit=100000&parameter_id=2&coordinates=40.220%2C-74.759&radius=1000&order_by=lastUpdated&dump_raw=false"

    headers = {
        "X-API-Key": "b7c9991776536050673fb080ef4e4fd678ac7110bc63693689bd195b3b20807f",
        "accept": "application/json"

        }

    print("Sending OpenAQ API request...")
    try:
        res = requests.get(url, headers=headers)

        timeList = []
        valueList = []
        for entry in res.json()["results"]:
            time = entry[temporal]
            value = entry["average"]

            timeList.append(datetime.datetime.fromisoformat(time))
            valueList.append(value)

        print(f"OpenAQ entries documented: {limit}")
        print(f"OpenAQ API query found entries: " + str(res.json()["meta"]["found"])) #if 0, then warn and abort
    except KeyError:
        print(json.dumps(res.json(), indent=4))
        raise Exception("Got bad data from OpenAQ API...")
        
    cache[(temporal, dateTo, dateFrom)] = (timeList, valueList)
    return (timeList, valueList)


