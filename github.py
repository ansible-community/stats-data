import csv
import requests

from datetime import datetime
from dotenv import dotenv_values


config = dotenv_values(".env")

GITHUB_CSV_FILE = config.get("GITHUB_CSV_FILE") or "github.csv"

headers = {"Accept": "application/vnd.github.v3+json"}
base_url = "https://api.github.com"
api_endpoint = "repos"

owner = "ansible"
repo = "ansible"


r = requests.get(f"{base_url}/{api_endpoint}/{owner}/{repo}", headers=headers)

if not r.ok:
    raise Exception(r.text)

resp = r.json()

keys = sorted([key for key in resp.keys() if "count" in key])

with open(GITHUB_CSV_FILE, "w", newline="") as csv_file:
    field_names = ("DateTime", "Repo", *keys)
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    row = {
        "DateTime": datetime.utcnow(),
        "Repo": f"{owner}/{repo}",
    }

    for key in keys:
        row[key] = resp[key]

    writer.writerow(row)
