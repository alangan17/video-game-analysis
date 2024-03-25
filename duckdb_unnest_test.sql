WITH raw_data AS (
  SELECT *
  --FROM read_json_auto('rawg_games_sample.json')
  --FROM read_json_auto('.\data\games_2023*.json')
  FROM read_json_auto('.\data\games_2023-01-01,2023-12-31_40_1.json')
),
unnested_array AS (
  SELECT r.results
  FROM
    raw_data,
    unnest(raw_data.results) as r
),
unnested_dict AS (
    SELECT
        unnest(r.results)
    FROM
        unnested_array as r
)
SELECT
    slug,
    name,
    released
    --unnest(unnested_dict.genres).name as genre_name
    -- unnest(unnested_dict.genres, recursive := true) as genre
FROM unnested_dict
ORDER BY released ASC
;