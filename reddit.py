import csv
import praw

from datetime import datetime
from dotenv import dotenv_values
from functools import reduce


config = dotenv_values(".env")

REDDIT_CSV_FILE = config.get("REDDIT_CSV_FILE") or "reddit.csv"
REDDIT_ENGAGEMENT_CSV_FILE = config.get("REDDIT_ENGAGEMENT_CSV_FILE") or "reddit-engagement.csv"

reddit = praw.Reddit("stats", config_interpolation="basic")
ansible_subreddit = reddit.subreddit("ansible")
ansible_subreddit_traffic = ansible_subreddit.traffic()


with open(REDDIT_CSV_FILE, "w", newline="") as csv_file:
    field_names = (
        "DateTime",
        "Total Ansible Subreddit Subscribers",
        "Previous Week Unique Pageviews",
        "Previous Week Total Pageviews",
        "Previous Week New Subscribers",
    )
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    writer.writerow(
        {
            "DateTime": datetime.utcnow(),
            "Total Ansible Subreddit Subscribers": ansible_subreddit.subscribers,
            "Previous Week Unique Pageviews": reduce(lambda x, y: x + int(y[1]), ansible_subreddit_traffic["day"][:8], int()),
            "Previous Week Total Pageviews": reduce(lambda x, y: x + int(y[2]), ansible_subreddit_traffic["day"][:8], int()),
            "Previous Week New Subscribers": reduce(lambda x, y: x + int(y[3]), ansible_subreddit_traffic["day"][:8], int()),
        }
    )

with open(REDDIT_ENGAGEMENT_CSV_FILE, "w", newline="") as csv_file:
    field_names = (
        "DateTime",
        "Submission Created",
        "Title",
        "Upvotes",
        "Comments",
        "Permalink",
    )
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    for submission in filter(lambda x: x.ups >= 10 or len(x.comments) >= 10, ansible_subreddit.top("week")):
        writer.writerow(
            {
                "DateTime": datetime.utcnow(),
                "Submission Created": datetime.utcfromtimestamp(submission.created_utc),
                "Title": submission.title,
                "Upvotes": submission.ups,
                "Comments": len(submission.comments),
                "Permalink": f"https://www.reddit.com{submission.permalink}",
            }
        )
