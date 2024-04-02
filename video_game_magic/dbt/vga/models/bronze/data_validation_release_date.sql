SELECT distinct
  left(released, 7) as release_date_YYYYMM,
  count(distinct released) as release_date_count,
  min(released) as min_release_date,
  max(released) as max_release_date,
  count(distinct game_id) as game_count
FROM {{ source('ext_tbl', 'external_games') }} 
GROUP BY release_date_YYYYMM