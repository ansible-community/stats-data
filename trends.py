import csv

from datetime import datetime
from dotenv import dotenv_values
from pytrends.request import TrendReq
from pandas import concat

config = dotenv_values(".env")

GOOGLE_CSV_FILE = config.get("GOOGLE_CSV_FILE") or "google.csv"
TREND_CSV_FILE  = f"trend_{GOOGLE_CSV_FILE}"

# connect to google 
pytrends = TrendReq(hl='en-GB', tz=0) 

# build payload
kw_list = ["/m/0k0vzjb"] # Ansible:Software
pytrends.build_payload(kw_list, cat=0, timeframe='today 1-m')

#1 Interest over Time
data = pytrends.interest_over_time() 
data = data.reset_index() 
data = data.rename(columns={"date": "Date", "/m/0k0vzjb": "Trend"})
data.to_csv(GOOGLE_CSV_FILE, encoding='utf-8', index=False)

# Related queries
rq   = pytrends.related_queries()
top  = rq['/m/0k0vzjb']['top']
top["Type"] = 'top'
rise = rq['/m/0k0vzjb']['rising']
rise["Type"] = 'rising'
rq = concat([top,rise])
rq['Date'] =  datetime.utcnow()
rq = rq[['Date','Type','query','value']]
rq.to_csv(TREND_CSV_FILE, encoding='utf-8', index=False)

## TODO work out how to append...
