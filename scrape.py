import requests
from bs4 import BeautifulSoup
import time
from urllib.parse import urljoin, urlparse

# Configure your target URLs and credentials
LOGIN_URL = "https://www.arcadepunks.com/login"
START_URL = "https://www.arcadepunks.com/" # The crawler will start here
DOMAIN = "www.arcadepunks.com"             # Keeps the crawler from wandering to other websites
USERNAME = "robforpm"
PASSWORD = "5Co9kzRKui!9lWl%"

def scan_entire_site():
    session = requests.Session()
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    })

    # 1. Log in to the site
    try:
        print("Fetching login page...")
        login_page = session.get(LOGIN_URL)
        login_page.raise_for_status()
        
        payload = {
            "log": USERNAME, 
            "pwd": PASSWORD
        }
        
        print("Attempting to log in...")
        session.post(LOGIN_URL, data=payload)
        
    except requests.exceptions.RequestException as e:
        print(f"Login failed: {e}")
        return

    # 2. Set up the crawler tracking variables
    visited_urls = set()
    urls_to_visit = [START_URL]
    nzb_links = set()

    print("Starting site-wide scan... (This may take a while)")

    # 3. Crawl loop
    while urls_to_visit:
        current_url = urls_to_visit.pop(0)

        # Skip if we've already scanned this exact page
        if current_url in visited_urls:
            continue

        print(f"Scanning: {current_url}")
        visited_urls.add(current_url)

        try:
            response = session.get(current_url, timeout=15)
            
            # Skip downloading non-HTML files (like raw images or zips) during the crawl
            if 'text/html' not in response.headers.get('Content-Type', ''):
                continue
                
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 4. Extract links from the current page
            for link in soup.find_all('a', href=True):
                href = link['href']
                full_url = urljoin(current_url, href) # Converts relative links (/downloads) to full URLs
                parsed_url = urlparse(full_url)

                # Check if it's an NZB file
                if full_url.lower().endswith('.nzb') or '.nzb' in full_url.lower():
                    if full_url not in nzb_links:
                        nzb_links.add(full_url)
                        print(f"--> Found NZB: {full_url}")
                
                # If it's a normal page on the same domain we haven't seen, add to queue
                elif parsed_url.netloc == DOMAIN:
                    if full_url not in visited_urls and full_url not in urls_to_visit:
                        # Ignore common media extensions so the crawler doesn't get stuck
                        ignore_exts = ['.jpg', '.jpeg', '.png', '.gif', '.zip', '.rar', '.7z']
                        if not any(full_url.lower().endswith(ext) for ext in ignore_exts):
                            urls_to_visit.append(full_url)

        except Exception as e:
            print(f"Error loading {current_url}: {e}")

        # Sleep for 1 second between page loads to avoid getting banned for DDoS-like behavior
        time.sleep(1)

    # 5. Save results to a text file on your Windows desktop/folder
    print("\n--- Scan Complete ---")
    if nzb_links:
        print(f"Found {len(nzb_links)} total NZB files.")
        with open("nzb_results.txt", "w") as file:
            for nzb in nzb_links:
                file.write(f"{nzb}\n")
        print("All links have been saved to 'nzb_results.txt' in this folder.")
    else:
        print("No .NZB files found across the site.")

if __name__ == "__main__":
    scan_entire_site()