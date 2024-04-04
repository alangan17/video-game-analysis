if 'custom' not in globals():
    from mage_ai.data_preparation.decorators import custom
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test

from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from google.cloud import storage
from os import path
from concurrent.futures import ThreadPoolExecutor, as_completed

def delete_blob(bucket_name, blob_name):
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    storage_client = GoogleCloudStorage.with_config(
        ConfigFileLoader(config_path, config_profile)
    ).client

    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    blob.delete()
    print(f"Deleted: {blob_name}")

def purge_all_files_in_bucket(bucket_name):
    # Create a Google Cloud Storage client
    config_path = path.join(get_repo_path(), "io_config.yaml")
    config_profile = "default"
    storage_client = GoogleCloudStorage.with_config(
        ConfigFileLoader(config_path, config_profile)
    ).client

    print(f"{bucket_name=}")
    bucket = storage_client.bucket(bucket_name)
    blobs = list(bucket.list_blobs())  # Convert to list for accurate count
    
    with ThreadPoolExecutor(max_workers=20) as executor:
        futures = [executor.submit(delete_blob, bucket_name, blob.name) for blob in blobs]
        for future in as_completed(futures):
            try:
                future.result()  # Wait for each future to complete.
            except Exception as exc:
                print(f'Generated an exception: {exc}')

@custom
def transform_custom(*args, **kwargs):
    bucket_name = kwargs.get("gcs_bucket_name")

    # config_path = path.join(get_repo_path(), "io_config.yaml")
    # config_profile = "default"
    # storage_client = GoogleCloudStorage.with_config(
    #     ConfigFileLoader(config_path, config_profile)
    # ).client

    # # Get the GCS bucket
    # bucket = storage_client.bucket(
    #     kwargs.get("gcs_bucket_name")
    # )
    
    # # List all objects in the bucket
    # blobs = bucket.list_blobs()
    
    # # Loop through all objects and delete them
    # for blob in blobs:
    #     blob.delete()
    #     print(f"{blob.name}")


    purge_all_files_in_bucket(bucket_name)


    return {}


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
