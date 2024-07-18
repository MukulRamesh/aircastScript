import dateutil.parser
import requests
import dateutil
from pytimeparse import parse



def getOpenAQ(temporal, date_to, date_from):

    # temporal = "hour" # or "day"
    # date_to = "2023-11-20"
    # date_from = "2023-11-19"
    # limit = "1"

    diff = dateutil.parser.parse(date_to) - dateutil.parser.parse(date_from)

    limit = (diff.total_seconds() / parse(f"1 {temporal}")).__ceil__()

    url = f"https://api.openaq.org/v2/averages?temporal={temporal}&parameters_id=2&date_to={date_to}&date_from={date_from}&locations_id=921018&spatial=location&limit={limit}&page=1"
    # url = "https://api.openaq.org/v2/locations?limit=100000&parameter_id=2&coordinates=40.220%2C-74.759&radius=1000&order_by=lastUpdated&dump_raw=false"

    headers = {
        "X-API-Key": "b7c9991776536050673fb080ef4e4fd678ac7110bc63693689bd195b3b20807f",
        "accept": "application/json"

        }

    res = requests.get(url, headers=headers)

    timeList = []
    valueList = []
    for entry in res.json()["results"]:
        time = entry["hour"]
        value = entry["average"]

        timeList.append(time)
        valueList.append(value)

    print(f"OpenAQ entries documented: {limit}")
    print(f"OpenAQ API query found entries: " + str(res.json()["meta"]["found"])) #if 0, then warn and abort

    return timeList, valueList