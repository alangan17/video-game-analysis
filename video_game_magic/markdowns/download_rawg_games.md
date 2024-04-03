Pipeline Variables:
    endpoint_url
        type: str
        default: "https://api.rawg.io/api/games"
        desc: api endpoint url

    api_array_key_name
        type: str
        default: "results"
        desc: subset of api response to output

    api_start_page_id
        type: int
        default: 1
        desc: api start page id to extract, if you want to continue from interrupted 
            extraction, change `api_start_page_id` and `api_end_page_id`

    api_end_page_id
        type: int or empty string
        default: ""
        desc: api end page id to extract, if you want to continue from interrupted
            extraction, change `api_start_page_id` and `api_end_page_id`

    api_params_page_size
        type: int
        default: 40
        desc: number of records to return in api response['results'], maximum is 40

    api_params_update_dates
        type: str
        default: ""
        desc: whether to filter update dates in api parameter, leave empty string if 
            you need to extract all data

    output_dir:
        type: str
        default: "data"
        desc: local output directory to save the extracted data

    output_file_prefix:
        type: str
        default: "games_latest"
        desc: prefix of the output file

    output_format:
        type: str
        default: "parquet"
        desc: output file format

    gcs_sink_bucket_name:
        type: str
        default: "vga-bucket-01"
        desc: gcs bucket to save the extracted data
    
    cleanup_local_file_after_gcs:
        type: str
        default: 'yes'
        desc: 'yes' or 'no' to cleanup local file after uploading to gcs