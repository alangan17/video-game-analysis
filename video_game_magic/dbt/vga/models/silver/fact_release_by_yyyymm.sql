{{ config(
    materialized='view',
    partition_by={
      "field": "released",
      "data_type": "date",
      "granularity": "month"
    },
    cluster_by = "game_id",
    post_hook=[
        "{{ log_row_count() }}",
    ],
    tags=[
        "silver",
        "fact"
    ]
) }}

with
base as (
    select
        {{ dbt_utils.star(
            from=ref('fact_release')
        ) }}
    from {{ ref('fact_release') }}
),

filter_released as (
    select *
    from base
    where 1 = 1
    and released is not null
),

add_yyyy_mm as (
    select
        {{ dbt_date.date_part('year', 'released') }} as release_year,
        {{ dbt_date.date_part('month', 'released') }} as release_month,
        {{ dbt_utils.star(
            from=ref('fact_release')
        ) }}
    from filter_released
),

add_yyyymm as (
    select
        release_year,
        release_month,
        CAST(CAST(release_year AS STRING) || LPAD(CAST(release_month AS STRING), 2, '0') AS INT) as release_year_month,
        {{ dbt_utils.star(
            from=ref('fact_release')
        ) }}
    from add_yyyy_mm
),

final as (
    select *
    from add_yyyymm
)

select *
from final
