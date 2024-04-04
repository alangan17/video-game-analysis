

with
base as (
    select
        `game_id`,
  `released`,
  `tba`,
  `rating`,
  `ratings_count`,
  `metacritic`,
  `reviews_text_count`,
  `suggestions_count`,
  `updated`,
  `reviews_count`
        from `video-game-analysis-418605`.`source`.`external_games`
    ),

    convert_released as (
        select
            game_id,
            tba,
            rating,
            ratings_count,
            metacritic,
            reviews_text_count,
            suggestions_count,
            parse_timestamp('%Y-%m-%dT%H:%M:%S', updated) as updated,
            reviews_count,
            parse_date('%Y-%m-%d', released) as released
        from base
    ),

    final as (
        select *
        from convert_released
    )

    select unique.*
    from (
        select
            array_agg (
                original
                order by released desc
                limit 1
            )[offset(0)] unique
        from final original
        group by game_id
    )