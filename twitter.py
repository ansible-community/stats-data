import csv
import requests

from datetime import datetime
from dotenv import dotenv_values


config = dotenv_values(".env")

TWITTER_CSV_FILE = config.get("TWITTER_CSV_FILE") or "twitter.csv"

base_url = "https://api.twitter.com/2"
headers = {"Authorization": config["TWITTER_AUTHORIZATION_HEADER"]}


endpoint = "users"
username = "ansible"
params = {"user.fields": "public_metrics"}
r = requests.get(f"{base_url}/{endpoint}/by/username/{username}", headers=headers, params=params)

if not r.ok:
    raise Exception(r.text)

resp = r.json()
followers_count = resp["data"]["public_metrics"]["followers_count"]


endpoint = "tweets"
params = {"query": "#ansible OR @ansible", "granularity": "day"}
r = requests.get(f"{base_url}/{endpoint}/counts/recent", headers=headers, params=params)

if not r.ok:
    raise Exception(r.text)

resp = r.json()
total_tweet_count = resp["meta"]["total_tweet_count"]


with open(TWITTER_CSV_FILE, "w", newline="") as csv_file:
    field_names = (
        "DateTime",
        "Key",
        "Value",
    )
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    writer.writerow(
        {
            "DateTime": datetime.utcnow(),
            "Key": f"{username} account followers",
            "Value": followers_count,
        }
    )
    writer.writerow(
        {
            "DateTime": datetime.utcnow(),
            "Key": "'#ansible OR @ansible' tweet count from last 7 days",
            "Value": total_tweet_count,
        }
    )
