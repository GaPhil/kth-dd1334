\echo *** Task 3 *** \echo
---> NEW TASK <---

DROP FUNCTION decstock() CASCADE;

CREATE FUNCTION decstock()
  RETURNS TRIGGER AS $pname$
BEGIN
  IF (SELECT NEW.isbn
      FROM stock
     ) IS NULL
    THEN RAISE EXCEPTION 'There is no stock to ship';
  ELSE -- do insert and update stock
    -- selects most recently added shipment and reduces that isbn's stock
    UPDATE stock
    SET stock = stock - 1
    WHERE stock.isbn = (
      SELECT isbn
      FROM shipments
      ORDER BY ship_date DESC
      LIMIT 1
    );
  END IF;
  RETURN NEW;
END;

$pname$ LANGUAGE plpgsql;

CREATE TRIGGER reduce_stock
AFTER INSERT ON shipments
FOR EACH ROW
EXECUTE PROCEDURE decstock();

-- Output: the whole table before making shipments.
SELECT *
FROM stock;

INSERT INTO shipments
VALUES (2000, 860, '0394900014', '2012-12-07');

-- DROP FUNCTION decstock() CASCADE;

