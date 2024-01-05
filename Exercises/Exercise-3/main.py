import boto3
import shutil
import os
import gzip

def clear_environment() -> None:
    shutil.rmtree("downloads", ignore_errors=True)

def main():
    s3 = boto3.client('s3')
    bucket = "commoncrawl"
    file_name = "wet.paths.gz"
    file_path = f"downloads/{file_name}"
    key = f"crawl-data/CC-MAIN-2022-05/{file_name}"

    # Creating downloads folder
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    s3.download_file(bucket, key, file_path)
    
    with gzip.open(file_path, 'rb') as f:
        file_content = f.read()
    

    # Downloading first file of list
    list_of_files = file_content.decode("utf-8").split("\n")
    second_file_name = list_of_files[0].split("/")[-1]
    second_file_path = f"downloads/{second_file_name}"
    s3.download_file(bucket, list_of_files[0], second_file_path)

    # Printing all lines
    for file in list_of_files:
        print(file)


if __name__ == "__main__":
    clear_environment()
    main()
