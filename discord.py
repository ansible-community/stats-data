import csv
import re

from datetime import datetime
from dotenv import dotenv_values
from requests_html import HTMLSession


config = dotenv_values(".env")

DISCORD_CSV_FILE = config.get("DISCORD_CSV_FILE") or "discord.csv"

DISCORD_INVITE = "https://discord.com/invite/sMJjuXb"

session = HTMLSession()
r = session.get(DISCORD_INVITE)

og_description = [meta.attrs.get("content") for meta in r.html.find("meta") if meta.attrs.get("property") == "og:description"][0]
member_count = re.search(r"([\d,]+)", og_description).groups()[0].replace(",", "")

with open(DISCORD_CSV_FILE, "w", newline="") as csv_file:
    field_names = (
        "DateTime",
        "Member Count",
    )
    writer = csv.DictWriter(csv_file, fieldnames=field_names)
    writer.writeheader()

    writer.writerow(
        {
            "DateTime": datetime.utcnow(),
            "Member Count": member_count,
        }
    )
