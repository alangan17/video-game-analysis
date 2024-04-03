{{ config(
    materialized='incremental',
    unique_key='game_id',
    partition_by={
      "field": "released",
      "data_type": "DATE",
      "granularity": "YEAR"
    },
    post_hook=[
        "{{ log_row_count() }}",
    ],
    tags=[
        "bronze",
        "fact"
    ]
) }}

with
base as (
    select
        {{ dbt_utils.star(
            from=ref('fact_release_temp')
        ) }}
        from {{ ref('fact_release_temp') }}
    )

    select *
    from base
