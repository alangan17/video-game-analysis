if 'data_exporter' not in globals():
    from mage_ai.data_preparation.decorators import data_exporter

import requests
import json
from os import path, makedirs

@data_exporter
def export_data(data, *args, **kwargs):
    """
    Exports data to some source.

    Args:
        data: The output from the upstream parent block
        args: The output from any additional upstream blocks (if applicable)

    Output (optional):
        Optionally return any object and it'll be logged and
        displayed when inspecting the block run.
    """
    print(data)
    

    headers = {'User-Agent': 'App Name: Education purpose', }
    try:
        response = requests.get(data["URL"], headers=headers)
        response.raise_for_status()
    
        res_data = json.loads(response.text)

        # Writing the data to a file in JSON format
        output_fullpath = path.join(data["output_dir"], data["output_filename"])
        # Check if the directory exists
        if not path.exists(data["output_dir"]):
            # The directory does not exist, create it
            makedirs(data["output_dir"])
            print(f'Directory created at: {data["output_dir"]}')
        else:
            # The directory exists
            print(f'Directory already exists: {data["output_dir"]}')

        with open(output_fullpath, 'w') as file:
            json.dump(res_data, file, indent=4)
        print(f"data saved to `{output_fullpath}`")
    
    except requests.exceptions.HTTPError as errh:
        print(f"Http Error: {errh}")
    except requests.exceptions.ConnectionError as errc:
        print(f"Error Connecting: {errc}")
    except requests.exceptions.Timeout as errt:
        print(f"Timeout Error: {errt}")
    except requests.exceptions.RequestException as err:
        print(f"OOps: Something Else: {err}")

    return data
