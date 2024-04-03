select *
from {{ ref("fact_release_by_yyyymm") }}
where 1=1
and metacritic is not null