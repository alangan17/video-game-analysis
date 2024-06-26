import json
import math
import os
from os import path

import pandas as pd
import requests

from mage_ai.settings.repo import get_repo_path

if "data_loader" not in globals():
    from mage_ai.data_preparation.decorators import data_loader
if "test" not in globals():
    from mage_ai.data_preparation.decorators import test


def generate_paginated_urls(
    base_url: str,
    output_filename_base: str,
    end_page: int,
    page_size: int = 40,
    start_page: int = 1,
    **kwargs,
) -> list:
    """Generate the urls"""
    # Splitting the URL on '&', replacing the relevant segment, then joining it back
    print(f"{base_url=}")
    parts = base_url.split("&")
    for i, part in enumerate(parts):
        if "page=" in part:
            parts[i] = "page={page}"
        if "page_size=" in part:
            parts[i] = "page_size={page_size}"
        if "updated=" in part:
            parts[i] = "updated={updated}"
    templated_url = "&".join(parts)
    print(templated_url)

    url_list_dict = []
    for page in range(start_page, end_page + 1):
        url_dict = {
            "output_filename": output_filename_base + "_" + str(page),
            "page_id": page,
            "URL": templated_url.format(
                page=page,
                page_size=page_size,
                updated=kwargs.get("api_params_update_dates"),
            ),
        }
        url_list_dict.append(url_dict)
    return url_list_dict


@data_loader
def load_data_from_api(*args, **kwargs):
    """
    Template for loading data from API
    """
    url = kwargs.get("endpoint_url")

    headers = {
        "User-Agent": "App Name: Education purpose",
    }
    params = {
        "key": os.environ["RAWG_API_KEY"],
        # 'ordering': '-released',
        "page_size": kwargs.get("api_params_page_size", 40),  # Max 40
        "page": 1,
        # Filter by update date
        "updated": kwargs.get("api_params_update_dates"),
    }

    # Uncomment this to use real api call
    response = requests.get(url, headers=headers, params=params)
    response.encoding = "utf-8"
    data = json.loads(response.text)

    # Uncomment this to save api call quota
    # # Create a Request object
    # dummy_request = requests.Request(
    #     method="Get",
    #     url=url,
    #     params=params
    # )
    # # Prepare the Request object
    # prepared_request = dummy_request.prepare()
    # response = requests.Response()
    # response.request = prepared_request
    # # Manually set the status code and content of the dummy Response
    # response.status_code = 200
    # response._content = b'Dummy response content'
    # # Manually link the prepared dummy Request to the dummy Response
    # response.request = prepared_request
    ## Read sample file
    # with open("data.json", 'r') as file:
    #     data = json.load(file)

    total_record_count = data.get("count")
    print(f"{total_record_count=}")
    assert total_record_count >= 1, "Total Record Count is invalid"

    total_page_count = math.ceil(
        total_record_count / kwargs.get("api_params_page_size")
    )
    print(f"{total_page_count=}")
    assert total_page_count >= 1, "Total Page Count is invalid"

    end_page = kwargs.get("api_end_page_id", 0)
    print(type(end_page))
    if end_page is None or end_page == "" or end_page == 0:
        end_page = total_page_count

    url_list_dict = generate_paginated_urls(
        base_url=response.request.url,
        output_filename_base=(
            # "games" + "_" +
            # str(kwargs.get("api_params_update_dates").replace(",", "__")) + "_" +
            # str(kwargs.get("api_params_page_size"))
            str(kwargs.get("output_filename_prefix"))
            + "_"
            + str(kwargs.get("api_params_page_size"))
        ),
        page_size=kwargs.get("api_params_page_size"),
        start_page=kwargs.get("api_start_page_id", 1),
        end_page=end_page,
        **kwargs,
    )

    df = pd.DataFrame(url_list_dict)
    df["output_dir"] = path.join(
        path.dirname(get_repo_path()), kwargs.get("output_dir")
    )

    return df


@test
def test_output(output, *args) -> None:
    """
    Template code for testing the output of the block.
    """
    assert output is not None, "The output is undefined"
