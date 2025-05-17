from google.api_core.exceptions import NotFound
import os
import shutil
from google.cloud import storage
from datetime import datetime

def create_customer_folder(customer_id):
    folder_path = f'{customer_id}/'
    return folder_path

def validate_folder_exists(bucket, carpeta_path):
    print(f"Validando existencia de la carpeta", bucket, carpeta_path)
    try:
        blob = bucket.blob(carpeta_path)
        blob.reload()
        return True
    except NotFound:
        return False
    
def connect_to_bucket(bucket_name):
    storage_client = storage.Client()

    bucket = storage_client.get_bucket(bucket_name)

    print(f"Conectado al bucket: {bucket.name}")
    return bucket

def generate_name_file(filename):
    _, extension = os.path.splitext(filename)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    nuevo_nombre = f"{timestamp}{extension}"
    return nuevo_nombre

def download_video_from_gcs(bucket_name, blob_path, destination_file):
    bucket = connect_to_bucket(bucket_name)
    blob = bucket.blob(blob_path)
    blob.download_to_filename(destination_file)
    print(f"Video descargado en: {destination_file}")

def cleanup_files(video_path, frames_dir):
    if os.path.exists(video_path):
        os.remove(video_path)
    if os.path.exists(frames_dir) and os.path.isdir(frames_dir):
        shutil.rmtree(frames_dir)