\echo *** Task 2 *** \echo
---> NEW TASK <---

\echo *** Task 2.1 *** \echo

CREATE VIEW isbn_and_title AS
SELECT isbn, title
FROM editions, books
WHERE editions.book_id = books.book_id;

DROP VIEW isbn_and_title;

\echo *** Task 2.2 *** \echo

-- INSERT INTO editions(isbn, book_id, edition, publisher_id, publication_date)
-- VALUES ('5555', 12345, 1, 59, '2012-12-02');
\echo ERROR:  insert or update on table "editions" violates foreign key constraint "editions_book_id_fkey"
\echo DETAIL:  Key (book_id)=(12345) is not present in table "books".

\echo *** Task 2.3 *** \echo

--INSERT INTO editions(isbn)
--VALUES ('5555');
\echo ERROR:  new row for relation "editions" violates check constraint "integrity"
\echo DETAIL:  Failing row contains (5555, null, null, null, null).

\echo *** Task 2.4 *** \echo
-- no need for author or subject, since author_id and subject_id are foreign keys in books

INSERT INTO books(book_id, title)
VALUES (12345, 'How I Insert');
INSERT INTO editions(isbn, book_id, edition, publisher_id, publication_date)
VALUES ('5555', 12345, 1, 59, '2012-12-02');
SELECT * FROM books;
