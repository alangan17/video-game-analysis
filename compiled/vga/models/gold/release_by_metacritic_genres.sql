

with
base as (
    select
        
*
/* No columns were returned. Maybe the relation doesn't exist yet 
or all columns were excluded. This star is only output during  
dbt compile, and exists to keep SQLFluff happy. */
            
        from `video-game-analysis-418605`.`vga`.`fact_release_by_yyyymm`
    ),

    genres as (
        select
        `genre_id`,
  `genre_name`,
  `genre_slug`,
  `game_id`,
  `game_genre_id`
            from `video-game-analysis-418605`.`vga`.`dim_genres`
        ),

        has_metacritic as (
            select *
            from base
            where
                1 = 1
                and metacritic is not null
        ),

        release_join_genres as (
            select
                r.*,
                g.genre_name
            from has_metacritic as r
            left join genres
                as g on 1 = 1
            and r.game_id = g.game_id
        ),

        final as (
            select
                release_year,
                release_month,
                release_year_month,
                released,

                genre_name,

                metacritic,
                game_id
            from release_join_genres
        )

        select *
        from final