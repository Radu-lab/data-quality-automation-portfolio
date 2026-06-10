with daily as (
    select
        sum(dist_flown_km) as flown,
        sum(dist_direct_km) as direct,
        sum(dist_achieved_km) as achieved
    from {{ ref('stg_flight_data2026') }}
),
monthly as (
    select
        sum(total_flown) as flown,
        sum(total_direct) as direct,
        sum(total_achieved) as achieved
    from {{ ref('monthly_results') }}
)
select *
from daily, monthly
where daily.flown != monthly.flown
   or abs(daily.direct - monthly.direct) > 0.01
   or abs(daily.achieved - monthly.achieved) > 0.01