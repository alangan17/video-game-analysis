

with
base as (
    select
        
*
/* No columns were returned. Maybe the relation doesn't exist yet 
or all columns were excluded. This star is only output during  
dbt compile, and exists to keep SQLFluff happy. */
            
        from `video-game-analysis-418605`.`vga`.`fact_release_by_yyyymm`
    ),

    parent_platform as (
        select
        `parent_platform_id`,
  `parent_platform_name`,
  `parent_platform_slug`,
  `game_id`,
  `game_parent_platform_id`
            from `video-game-analysis-418605`.`vga`.`dim_parent_platforms`
        ),

        has_metacritic as (
            select *
            from base
            where
                1 = 1
                and metacritic is not null
        ),

        release_join_parent_platform as (
            select
                r.*,
                p.parent_platform_name as platform_name
            from has_metacritic as r
            left join parent_platform as p
                on
                    1 = 1
                    and r.game_id = p.game_id
        ),

        final as (
            select
                release_year,
                release_month,
                release_year_month,
                released,

                platform_name,

                metacritic,
                game_id
            from release_join_parent_platform
        )

        select *
        from final