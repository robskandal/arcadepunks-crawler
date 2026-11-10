# ArcadePunks .NZB Crawler

A Python-based web scraper and crawler designed to systematically scan `arcadepunks.com` and extract all available `.NZB` download links. 

## What It Does
* **Authenticates:** Logs into the website using your provided credentials to access protected pages.
* **Spiders the Domain:** Starts at the homepage and systematically crawls internal links without wandering off to external websites.
* **Extracts .NZB Links:** Parses the HTML of every visited page to find and collect links pointing to `.nzb` files.
* **Polite Crawling:** Includes a 1-second delay between page requests to prevent server overload and avoid IP bans.
* **Exports Data:** Saves all discovered links into a clean `nzb_results.txt` file on your machine.

## Prerequisites
* **OS:** Windows 10 (or any OS that supports Python)
* **Python:** Python 3.x installed
* **Libraries:** `requests` and `beautifulsoup4`

## Installation & Setup

1. **Clone the repository** (or download the files):
   ```bash
   git clone [https://github.com/YOUR_USERNAME/arcadepunks-crawler.git](https://github.com/YOUR_USERNAME/arcadepunks-crawler.git)
   cd arcadepunks-crawler
