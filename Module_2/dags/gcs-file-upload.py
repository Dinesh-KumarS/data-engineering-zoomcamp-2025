from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import requests
import gzip
import shutil
import os
from google.cloud import storage

# Constants
GCS_BUCKET = "YOUR_BUCKER_NAME"  # Replace with your GCS bucket name
DOWNLOAD_FOLDER = "/tmp/nyc_taxi_data/"  # Local temp directory for downloads
YEARS = ["2019", "2020", "2021"]
MONTHS = [f"{month:02d}" for month in range(1, 13)]  # Generate 01 to 12
TYPES = ["yellow", "green"]

# Helper functions
def download_file(file_url, local_path):
    response = requests.get(file_url, stream=True)
    response.raise_for_status()
    with open(local_path, "wb") as f:
        for chunk in response.iter_content(chunk_size=1024):
            f.write(chunk)

def extract_gz_file(gz_path, extracted_path):
    with gzip.open(gz_path, "rb") as f_in:
        with open(extracted_path, "wb") as f_out:
            shutil.copyfileobj(f_in, f_out)

def upload_to_gcs(bucket_name, source_file, destination_blob):
    client = storage.Client()
    bucket = client.bucket(bucket_name)
    blob = bucket.blob(destination_blob)
    blob.upload_from_filename(source_file)

def process_file(file_type, year, month, **kwargs):
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    
    file_name = f"{file_type}_tripdata_{year}-{month}.csv.gz"
    file_url = f"https://github.com/DataTalksClub/nyc-tlc-data/releases/download/{file_type}/{file_name}"
    local_gz_path = os.path.join(DOWNLOAD_FOLDER, file_name)
    local_csv_path = local_gz_path.replace(".gz", "")
    
    # Download the file
    download_file(file_url, local_gz_path)
    
    # Extract the file
    extract_gz_file(local_gz_path, local_csv_path)
    
    # Upload to GCS
    gcs_path = f"{file_type}/{year}/{month}/{os.path.basename(local_csv_path)}"
    upload_to_gcs(GCS_BUCKET, local_csv_path, gcs_path)
    
    # Cleanup
    os.remove(local_gz_path)
    os.remove(local_csv_path)

# Define DAG
with DAG(
    dag_id="download_and_upload_nyc_taxi_data_sequential",
    schedule_interval=None,
    start_date=datetime(2025, 1, 1),
    catchup=True,
) as dag:

    previous_task = None

    for year in YEARS:
        for month in MONTHS:
            for file_type in TYPES:
                task = PythonOperator(
                    task_id=f"process_{file_type}_{year}_{month}",
                    python_callable=process_file,
                    op_kwargs={"file_type": file_type, "year": year, "month": month},
                )
                
                # Set dependencies for sequential execution
                if previous_task:
                    previous_task >> task
                
                previous_task = task
