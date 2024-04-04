

with
base as (
    select distinct
        game_id,
        slug as game_slug,
        name as game_name
    from `video-game-analysis-418605`.`source`.`external_games`
),

final as (
    select *
    from base
)

select *
from final