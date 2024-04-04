

with
base as (
    select distinct
        store_id,
        store_name,
        store_slug,
        game_id
    from `video-game-analysis-418605`.`source`.`external_stores`
),

add_unique_key as (
    select
        *,
        to_hex(md5(cast(coalesce(cast(game_id as string), '_dbt_utils_surrogate_key_null_') || '-' || coalesce(cast(store_id as string), '_dbt_utils_surrogate_key_null_') as string))) as game_store_id
    from base
),

final as (
    select *
    from add_unique_key
)

select *
from final