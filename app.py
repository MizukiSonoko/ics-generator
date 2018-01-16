
import requests
import json
from icalendar import Calendar, Event, vDate
import datetime

def convertDate(s):
  try: 
    return datetime.datetime.strptime(s, '%Y-%m-%d')
  except ValueError as e:
    pass

  try: 
    return datetime.datetime.strptime(s, '%Y/%m/%d')
  except ValueError as e:
    pass

def convertTime(s):      
  try: 
    return datetime.datetime.strptime(s, '%H:%M:%S')
  except ValueError as e:
    pass

  try: 
    return datetime.datetime.strptime(s, '%H:%M')
  except ValueError as e:
    pass


if __name__ == "__main__":
  

  url = "https://www.data4citizen.jp/app/users/openDataOutput/json/get/O_EVENTDATA_AIZUWAKAMATSU_CITY"

  res = requests.get(url)
  if res.status_code != 200:
    print("Ops!")
    quitz()

  ical = Calendar()
  data = json.loads(res.text)
  for d in data["data"]:
    event = Event()
    start_date = convertDate(d["start_date"])
    start_time = d["start_time"]
    end_date   = d["end_date"]
    end_time   = d["end_time"]
    print("start:",start_date," title:",d["title"])

    #ical.add_component(event)
