
    
    

with dbt_test__target as (

  select game_tag_id as unique_field
  from `video-game-analysis-418605`.`vga`.`dim_tags`
  where game_tag_id is not null

)

select
    unique_field,
    count(*) as n_records

from dbt_test__target
group by unique_field
having count(*) > 1


