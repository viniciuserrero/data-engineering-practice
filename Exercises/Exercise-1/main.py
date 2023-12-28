import os
import shutil
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from urllib.parse import ParseResult, urlparse
from zipfile import ZipFile

import requests

download_uris = [
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2018_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q2.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q3.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2019_Q4.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2020_Q1.zip",
    "https://divvy-tripdata.s3.amazonaws.com/Divvy_Trips_2220_Q1.zip",
]


def clear_environment() -> None:
    shutil.rmtree("downloads", ignore_errors=True)


def validate_url(parsed_url: ParseResult) -> bool:
    return all([parsed_url.scheme, parsed_url.netloc])


def main():
    # Creating downloads folder
    os.makedirs("downloads", exist_ok=True)

    with ThreadPoolExecutor() as executor:
        for uri in download_uris:
            executor.submit(get_file, uri)


def get_file(uri: str) -> bool:
    # Parsing url
    parsed_url = urlparse(uri)
    file_path = parsed_url.path.lstrip("/")

    if not validate_url(parsed_url):
        print(f"Invalid URI: {uri}")
        return False

    # Downloading
    print(f"Downloading {file_path}")
    response = requests.get(uri)

    # Verifying status code
    if not response.ok:
        print(f"Error downloading {file_path}")
        print(response.content)
        return False

    # Extracting
    print(f"Extracting {file_path}")
    with ZipFile(BytesIO(response.content)) as zip_file:
        zip_file.extractall("downloads")

    return True


if __name__ == "__main__":
    clear_environment()
    main()
