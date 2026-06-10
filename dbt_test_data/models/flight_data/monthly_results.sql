select
    entity_name,
    type_model,
    month_num,
    sum(dist_flown_km) as total_flown,
    sum(dist_direct_km) as total_direct,
    sum(dist_achieved_km) as total_achieved
from {{ ref('stg_flight_data2026') }}
group by entity_name, type_model, month_num
order by entity_name asc