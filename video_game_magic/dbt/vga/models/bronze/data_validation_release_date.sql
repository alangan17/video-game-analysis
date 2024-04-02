SELECT DISTINCT
    left(released, 7) AS release_date_yyyymm,
    count(DISTINCT released) AS release_date_count,
    min(released) AS min_release_date,
    max(released) AS max_release_date,
    count(DISTINCT game_id) AS game_count
FROM {{ source('ext_tbl', 'external_games') }}
GROUP BY release_date_yyyymm
