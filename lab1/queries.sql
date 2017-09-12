-- use booktown db instead of personal one to avoid accidentaly modifying db
\c booktown \echo

\echo *** Task 1 *** \echo
---> NEW TASK <---

\echo *** Task 1.1 *** \echo

SELECT
  last_name,
  first_name
FROM authors
WHERE author_id = (
  SELECT author_id
  FROM books
  WHERE title = 'The Shining'
);

\echo *** Task 1.2 *** \echo

SELECT title
FROM books
WHERE author_id = (
  SELECT author_id
  FROM authors
  WHERE first_name = 'Paulette' AND last_name = 'Bourgeois'
);

\echo *** Task 1.3 *** \echo
-- avoid inner join, since it returns duplicate attributes

SELECT
  last_name,
  first_name
FROM customers
  INNER JOIN shipments
    ON customers.customer_id = shipments.customer_id
  INNER JOIN editions
    ON shipments.isbn = editions.isbn
  INNER JOIN books
    ON editions.book_id = books.book_id
  INNER JOIN subjects
    ON books.subject_id = subjects.subject_id
WHERE subject = 'Horror';

\echo *** Task 1.4 *** \echo

SELECT title
FROM books
  NATURAL JOIN editions
  NATURAL JOIN stock
WHERE stock = (
  SELECT max(stock)
  FROM stock
);

\echo *** Task 1.5 *** \echo

SELECT SUM(retail_price)
FROM stock
  INNER JOIN editions
    ON stock.isbn = editions.isbn
  INNER JOIN books
    ON editions.book_id = books.book_id
  INNER JOIN subjects
    ON books.subject_id = subjects.subject_id
WHERE subject = 'Science Fiction';

\echo *** Task 1.6 *** \echo

SELECT title
FROM books
  INNER JOIN editions
    ON books.book_id = editions.book_id
  INNER JOIN shipments
    ON editions.isbn = shipments.isbn
GROUP BY books.title
HAVING COUNT(customer_id) = 2;

\echo *** Task 1.7 *** \echo
--> TODO <--

\echo *** Task 1.8 *** \echo
-- total money earnt is profit made on each shipment

SELECT SUM(retail_price - cost)
FROM shipments, stock
WHERE shipments.isbn = stock.isbn;

\echo *** Task 1.9 *** \echo

SELECT
  last_name,
  first_name
FROM customers, shipments, editions, books, subjects
WHERE (customers.customer_id = shipments.customer_id
       AND shipments.isbn = editions.isbn
       AND editions.book_id = books.book_id
       AND books.subject_id = subjects.subject_id
)
GROUP BY customers.last_name, customers.first_name
HAVING COUNT(subjects.subject_id) > 2;

\echo *** Task 1.10 *** \echo
-- find all sold subjects and subtract from all possible subjects

SELECT a.subject
FROM (SELECT subject
      FROM subjects
     ) AS a
WHERE subject NOT IN (
  SELECT DISTINCT subject
  FROM shipments, editions, books, subjects
  WHERE (shipments.isbn = editions.isbn
         AND editions.book_id = books.book_id
         AND books.subject_id = subjects.subject_id
  )
);
