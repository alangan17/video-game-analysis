from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def trigger(*args, **kwargs):
    """
    Trigger pipeline `load_gcs_to_bq`
    """
    bq_project_id = kwargs.get("bigquery_project_id", "video-game-analysis-123456")

    trigger_pipeline(
        'load_gcs_to_bq',        # Required: enter the UUID of the pipeline to trigger
        variables={
            "bq_table_name_games": f"{bq_project_id}.source.external_games",
            "bq_table_name_genres": f"{bq_project_id}.source.external_genres",
            "bq_table_name_parent_platforms": f"{bq_project_id}.source.external_parent_platforms",
            "bq_table_name_platforms": f"{bq_project_id}.source.external_platforms",
            "bq_table_name_stores": f"{bq_project_id}.source.external_stores",
            "bq_table_name_tags": f"{bq_project_id}.source.external_tags",
            "gcs_bucket_name": kwargs.get("gcs_bucket", "vga-bucket-latest"),
        },                      # Optional: runtime variables for the pipeline
        check_status=True,      # Optional: poll and check the status of the triggered pipeline
        error_on_failure=True,  # Optional: if triggered pipeline fails, raise an exception
        poll_interval=10,       # Optional: check the status of triggered pipeline every N seconds
        poll_timeout=kwargs.get(
            "pipeline_timeout", 300
        ),                      # Optional: raise an exception after N seconds
    )
