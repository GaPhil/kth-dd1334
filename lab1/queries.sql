-- use booktown db instead of personal one to avoid accidentaly modifying db
\c booktown

--Task 1

--1.
SELECT last_name, first_name
FROM authors
WHERE author_id = (
	SELECT author_id
	FROM books
	WHERE title = 'The Shining'
);

--2.
SELECT title
FROM books
WHERE author_id = (
	SELECT author_id
	FROM authors
	WHERE first_name = 'Paulette' AND last_name =  'Bourgeois'
);

--3.

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
WHERE subject = 'Horror'

--customer -> shipments -> edition -> books -> subject
