import csv

from apiclient.discovery import build
from datetime import datetime
from dotenv import dotenv_values


config = dotenv_values(".env")

YOUTUBE_CSV_FILE = config.get("YOUTUBE_CSV_FILE") or "youtube.csv"

api_key = config["YOUTUBE_API_KEY"]

youtube = build("youtube", "v3", developerKey=api_key)

queries = ("ansible",)

with open(YOUTUBE_CSV_FILE, "w", newline="") as csv_file:
    field_names = ("DateTime", "Query", "Total Results")
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for query in queries:
        request = youtube.search().list(part="snippet", maxResults=0, q=query)
        resp = request.execute()
        writer.writerow({"DateTime": datetime.utcnow(), "Query": query, "Total Results": resp["pageInfo"]["totalResults"]})
