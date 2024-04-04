

with
base as (
    select distinct
        platform_id as parent_platform_id,
        platform_name as parent_platform_name,
        platform_slug as parent_platform_slug,
        game_id
    from `video-game-analysis-418605`.`source`.`external_parent_platforms`
),

add_unique_key as (
    select
        *,
        to_hex(md5(cast(coalesce(cast(game_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(parent_platform_id as string), '_dbt_utils_surrogate_key_null_') as string))) as game_parent_platform_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final