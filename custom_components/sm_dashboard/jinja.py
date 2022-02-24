import datetime
import json

def fromjson(value):
    return json.loads(value)

def dayfromnow(day):
    usedate = datetime.date.today()
    usedate += datetime.timedelta(days=day)
    weekday = usedate.strftime("%a")
    return weekday

def windicon(direction):
    switcher = {
        "N": "mdi:arrow-down-thick",
        "NNE": "mdi:arrow-down-thick",
        "NNO": "mdi:arrow-down-thick",
        "NE": "mdi:arrow-bottom-left-thick",
        "NO": "mdi:arrow-bottom-left-thick",
        "ENE": "mdi:arrow-left-thick",
        "ONO": "mdi:arrow-left-thick",
        "E": "mdi:arrow-left-thick",
        "O": "mdi:arrow-left-thick",
        "ESE": "mdi:arrow-left-thick",
        "OZO": "mdi:arrow-left-thick",
        "SE": "mdi:arrow-top-left-thick",
        "ZO": "mdi:arrow-top-left-thick",
        "SSE": "mdi:arrow-up-thick",
        "ZZO": "mdi:arrow-up-thick",
        "S": "mdi:arrow-up-thick",
        "Z": "mdi:arrow-up-thick",
        "SSW": "mdi:arrow-up-thick",
        "ZZW": "mdi:arrow-up-thick",
        "SW": "mdi:arrow-top-right-thick",
        "ZW": "mdi:arrow-top-right-thick",
        "WSW": "mdi:arrow-right-thick",
        "WZW": "mdi:arrow-right-thick",
        "W": "mdi:arrow-right-thick",
        "WNW": "mdi:arrow-right-thick",
        "NW": "mdi:arrow-bottom-right-thick",
        "NNW": "mdi:arrow-down-thick"
    }
    return switcher.get(direction, "mdi:sync")