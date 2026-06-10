SELECT
	DISTINCT order_id,
	customer_id,
	amount,
	LOWER(status) AS status,
	order_date
from {{ ref('data1') }}