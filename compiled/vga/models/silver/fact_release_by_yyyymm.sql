

with
base as (
    select
        `game_id`,
  `tba`,
  `rating`,
  `ratings_count`,
  `metacritic`,
  `reviews_text_count`,
  `suggestions_count`,
  `updated`,
  `reviews_count`,
  `released`
    from `video-game-analysis-418605`.`vga`.`fact_release`
),

filter_released as (
    select *
    from base
    where 1 = 1
    and released is not null
),

add_yyyy_mm as (
    select
        extract(year from released) as release_year,
        extract(month from released) as release_month,
        `game_id`,
  `tba`,
  `rating`,
  `ratings_count`,
  `metacritic`,
  `reviews_text_count`,
  `suggestions_count`,
  `updated`,
  `reviews_count`,
  `released`
    from filter_released
),

add_yyyymm as (
    select
        release_year,
        release_month,
        CAST(CAST(release_year AS STRING) || LPAD(CAST(release_month AS STRING), 2, '0') AS INT) as release_year_month,
        `game_id`,
  `tba`,
  `rating`,
  `ratings_count`,
  `metacritic`,
  `reviews_text_count`,
  `suggestions_count`,
  `updated`,
  `reviews_count`,
  `released`
    from add_yyyy_mm
),

final as (
    select *
    from add_yyyymm
)

select *
from final