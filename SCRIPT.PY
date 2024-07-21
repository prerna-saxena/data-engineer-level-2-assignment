import requests
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
import os

def download_file(url, dest_folder):
    if not os.path.exists(dest_folder):
        os.makedirs(dest_folder)
    
    filename = os.path.join(dest_folder, url.split("/")[-1])
    retries = Retry(total=5, backoff_factor=1, status_forcelist=[ 502, 503, 504 ])

    with requests.Session() as session:
        session.mount('http://', HTTPAdapter(max_retries=retries))
        response = session.get(url, stream=True)
        if response.status_code == 200:
            with open(filename, 'wb') as f:
                for chunk in response.iter_content(chunk_size=1024):
                    f.write(chunk)
            print(f"Downloaded {filename}")
        else:
            print(f"Failed to download {url}")

# Example URL and destination folder
url = 'http://example.com/data/2019.csv'
dest_folder = './data/2019'
download_file(url, dest_folder)
