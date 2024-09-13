import pytest
from uuid import uuid4

# Import the functions from the client code
from minio_client import (  
    create_bucket, upload_object, download_object, update_object,
    delete_object, list_objects, delete_bucket, minio_client
)

# Utility function for creating a unique bucket name for tests
def unique_bucket_name():
    return f"test-bucket-{uuid4()}"

# Setup and teardown for bucket creation and deletion
@pytest.fixture
def test_bucket():
    bucket_name = unique_bucket_name()
    create_bucket(bucket_name)
    yield bucket_name
    delete_bucket(bucket_name)

def test_create_bucket(test_bucket):
    """Test the creation of a new bucket."""
    assert minio_client.bucket_exists(test_bucket), "Bucket should exist after creation."

def test_upload_object(test_bucket, tmp_path):
    """Test uploading an object to a bucket."""
    file_path = tmp_path / "testfile.txt"
    object_name = "testfile.txt"

    # Create a sample file to upload
    file_path.write_text("This is a test file.")

    # Test upload
    upload_object(test_bucket, object_name, str(file_path))
    objects = list(minio_client.list_objects(test_bucket))
    assert object_name in [obj.object_name for obj in objects], "Object should be uploaded."

def test_download_object(test_bucket, tmp_path):
    """Test downloading an object from a bucket."""
    file_path = tmp_path / "testfile.txt"
    object_name = "testfile.txt"

    # Create a sample file and upload it first
    file_path.write_text("This is a test file.")
    upload_object(test_bucket, object_name, str(file_path))

    # Test download
    download_path = tmp_path / f"downloaded-{object_name}"
    download_object(test_bucket, object_name, str(download_path))
    assert download_path.exists(), "Downloaded file should exist."
    assert download_path.read_text() == "This is a test file.", "Downloaded file content should match."

def test_update_object(test_bucket, tmp_path):
    """Test updating an object in a bucket."""
    file_path = tmp_path / "testfile.txt"
    object_name = "testfile.txt"

    # Upload initial file
    file_path.write_text("This is a test file.")
    upload_object(test_bucket, object_name, str(file_path))

    # Update file content
    file_path.write_text("This is an updated test file.")
    update_object(test_bucket, object_name, str(file_path))

    # Download and verify the update
    download_path = tmp_path / f"downloaded-{object_name}"
    download_object(test_bucket, object_name, str(download_path))
    assert download_path.read_text() == "This is an updated test file.", "Object content should be updated."

def test_delete_object(test_bucket, tmp_path):
    """Test deleting an object from a bucket."""
    file_path = tmp_path / "testfile.txt"
    object_name = "testfile.txt"

    # Create a sample file and upload it first
    file_path.write_text("This is a test file.")
    upload_object(test_bucket, object_name, str(file_path))

    # Test delete
    delete_object(test_bucket, object_name)
    objects = list(minio_client.list_objects(test_bucket))
    assert object_name not in [obj.object_name for obj in objects], "Object should be deleted."

def test_list_objects(test_bucket, tmp_path):
    """Test listing objects in a bucket."""
    file_path = tmp_path / "testfile.txt"
    object_name = "testfile.txt"

    # Upload a file to the bucket
    file_path.write_text("This is a test file.")
    upload_object(test_bucket, object_name, str(file_path))

    # List objects and check
    objects = minio_client.list_objects(test_bucket)
    object_names = [obj.object_name for obj in objects]
    assert object_name in object_names, "Uploaded object should appear in the list."
