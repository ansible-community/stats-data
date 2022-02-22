import csv
import requests

from collections import defaultdict
from datetime import datetime, timedelta
from dotenv import dotenv_values
from time import sleep


config = dotenv_values(".env")

STACKEXCHANGE_CSV_FILE = config.get("STACKEXCHANGE_CSV_FILE") or "stackexchange.csv"
STACKEXCHANGE_TOP_ANSWERERS_CSV_FILE = config.get("STACKEXCHANGE_TOP_ANSWERERS_CSV_FILE") or "stackexchange-top-answerers.csv"
STACKEXCHANGE_NO_ANSWERS_CSV_FILE = config.get("STACKEXCHANGE_NO_ANSWERS_CSV_FILE") or "stackexchange-no-answers.csv"

base_url = "https://api.stackexchange.com"
api_version = "2.3"
backoff = 0

sites = ("stackoverflow", "serverfault", "superuser")
tags = ("ansible",)

stats = defaultdict(dict)


api_endpoint = "tags"

for site in sites:
    for tag in tags:
        sleep(backoff)
        r = requests.get(
            f"{base_url}/{api_version}/{api_endpoint}",
            params={"inname": tag, "order": "desc", "sort": "popular", "site": site},
        )

        if not r.ok:
            raise Exception(r.text)

        resp = r.json()
        backoff = resp.get("backoff", 0)

        for item in resp.get("items", []):
            stats[item["name"]][site] = item["count"]

with open(STACKEXCHANGE_CSV_FILE, "w", newline="") as csv_file:
    field_names = ("DateTime", "Tag", *sites)
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for tag, tag_stats in stats.items():
        writer.writerow({"DateTime": datetime.utcnow(), "Tag": tag, **tag_stats})

sites = ("stackoverflow",)
api_endpoint = "tags"

with open(STACKEXCHANGE_TOP_ANSWERERS_CSV_FILE, "w", newline="") as csv_file:
    field_names = (
        "DateTime",
        "Site",
        "Time Period",
        "user_id",
        "Display Name",
        "Post Count",
        "Score",
        "Accept Rate",
        "Link",
    )
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    time_periods = ("all_time", "month")
    for site in sites:
        for tag in tags:
            for time_period in time_periods:
                sleep(backoff)
                r = requests.get(f"{base_url}/{api_version}/{api_endpoint}/{tag}/top-answerers/{time_period}", params={"site": site, "pagesize": 10})

                if not r.ok:
                    raise Exception(r.text)

                resp = r.json()
                backoff = resp.get("backoff", 0)

                for answerer in resp.get("items", []):
                    writer.writerow(
                        {
                            "DateTime": datetime.utcnow(),
                            "Site": site,
                            "Time Period": time_period,
                            "user_id": answerer["user"]["user_id"],
                            "Display Name": answerer["user"]["display_name"],
                            "Post Count": answerer["post_count"],
                            "Score": answerer["score"],
                            "Accept Rate": answerer["user"].get("accept_rate"),
                            "Link": answerer["user"]["link"],
                        }
                    )


api_endpoint = "questions"

with open(STACKEXCHANGE_NO_ANSWERS_CSV_FILE, "w", newline="") as csv_file:
    field_names = (
        "DateTime",
        "Site",
        "user_id",
        "Display Name",
        "User Link",
        "Question Creation",
        "Question Title",
        "Question Score",
        "Question Link",
    )
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for site in ("stackoverflow",):
        for tag in tags:
            sleep(backoff)
            r = requests.get(
                f"{base_url}/{api_version}/{api_endpoint}/no-answers",
                params={
                    "fromdate": int((datetime.utcnow() - timedelta(days=7)).timestamp()),
                    "order": "asc",
                    "site": site,
                    "tagged": tag,
                },
            )

            if not r.ok:
                raise Exception(r.text)

            resp = r.json()
            backoff = resp.get("backoff", 0)

            for no_answer in resp.get("items", []):
                writer.writerow(
                    {
                        "DateTime": datetime.utcnow(),
                        "Site": site,
                        "user_id": no_answer["owner"]["user_id"],
                        "Display Name": no_answer["owner"]["display_name"],
                        "User Link": no_answer["owner"]["link"],
                        "Question Creation": datetime.utcfromtimestamp(no_answer["creation_date"]),
                        "Question Title": no_answer["title"],
                        "Question Score": no_answer["score"],
                        "Question Link": no_answer["link"],
                    }
                )
