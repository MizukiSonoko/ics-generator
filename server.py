from flask import Flask, request, redirect, url_for
from flask_mako import MakoTemplates, render_template
import json
import requests
import json
from icalendar import Calendar, Event, vDate
import datetime
import time
import hashlib

UPLOAD_FOLDER = "static/temporary"

app = Flask(__name__, static_folder='static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
mako = MakoTemplates(app)


def convertDate(s):
  try: 
    d = datetime.datetime.strptime(s, '%Y-%m-%d')
    return datetime.date(d.year, d.month, d.day)
  except ValueError as e:
    pass

  try: 
    d = datetime.datetime.strptime(s, '%Y/%m/%d')
    return datetime.date(d.year, d.month, d.day)
  except ValueError as e:
    pass

def convertTime(s):      
  try: 
    return time.strptime(s, '%H:%M:%S')
  except ValueError as e:
    pass

  try: 
    return time.strptime(s, '%H:%M')
  except ValueError as e:
    pass

def merge(d,t):
    	return datetime.datetime(d.year,d.month,d.day,t.tm_hour,t.tm_min)

def getFilename(data):
    r = datetime.datetime(2014,1,2,3,4,5).strftime('%s')
    for d in data:
        r += d["title"]
    return hashlib.sha224(r.encode('utf-8')).hexdigest()

def makeIcs(data):
    ical = Calendar()
    for d in data:
        event = Event()

        start_date = convertDate(d["start_date"])
        start_time = convertTime(d["start_time"])

        # 終わり時間を0:00から変える
        if '00:00' != d["end_time"]:
            end_time = convertTime(d["end_time"])
        else:
            end_time = convertTime("23:59")

        # end_dateが0000/00/00の時は同日と処理する
        if "0000/00/00" == d["end_date"] and "00:00" != d["start_time"]:
            end_date   = convertDate(d["start_date"])
        else:
            end_date   = convertDate(d["end_date"])

        start = merge( start_date, start_time) 
        end = merge( end_date, end_time) 

        # 時間が両方00:00ならば終日として扱う
        if "00:00" == d["end_time"] and "00:00" == d["start_time"]:
            event.add('dtstart', vDate(start))
            event.add('dtend', vDate(end))
        else:
            event.add('dtstart', vDate(start))
            event.add('dtend', vDate(end))
            
        event.add('summary', d["title"])
        event.add('description', d["description"].replace('#nr#','\n'))
        ical.add_component(event)

    filepath = '{}/{}.ics'.format(app.config['UPLOAD_FOLDER'],getFilename(data))
    f = open(filepath, 'wb')
    f.write(ical.to_ical())
    f.close()
    return filepath

def getData():
    url = "https://www.data4citizen.jp/app/users/openDataOutput/json/get/O_EVENTDATA_AIZUWAKAMATSU_CITY"
    res = requests.get(url, params={'start_date': '2018/01/01'})
    ical = Calendar()
    data = json.loads(res.text)    
    return data

@app.route("/", methods=['GET', 'POST'])
def index():
    data = getData()
    return render_template('index.mako',data=data)

def getContainedEvent(data, titles):
    return list(filter(lambda e: e['title'] in titles,data))

@app.route("/generate", methods=['GET', 'POST'])
def generate():
    data = getData()
    if request.method == 'POST':
        titles = []
        for v in request.form.values():
            titles.append(v)
        url = makeIcs(getContainedEvent( data['data'], titles))
        return render_template('result.mako', url="/{}".format(url))

    return redirect('/')

if __name__ == '__main__':
    app.debug = True
    app.run(host='0.0.0.0')