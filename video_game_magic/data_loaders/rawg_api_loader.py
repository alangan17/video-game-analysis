import io
import os
import json
import pandas as pd
import requests
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if 'test' not in globals():
    from mage_ai.data_preparation.decorators import test


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = kwargs.get("endpoint_url")

    # Add parameters
    params = {
        'key': os.environ['RAWG_API_KEY'],
        # Add more parameters as needed
    }

    response = requests.get(url, params=params)

    # Assuming the response contains JSON data, parse it into a Python dictionary
    data = response.json()

    # Specify the file name you want to save the data to
    file_name = 'data.json'

    # Writing the data to a file in JSON format
    with open(file_name, 'w') as file:
        json.dump(data, file, indent=4)

    return {
        "endpoint": url,
        "output_filename": file_name
    }


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, 'The output is undefined'
