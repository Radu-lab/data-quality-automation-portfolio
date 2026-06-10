select *
from {{ source('raw', 'consumer') }}