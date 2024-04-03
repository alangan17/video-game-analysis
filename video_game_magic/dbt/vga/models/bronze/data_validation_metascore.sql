{{ config(
    materialized='view',
    post_hook=[
        "{{ log_row_count() }}",
    ],
    tags=[
        "bronze",
        "data_validation"
    ]
) }}

SELECT
    min(metacritic) AS min_metacritic,
    max(metacritic) AS max_metacritic,
    count(metacritic) AS count_metacritic,
    count(game_id) AS count_game
FROM {{ source('ext_tbl', 'external_games') }}
