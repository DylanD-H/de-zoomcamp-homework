{{
    config(
        materialized='view'
    )
}}

with 
source as (
    select * from {{ source('staging', 'external_fhv_tripdata') }}
    WHERE dispatching_base_num is not null
)

select
    dispatching_base_num,
    pickup_datetime,
    dropoff_datetime,
    pulocationid,
    dolocationid,
    sr_flag,
    affiliated_base_number

from source
