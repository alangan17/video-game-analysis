

with
base as (
    select distinct
        id as genre_id,
        name as genre_name,
        slug as genre_slug,
        game_id
    from `video-game-analysis-418605`.`source`.`external_genres`
),

add_unique_key as (
    select
        *,
        to_hex(md5(cast(coalesce(cast(game_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(genre_id as string), '_dbt_utils_surrogate_key_null_') as string))) as game_genre_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final