

with
base as (
    select distinct
        id as tag_id,
        name as tag_name,
        slug as tag_slug,
        game_id
    from `video-game-analysis-418605`.`source`.`external_tags`
    where 1=1
    and language = 'eng'
),

add_unique_key as (
    select
        *,
        to_hex(md5(cast(coalesce(cast(game_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(tag_id as string), '_dbt_utils_surrogate_key_null_') as string))) as game_tag_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final