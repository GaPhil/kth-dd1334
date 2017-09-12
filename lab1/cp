\echo *** Task 3 *** \echo
---> NEW TASK <---

DROP FUNCTION decstock() CASCADE;

CREATE FUNCTION decstock()
  RETURNS TRIGGER AS $pname$
BEGIN
  IF (SELECT stock
      FROM stock
      WHERE stock.isbn = NEW.isbn) <= 0
  THEN
    RAISE EXCEPTION 'There is no stock to ship!';
  ELSE
    UPDATE stock
    SET stock = stock - 1
    WHERE stock.isbn = new.isbn;
  END IF;
  RETURN NEW;
END;

$pname$ LANGUAGE plpgsql;

CREATE TRIGGER reduce_stock
AFTER INSERT ON shipments
FOR EACH ROW
EXECUTE PROCEDURE decstock();

\echo *** PRINT OUT CONTENT OF STOCK *** \echo

SELECT *
FROM stock;

\echo *** ATTEMPT TO SHIP BOOK THAT IS NOT IN STOCK *** \echo

INSERT INTO shipments
VALUES(2000, 860, '0394900014', '2012-12-07');

\echo \echo *** SHIP BOOK THAT IS IN STOCK *** \echo

INSERT INTO shipments
VALUES(2001, 860, '044100590X', '2012-12-07');

\echo \echo *** SHOW THAT ON SECOND SHIPMENT WAS INSERTED *** \echo

SELECT * FROM shipments WHERE shipment_id > 1999;

\echo \echo *** PRINT OUT CONTENT OF STOCK *** \echo

SELECT * FROM stock;

\echo \echo *** RESTORE DATABASE TO ITS ORIGINAL STATE *** \echo
DELETE FROM shipments WHERE shipment_id > 1999;
UPDATE stock SET stock = 89 WHERE isbn = '044100590X';

DROP FUNCTION decstock() CASCADE;
