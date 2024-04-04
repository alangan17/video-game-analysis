from mage_ai.orchestration.triggers.api import trigger_pipeline
if 'data_loader' not in globals():
    from mage_ai.data_preparation.decorators import data_loader


@data_loader
def trigger(*args, **kwargs):
    """
    Trigger pipeline `transform_bi_models`
    """

    trigger_pipeline(
        'transform_bi_models',  # Required: enter the UUID of the pipeline to trigger
        variables={},           # Optional: runtime variables for the pipeline
        check_status=True,      # Optional: poll and check the status of the triggered pipeline
        error_on_failure=True,  # Optional: if triggered pipeline fails, raise an exception
        poll_interval=10,       # Optional: check the status of triggered pipeline every N seconds
        poll_timeout=kwargs.get(
            "pipeline_timeout", 300
        ),                      # Optional: raise an exception after N seconds
    )
