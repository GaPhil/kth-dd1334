#!/usr/bin/python
import pgdb
from sys import argv


#  Here you shall complete the code to allow a customer to use this interface to check his or her shipments.
#  You will fill in the 'shipments' function

#  The code should not allow the customer to find out other customers or other booktown data.
#  Security is taken as the customer knows his own customer_id, first and last names.  
#  So not really so great but it illustrates how one would check a password if there were the addition of encryption.

#  Most of the code is here except those little pieces needed to avoid injection attacks.  
#  You might want to read up on pgdb, postgresql, and this useful function: pgdb.escape_string(some text)

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
        # ID should be hard typed to an integer
        #  So think that they can enter: 1 OR 1=1
        try:
            customer_id = int(raw_input("customerID: "))
        except (NameError, ValueError, TypeError, SyntaxError):
            print("That was not a number...")
            return

        # These names inputs are terrible and allow injection attacks.
        # So think that they can enter: Hilbert' OR 'a'='a
        try:
            fname = pgdb.escape_string(raw_input("First Name: ").strip())
            lname = pgdb.escape_string(raw_input("Last Name: ").strip())
        except (NameError, ValueError, TypeError, SyntaxError):
            print("That was not a string...")
            return
        query = """  SELECT first_name, last_name FROM customers WHERE customer_id = %s;""" % customer_id

        try:
            print "The database is being checked:" + query
            self.cur.execute(query)  # find fname and lname from customer_id
        except (NameError, ValueError, TypeError, SyntaxError):
            print("Query execution failed!")
            return

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

        # THIS IS NOT RIGHT YOU MUST PRINT OUT a listing of shipment_id,ship_date,isbn,title for this customer

        query = """  SELECT shipment_id, ship_date, shipments.isbn, title 
                      FROM shipments
                        JOIN editions
                          ON shipments.isbn = editions.isbn
                        JOIN books
                          ON editions.book_id = books.book_id
                      WHERE customer_id = %s;""" % customer_id

        try:
            self.cur.execute(query)
            print "Customer: %d %s %s:" % (customer_id, fname, lname)
            print "shipment_id,ship_date,isbn,title"
            self.print_answer()
        except (NameError, ValueError, TypeError, SyntaxError):
            print("Execution failed!")
            return

        self.print_answer()

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
