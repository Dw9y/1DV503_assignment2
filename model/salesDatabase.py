import csv
from model.core_queries import MySQLParam
import mysql.connector
from mysql.connector import errorcode


class SalesDatabase:
    _cnx = mysql.connector.connect(user='root',
                                   password='root',
                                   host='127.0.0.1',
                                   # unix_socket= '/Applications/MAMP/tmp/mysql/mysql.sock',
                                   )

    # Name of database
    _db_name = 'sf222vs_sales'

    # Opens connection to mySQL
    _cursor = _cnx.cursor()

    def __init__(self):
        if not self.__db_exist():
            self.__create_database()
            self._cnx.database = self._db_name
            self.__insert_from_file("../model/fake_data/clients.csv",
                                    ";",
                                    MySQLParam.TABLE_CLIENTS,
                                    MySQLParam.INSERT_CLIENTS
                                    )
            self.__insert_from_file("../model/fake_data/client_references.csv", ",",
                                    MySQLParam.TABLE_CLIENTS_REFERENCES,
                                    MySQLParam.INSERT_CLIENTS_REFERENCES
                                    )
            self.__insert_from_file("../model/fake_data/offices.csv",
                                    ";",
                                    MySQLParam.TABLE_OFFICES,
                                    MySQLParam.INSERT_OFFICES)
            self.__insert_from_file("../model/fake_data/employees.csv",
                                    ";",
                                    MySQLParam.TABLE_SALESMEN, MySQLParam.INSERT_SALESMEN)
            self.__insert_from_file("../model/fake_data/products.csv", ";", MySQLParam.TABLE_PRODUCTS,
                                    MySQLParam.INSERT_PRODUCTS)
            self.__insert_from_file("../model/fake_data/order.csv", ",", MySQLParam.TABLE_SALES,
                                    MySQLParam.INSERT_SALES)
            self.__insert_from_file("../model/fake_data/order_line_item.csv", ";", MySQLParam.TABLE_SALES_LINE_ITEM,
                                    MySQLParam.INSERT_SALES_LINE_ITEM
                                    )
        else:
            print("Connected to database: {}".format(self._db_name))

    # Checks if database exists thru trying to use it.
    def __db_exist(self):
        try:
            self._cursor.execute("USE {}".format(self._db_name))
            return True
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_BAD_DB_ERROR:
                return False
            else:
                print(err)
                exit(1)

    # Creates a database
    def __create_database(self):
        try:
            self._cursor.execute("CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(self._db_name))
            print("Creating database: {}".format(self._db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)
        else:
            print("OK")

    # Creates a table
    def create_table(self, table):
        try:
            print("Creating table: {}".format(table.split()[2]))
            self._cursor.execute(table)
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    def __insert_from_file(self, filename, delimiter, table, insert):
        try:
            with open(filename, 'r', newline='', encoding='utf-8') as csv_file:
                csv_data = csv.reader(csv_file, skipinitialspace=True, delimiter=delimiter)
                next(csv_data, None)  # Skips first row so headers doesn't get uploaded as data
                self.create_table(table.value)
                for row in csv_data:
                    self._cursor.execute(insert.value, row)

        except OSError as e:
            print("{} : {}".format(filename, e.args[-1]))
            self._cursor.execute("DROP DATABASE {}".format(self._db_name))  # Drops faulty database
            exit(1)

        self._cnx.commit()  # commit changes to database

    # takes a mySQL query and returns the data
    def get_data(self, query):
        self._cursor.execute(query)
        return self._cursor

    def get_cursor(self):
        return self._cursor
