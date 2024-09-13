from minio import Minio
from minio.error import S3Error
import os

print("Initializing Minio client")
minio_client = Minio(
    "localhost:9000",
    access_key="minioadmin",
    secret_key="minioadmin",
    secure=False
)

def create_bucket(bucket_name):
    """Create a new bucket."""
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            print(f"Bucket '{bucket_name}' created successfully.")
        else:
            print(f"Bucket '{bucket_name}' already exists.")
    except S3Error as err:
        print(f"Failed to create bucket: {err}")

def upload_object(bucket_name, object_name, file_path):
    """Upload an object to a bucket."""
    try:
        minio_client.fput_object(bucket_name, object_name, file_path)
        print(f"Object '{object_name}' uploaded successfully to bucket '{bucket_name}'.")
    except S3Error as err:
        print(f"Failed to upload object: {err}")

def download_object(bucket_name, object_name, file_path):
    """Download an object from a bucket."""
    try:
        minio_client.fget_object(bucket_name, object_name, file_path)
        print(f"Object '{object_name}' downloaded successfully from bucket '{bucket_name}'.")
    except S3Error as err:
        print(f"Failed to download object: {err}")

def update_object(bucket_name, object_name, file_path):
    """Update an existing object by re-uploading it."""
    try:
        upload_object(bucket_name, object_name, file_path)
        print(f"Object '{object_name}' updated successfully in bucket '{bucket_name}'.")
    except S3Error as err:
        print(f"Failed to update object: {err}")

def delete_object(bucket_name, object_name):
    """Delete an object from a bucket."""
    try:
        minio_client.remove_object(bucket_name, object_name)
        print(f"Object '{object_name}' deleted successfully from bucket '{bucket_name}'.")
    except S3Error as err:
        print(f"Failed to delete object: {err}")

def list_objects(bucket_name):
    """List all objects in a bucket."""
    try:
        objects = minio_client.list_objects(bucket_name)
        print(f"Objects in bucket '{bucket_name}':")
        for obj in objects:
            print(obj.object_name)
    except S3Error as err:
        print(f"Failed to list objects: {err}")

def delete_bucket(bucket_name):
    """Delete a bucket."""
    try:
        minio_client.remove_bucket(bucket_name)
        print(f"Bucket '{bucket_name}' deleted successfully.")
    except S3Error as err:
        print(f"Failed to delete bucket: {err}")

# Example usage
if __name__ == "__main__":
    bucket_name = "test-bucket"
    object_name = "example.txt"
    file_path = "requirements.txt"

    print("Creating a new bucket...")
    create_bucket(bucket_name)

    print("Uploading an object...")
    upload_object(bucket_name, object_name, file_path)

    print("List objects in the bucket...")
    list_objects(bucket_name)

    print("Download the object...")
    download_object(bucket_name, object_name, f"downloaded-{object_name}")

    print("update the object...")
    update_object(bucket_name, object_name, file_path)

    print("Delete the object...")
    delete_object(bucket_name, object_name)

    print("Delete the bucket..")
    delete_bucket(bucket_name)
