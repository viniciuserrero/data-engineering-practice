import requests
import pandas
import re
import shutil
import os
from urllib.parse import urlparse

URL = "https://www.ncei.noaa.gov/data/local-climatological-data/access/2021/"


def clear_environment() -> None:
    shutil.rmtree("downloads", ignore_errors=True)


def validate_url(url: str) -> None:
    parsed_url = urlparse(url)
    if not all([parsed_url.scheme, parsed_url.netloc]):
        raise Exception("Invalid URL")


def main():
    # Creating downloads folder
    os.makedirs("downloads", exist_ok=True)

    # First request to website to scrape
    validate_url(URL)
    response = requests.get(URL)

    if not response.ok:
        raise Exception("Error while trying to connect to source")

    # Using regex to find file name in a line that contains the specified date
    line_regex = r"\n.*?2022-02-07 14:03.*?\n"
    file_name_regex = r"href=\"(.*?)\""

    line = re.search(line_regex, response.text).group()
    file_name = re.search(file_name_regex, line).group().lstrip("'href=\"").rstrip('"')

    # Downloading the file
    download_url = os.path.join(URL, file_name)
    file = requests.get(download_url)

    file_path = os.path.join("downloads", file_name)
    with open(file_path, "wb") as f:
        f.write(file.content)

    # Using pandas to extract maximum temperature
    df = pandas.read_csv(file_path)
    max_temp = df["HourlyDryBulbTemperature"].max()
    print(f"The maximum temperature is {max_temp}°")


if __name__ == "__main__":
    clear_environment()
    main()
