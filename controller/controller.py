from controller_queries import ControllerQueries
from model.salesDatabase import SalesDatabase
from view.view import View


class Controller:

    def __init__(self):
        self.db = SalesDatabase()
        self.view = View(self)
        self.view_cursor = self.db.get_cursor()
        self.view_query = ControllerQueries.DEFAULT_VIEW.value
        self.order_by = " "

    def main(self):
        self.__create_view()
        self.view.main()

    def update_view(self):
        print("\n{}".format(self.view_query))
        self.view_cursor = self.db.get_data(self.view_query)

    def get_view_rows(self):
        return self.view_cursor.fetchall()

    def get_view_column_names(self):
        return self.view_cursor.column_names

    def __create_view(self):
        self.db.create_table(ControllerQueries.CREATE_VIEW.value)

    def set_query_date(self, date_start, date_end):
        if date_start <= date_end:
            if date_start == date_end:
                new_line = "where salesdate='{}'".format(date_start)
            else:
                new_line = "where salesdate>='{}' and salesdate<='{}'".format(date_start, date_end)
            lines = self.view_query.split("\n")
            new_view_query = ""
            found_line = False
            for line in lines:
                if line.lower().startswith("where salesdate", 0, 15):
                    found_line = True
                    new_view_query += "{} \n".format(new_line)
                elif not found_line and line.lower().startswith("group by", 0, 8):
                    found_line = True
                    new_view_query += "{} \n".format(new_line)
                    new_view_query += "{} \n".format(line)
                else:
                    if line != "":
                        new_view_query += "{} \n".format(line)
            if found_line:
                self.view_query = new_view_query
            else:
                self.view_query += new_line

    # sets a new query. Option = [TotalPrice/Average][period][office/salesman]
    def set_query(self, option):
        if option == 111:
            self.view_query = ControllerQueries.YEAR_OFFICE.value
        elif option == 121:
            self.view_query = ControllerQueries.MONTH_OFFICE.value
        elif option == 131:
            self.view_query = ControllerQueries.DAY_OFFICE.value
        elif option == 112:
            self.view_query = ControllerQueries.YEAR_SALESMAN.value
        elif option == 122:
            self.view_query = ControllerQueries.MONTH_SALESMAN.value
        elif option == 132:
            self.view_query = ControllerQueries.DAY_SALESMAN.value
        elif option == 103:
            self.view_query = ControllerQueries.INNER_PRODUCT.value
        elif option == 104:
            self.view_query = ControllerQueries.INNER_TOPCLIENTS.value
        elif option // 100 == 2 and option % 10 == 1:  # Checks if option = 221, 221,231
            self.view_query = ControllerQueries.INNER_AVG_OFFICE.value
        elif option // 100 == 2 and option % 10 == 2:  # Checks if option = 222, 222,232
            self.view_query = ControllerQueries.INNER_AVG_SALESMAN.value

        else:
            # if the option code isn't implemented, also used for reset
            self.view_query = ControllerQueries.DEFAULT_VIEW.value

    # Wraps a subquery with a new query. Option = [period][office/salesman]
    def set_query_with_sub_query(self, option):
        if option == 11:
            new_query = ControllerQueries.OUTER_AVG_YEAR_OFFICE_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_AVG_YEAR_OFFICE_TAIL.value
        elif option == 21:
            new_query = ControllerQueries.OUTER_AVG_MONTH_OFFICE_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_AVG_MONTH_OFFICE_TAIL.value
        elif option == 31:
            new_query = ControllerQueries.OUTER_AVG_DAY_OFFICE_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_AVG_DAY_OFFICE_TAIL.value
        elif option == 12:
            new_query = ControllerQueries.OUTER_AVG_YEAR_SALESMAN_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_AVG_YEAR_SALESMAN_TAIL.value
        elif option == 3:
            new_query = ControllerQueries.OUTER_PRODUCT_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_PRODUCT_TAIL.value
        elif option == 4:
            new_query = ControllerQueries.OUTER_TOPCLIENTS_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_TOPCLIENTS_TAIL.value

        elif option == 22:
            new_query = ControllerQueries.OUTER_AVG_MONTH_SALESMAN_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_AVG_MONTH_SALESMAN_TAIL.value
        elif option == 32:
            new_query = ControllerQueries.OUTER_AVG_DAY_SALESMAN_HEAD.value
            new_query += self.view_query
            new_query += ControllerQueries.OUTER_AVG_DAY_SALESMAN_TAIL.value
        else:
            # if the option code isn't implemented
            print("Internal error: set_query_with_sub_query")
            new_query = ControllerQueries.DEFAULT_VIEW

        self.view_query = new_query

    # TODO: dosent work with avg columns
    # Code is not used by view, because of the problem with avg. columns.
    # Same problem in mysql, so it must be a query problem
    def set_order_by(self, column):
        asc_dec = 'ASC'
        if not self.order_by == " ":
            lines = self.order_by.split(" ")
            if lines[2] == column:
                if lines[3] == 'ASC':
                    asc_dec = 'DESC'

        self.order_by = "ORDER BY {} {}".format(column, asc_dec)

        is_ordered_by = False
        new_query = ""
        query_lines = self.view_query.split("\n")
        for query_line in query_lines:
            if query_line.lower().startswith("order"):
                is_ordered_by = True
                new_query += "{} \n".format(self.order_by)
            else:
                if query_line != "":
                    new_query += "{} \n".format(query_line)

        if is_ordered_by:
            self.view_query = new_query
        else:
            self.view_query += self.order_by


if __name__ == '__main__':
    leaderboard = Controller()
    leaderboard.main()
