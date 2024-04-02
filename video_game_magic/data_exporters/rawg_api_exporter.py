from mage_ai.settings.repo import get_repo_path
from mage_ai.io.config import ConfigFileLoader
from mage_ai.io.google_cloud_storage import GoogleCloudStorage
from os import path, makedirs, remove

import requests
import json
import pandas as pd

if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

def normalize_data(
        data,
        array_key_name:str="results"
    ):

    # Ensure each item in 'results' has the 'parent_platforms' key
    for item in data['results']:
        if 'parent_platforms' not in item:
            item['parent_platforms'] = []

        if 'platforms' not in item:
            item['platforms'] = []

        if 'stores' not in item:
            item['stores'] = []

        if 'genres' not in item:
            item['genres'] = []

        if 'tags' not in item:
            item['tags'] = []

    df_games = pd.json_normalize(data=data[array_key_name])
    df_games.rename(columns={'id': 'game_id'}, inplace=True)
    df_games.columns = [col.replace('.', '_') for col in df_games.columns]

    dataframe_schema = {
        'game_id': 'int64',
        'slug': 'object',  # String, using object for textual data
        'name': 'object',
        'released': 'object',
        'tba': 'bool',
        'rating': 'float64',
        'rating_top': 'float64',
        'ratings_count': 'int64',
        'metacritic': 'float64',
        'reviews_text_count': 'int64',
        'playtime': 'float64',
        'suggestions_count': 'int64',
        'added': 'float64',
        'suggestions_count': 'int64',
        'updated': 'object',  # Assuming date format, convert similar to 'released'
        'reviews_count': 'int64',
        'saturated_color': 'object',  # Color code, string
        'dominant_color': 'object',  # Color code, string
    }

    # Example of converting the DataFrame to match the defined schema
    df_games = df_games[dataframe_schema.keys()]
    for column, dtype in dataframe_schema.items():
        try:
            df_games[column] = df_games[column].astype(dtype)
        except KeyError:
            print(f"Column {column} not found in DataFrame.")
        except Exception as e:
            print(f"Error converting column {column} to {dtype}: {e}")
    print(f"{df_games.info()=}")

    # Flatten nested structures
    df_platforms = pd.json_normalize(data['results'], record_path='platforms', meta=['id'], meta_prefix='game_')
    df_platforms.columns = [col.replace('.', '_') for col in df_platforms.columns]
    print(f"{df_platforms.info()=}")

    df_parent_platforms = pd.json_normalize(data['results'], record_path='parent_platforms', meta=['id'], meta_prefix='game_')
    df_parent_platforms.columns = [col.replace('.', '_') for col in df_parent_platforms.columns]
    print(f"{df_parent_platforms.info()=}")

    df_stores = pd.json_normalize(data['results'], record_path='stores', meta=['id'], meta_prefix='game_')
    df_stores.columns = [col.replace('.', '_') for col in df_stores.columns]
    print(f"{df_stores.info()=}")

    df_tags = pd.json_normalize(data['results'], record_path='tags', meta=['id'], meta_prefix='game_')
    df_tags.columns = [col.replace('.', '_') for col in df_tags.columns]
    print(f"{df_tags.info()=}")

    df_genres = pd.json_normalize(data['results'], record_path='genres', meta=['id'], meta_prefix='game_')
    df_genres.columns = [col.replace('.', '_') for col in df_genres.columns]
    print(f"{df_genres.info()=}")

    return {
        "games": df_games,
        "platforms": df_platforms,
        "parent_platforms": df_parent_platforms,
        "stores": df_stores,
        "tags": df_tags,
        "genres": df_genres
    }

def upload_json_to_gcs(bucket_name, destination_blob_name, data):
    try:
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        # Upload the JSON string
        blob.upload_from_string(data, content_type='application/json')
        print(f"File {destination_blob_name} uploaded to {bucket_name}.")
    except Exception as e:
        print(f"Failed to upload file: {str(e)}")

@data_exporter
def export_data_to_google_cloud_storage(data, **kwargs) -> None:
    """
    Template code for a transformer block.

    Add more parameters to this function if this block has multiple parent blocks.
    There should be one parameter for each output variable from each parent block.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Returns:
        Anything (e.g. data frame, dictionary, array, int, str, etc.)
    """
    config_path = path.join(get_repo_path(), 'io_config.yaml')
    config_profile = 'default'

    bucket_name = kwargs.get('gcs_sink_bucket_name')

    print(data)
    
    headers = {'User-Agent': 'App Name: Education purpose', }
    try:
        # Real api call
        response = requests.get(data["URL"], headers=headers)
        response.raise_for_status()
        res_data = json.loads(response.text)

        # Read json data (dev mode)
        # with open("/home/src/data/source/games_2024-01-01__2024-01-01_40_1.json", 'r') as file:
            # res_data = json.load(file)

        # Flatten json data and split into 5 datasets
        df_datasets = normalize_data(
            res_data,
            array_key_name=kwargs.get("api_array_key_name")
        )

        # Split output settings per dataframe
        output_setup = []
        for key, item in df_datasets.items():
            output_filename = data["output_filename"] + "_" + key + ".parquet"
            output_dir_gcs = kwargs.get("gcs_sink_bucket_name") + "/" + key
            output_dir_local = data["output_filename"] + "/" + key
            output_fullpath = path.join(data["output_dir"], output_filename)

            item.to_parquet(output_fullpath, index=False)

            # Upload data to GCS
            object_key = path.join(key, output_filename)
            GoogleCloudStorage.with_config(ConfigFileLoader(config_path, config_profile)).export(
                output_fullpath,
                bucket_name,
                object_key,
            )
            print(f"data saved to bucket: `{bucket_name}`, path: `{object_key}`")

            if kwargs.get("clenup_local_file_after_gcs", "yes").lower() == 'yes':
                remove(output_fullpath)

    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else: {err}")
