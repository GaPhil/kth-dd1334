\echo *** Task 2 *** \echo
---> NEW TASK <---

\echo *** Task 2.1 *** \echo

CREATE VIEW isbn_and_title AS
SELECT isbn, title
FROM editions, books
WHERE editions.book_id = books.book_id;

DROP VIEW isbn_and_title;
