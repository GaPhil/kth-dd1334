#!/usr/bin/python
import pgdb
from sys import argv


class DBContext:
    """DBContext is a small interface to a database that simplifies SQL.
    Each function gathers the minimal amount of information required and executes the query."""

    def __init__(self):  # PG-connection setup
        print("AUTHORS NOTE: If you submit faulty information here, I am not responsible for the consequences.")

        print "The idea is that you, the authorized database user, log in."
        print "Then the interface is available to employees whos should only be able to enter shipments as they are made."
        params = {'host': 'nestor2.csc.kth.se', 'user': raw_input("Username: "), 'database': '',
                  'password': raw_input("Password: ")}
        self.conn = pgdb.connect(**params)
        self.menu = ["Record a shipment", "Show stock", "Show shipments", "Exit"]
        self.cur = self.conn.cursor()

    def print_menu(self):
        """Prints a menu of all functions this program offers.  Returns the numerical correspondant of the choice made."""
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
                print("That was not a number, genious.... :(")

    def makeShipments(self):

        # get input from user and check for types and escape removal
        try:
            customer_id = int(input("customer ID: "))
            shipment_id = int(input("shipment ID: "))
            isbn = pgdb.escape_string((raw_input("isbn: ").strip()))
            ship_date = pgdb.escape_string(raw_input("Ship date: ").strip())
        except (NameError, ValueError, TypeError, SyntaxError):
            print "Please enter correct type!"
            return

        query = "SELECT stock FROM stock WHERE isbn='%s'" % isbn
        print query

        # start transaction
        try:

            # YOU NEED TO Catch exceptions ie bad queries
            try:
                self.cur.execute(query)
            except (pgdb.DatabaseError, pgdb.OperationalError):
                print("Bad query!")
                return

            result = self.cur.fetchone()
            if not result:
                print("No books found with isbn '%s'" % isbn)
                return

            # check if books are in stock
            cnt = result[0]
            if cnt < 1:
                print("No more books in stock :(")
                return
            else:
                print "WE have the book in stock"

            query = """UPDATE stock SET stock=stock-1 WHERE isbn='%s';""" % isbn
            print query

            self.cur.execute(query)  # execute decrease stock

            print "stock decremented"

            query = """INSERT INTO shipments VALUES (%i, %i, '%s','%s');""" % (
                shipment_id, customer_id, isbn, ship_date)
            print query

            try:
                self.cur.execute(query)  # execute insert
            except (pgdb.DatabaseError, pgdb.OperationalError):
                print "Failed on insert!"
                return

            print "shipment created"

            # This ends the transaction (and starts a new one)
            self.conn.commit()

        except (pgdb.DatabaseError, pgdb.OperationalError):
            print "  Exception encountered while modifying table!"
            self.conn.rollback()
            print "  Rolling back."
            return

    def showStock(self):
        query = """SELECT * FROM stock;"""
        print query
        try:
            self.cur.execute(query)
        except (pgdb.DatabaseError, pgdb.OperationalError):
            print "  Exception encountered while modifying table data."
            self.conn.rollback()
            return
        self.print_answer()

    def showShipments(self):
        query = """SELECT * FROM shipments;"""
        print query
        try:
            self.cur.execute(query)
        except (pgdb.DatabaseError, pgdb.OperationalError):
            print "  Exception encountered while modifying table data."
            self.conn.rollback()
            return
        self.print_answer()

    def exit(self):
        self.cur.close()
        self.conn.close()
        exit()

    def print_answer(self):
        print("\n".join([", ".join([str(a) for a in x]) for x in self.cur.fetchall()]))

    # we call this below in the main function.
    def run(self):
        """Main loop.
        Will divert control through the DBContext as dictated by the user."""
        actions = [self.makeShipments, self.showStock, self.showShipments, self.exit]
        while True:
            try:
                actions[self.print_menu() - 1]()
            except IndexError:
                print("Bad choice")
                continue


if __name__ == "__main__":
    db = DBContext()
    db.run()
