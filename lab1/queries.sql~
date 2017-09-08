-- use booktown db instead of personal one to avoid accidentaly modifying db
\c booktown \echo

\echo *** Task 1 *** \echo
---> NEW TASK <---

\echo *** Task 1.1 *** \echo

SELECT last_name, first_name
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
	WHERE first_name = 'Paulette' AND last_name =  'Bourgeois'
);

\echo *** Task 1.3 *** \echo
-- avoid inner join, since it returns duplicate attributes

SELECT last_name, first_name
FROM customers
INNER JOIN shipments
	ON customers.customer_id=shipments.customer_id
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

