CREATE TRIGGER reduce_stock
ON shipment
AFTER INSERT

-- selects most recently added shipment and reduces that isbn's stock

UPDATE stock
SET stock = stock - 1
WHERE stock.isbn = (
	SELECT isbn
	FROM shipments
	ORDER BY ship_date DESC
	LIMIT 1
	);

SELECT COUNT(stock)
FROM stock;
