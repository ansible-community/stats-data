# stats-data

## Repo Overview

This repo contains scripts to scrape various community data points.

## Usage

### Requirements

| Script / Service | Requirements |
| --- | --- |
| discord | None |
| github | None |
| google | Custom Search Engine |
| reddit | Registered reddit bot |
| stackexchange | None |
| twitter | Valid account |
| youtube | Valid API Key |

### Setup

```
python3 -m venv ./.venv
source .venv/bin/activate  # (or activate.fish, activate.zsh, etc)
pip install -r requirements.txt
```

### Configuration

Example `.env`

```
# Required
CSE_API_KEY='GOOGLE_API_KEY'
CSE_CX='GOOGLE_CX_KEY'
TWITTER_AUTHORIZATION_HEADER='Bearer TWITTER_BEARER_TOKEN'
YOUTUBE_API_KEY='GOOGLE_API_KEY'

# Optional
DISCORD_CSV_FILE='discord_file_from_env.csv'
GITHUB_CSV_FILE='github_file_from_env.csv'
GOOGLE_CSV_FILE='google_file_from_env.csv'
REDDIT_CSV_FILE='reddit_file_from_env.csv'
REDDIT_ENGAGEMENT_CSV_FILE='reddit_engagement_file_from_env.csv'
STACKEXCHANGE_CSV_FILE='stackexchange_file_from_env.csv'
STACKEXCHANGE_TOP_ANSWERERS_CSV_FILE='stackexchange_top_answerers_file_from_env.csv'
STACKEXCHANGE_NO_ANSWERS_CSV_FILE='stackexchange_no_answers_file_from_env.csv'
TWITTER_CSV_FILE='twitter_file_from_env.csv'
YOUTUBE_CSV_FILE='youtube_file_from_env.csv'
```

Example `praw.ini`

```
[stats]
bot_name=stats
bot_version=0.0.1
bot_author=REDDIT_USERNAME

client_id=REDDIT_CLIENT_ID
client_secret=REDDIT_CLIENT_SECRET

username=REDDIT_USERNAME
password=REDDIT_PASSWORD

user_agent=script:%(bot_name)s:v%(bot_version)s (by u/%(bot_author)s)

```

See https://praw.readthedocs.io/en/stable/getting_started/configuration/prawini.html for more info.
