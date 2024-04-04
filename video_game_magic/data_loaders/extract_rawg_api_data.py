from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader
from datetime import datetime, timedelta

def get_date_yyyymmdd(dayoffset=1):
    today_date = datetime.now()
    date_str = today_date + timedelta(days=dayoffset)
    return date_str.strftime('%Y-%m-%d')

@data_loader
def trigger(*args, **kwargs):
    """
    Trigger Pipeline `download_rawg_games`
    """

    extract_api_mode = kwargs.get("extract_api_mode", "latest").lower()
    if extract_api_mode == 'latest':
        api_start_date = get_date_yyyymmdd(
            dayoffset = kwargs.get("extract_api_date_offset", -1)
        )
        api_end_date = get_date_yyyymmdd(
            dayoffset = 0
        )
        api_params_update_dates = (
            f"{api_start_date},{api_end_date}"
        )
        
    if extract_api_mode == 'historical':
        # Get all API data (as of 2024-04-03, will produce about 865342/40 = 21635 request)
        api_params_update_dates = ""

    assert extract_api_mode in ['latest', 'historical'], "extract_api_mode should be either `latest` or `historical`"
    print(f"{api_params_update_dates = }")

    trigger_pipeline(
        'download_rawg_games',  # Required: enter the UUID of the pipeline to trigger
        variables={
            "api_array_key_name": "results",
            "api_end_page_id": "",
            "api_params_page_size": 40,
            "api_params_update_dates": api_params_update_dates,
            "api_start_page_id": 1,
            "cleanup_local_file_after_gcs": "yes",
            "endpoint_url": "https://api.rawg.io/api/games",
            "gcs_sink_bucket_name": kwargs.get("gcs_bucket", "vga-bucket-latest"),
            "output_dir": "data",
            "output_filename_prefix": "games_latest",
            "output_format": "parquet"
        },                      # Optional: runtime variables for the pipeline
        check_status=True,      # Optional: poll and check the status of the triggered pipeline
        error_on_failure=True,  # Optional: if triggered pipeline fails, raise an exception
        poll_interval=10,       # Optional: check the status of triggered pipeline every N seconds
        poll_timeout=kwargs.get(
            "pipeline_timeout", 300
        ),                      # Optional: raise an exception after N seconds
        verbose=True,           # Optional: print status of triggered pipeline run
    )
