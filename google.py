import csv

from apiclient.discovery import build
from datetime import datetime
from dotenv import dotenv_values


config = dotenv_values(".env")

GOOGLE_CSV_FILE = config.get("GOOGLE_CSV_FILE") or "google.csv"

api_key = config["CSE_API_KEY"]
cx = config["CSE_CX"]

google = build("customsearch", "v1", developerKey=api_key)

queries = ("ansible",)

with open(GOOGLE_CSV_FILE, "w", newline="") as csv_file:
    field_names = ("DateTime", "Query", "Total Results")
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for query in queries:
        request = google.cse().list(cx=cx, num=1, q=query)
        resp = request.execute()
        writer.writerow({"DateTime": datetime.utcnow(), "Query": query, "Total Results": resp["searchInformation"]["totalResults"]})
