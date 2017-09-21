#!/usr/bin/python
import pgdb


class DBContext:
    """DBContext is a small interface to a database that simplifies SQL.
    Each function gathers the minimal amount of information required and executes the query."""

    def __init__(self):  # PG-connection setup
        print("AUTHORS NOTE: If you submit faulty information here, I am not responsible for the consequences.")

        print "The idea is that you, the authorized database user, log in."
        print "Then the interface is available to customers whos should only be able to see their own shipments."
        params = {'host': 'nestor2.csc.kth.se', 'user': raw_input("Username: "), 'database': '',
                  'password': raw_input("Password: ")}
        self.conn = pgdb.connect(**params)
        self.menu = ["Shipments Status", "Exit"]
        self.cur = self.conn.cursor()

    def print_menu(self):
        """Prints a menu of all functions this program offers.Returns the numerical correspondent of the choice made."""
        for i, x in enumerate(self.menu):
            print("%i. %s" % (i + 1, x))
        return self.get_int()

    def get_int(self):
        """Retrieves an integer from the user.
        If the user fails to submit an integer, it will reprompt until an integer is submitted."""
        while True:
            try:
                choice = int(input("Choose: "))
                if 1 <= choice <= len(self.menu):
                    return choice
                print("Invalid choice.")
            except (NameError, ValueError, TypeError, SyntaxError):
                print("That was not a number, genius.... :(")

    def shipments(self):
        try:
            customer_id = int(raw_input("customerID: "))  # check int is taken in
        except (NameError, ValueError, TypeError, SyntaxError):
            print("That was not a number...")
            return

        # Protect against SQL injection attacks to remove escape characters
        fname = pgdb.escape_string(raw_input("First Name: ").strip())  # remove escape characters such as ' or \
        lname = pgdb.escape_string(raw_input("Last Name: ").strip())  # remove escape characters such as ' or \

        query = "SELECT first_name, last_name FROM customers WHERE customer_id = %s;" % customer_id

        try:
            print "The database is being checked: " + query
            self.cur.execute(query)  # find first name and last name given customer_id
        except (NameError, ValueError, TypeError, SyntaxError):
            print("Query execution failed!")
            return

        # retrieves the results of the query in the format `Row(first_name='Chad', last_name='Allen')`
        result_list = self.cur.fetchone()
        if result_list is None:
            print "Customer ID does not exist."
            return
        else:
            if result_list[0] == fname and result_list[1] == lname:
                print "Name and ID match - OK!"
            else:
                print "Name does not match ID!"
                return

        query = """ SELECT shipment_id, ship_date, shipments.isbn, title 
                      FROM shipments
                        JOIN editions
                          ON shipments.isbn = editions.isbn
                        JOIN books
                          ON editions.book_id = books.book_id
                      WHERE customer_id = %s; """ % customer_id

        try:
            self.cur.execute(query)  # extract shipment_id, ship_date, shipments.isbn, title given customer_id
            print "Customer: %d %s %s:" % (customer_id, fname, lname)
            print "shipment_id,ship_date,isbn,title"
            self.print_answer()
        except (NameError, ValueError, TypeError, SyntaxError):
            print("Execution failed!")
            return

    def exit(self):
        self.cur.close()
        self.conn.close()
        exit()

    def print_answer(self):
        print("\n".join([", ".join([str(a) for a in x]) for x in self.cur.fetchall()]))

    def run(self):
        """Main loop.
        Will divert control through the DBContext as dictated by the user."""
        actions = [self.shipments, self.exit]
        while True:
            try:
                actions[self.print_menu() - 1]()
            except IndexError:
                print("Bad choice")
                continue


if __name__ == "__main__":
    db = DBContext()
    db.run()
