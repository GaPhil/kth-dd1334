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
