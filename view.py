import tkinter as tk
from datetime import datetime
from tkinter import *
from tkinter import ttk
from tkcalendar import *


class View(tk.Tk):
    PAD = 10
    # TODO set the with as weight of total width
    column_width = {'rowID': 40, 'saleID': 40, 'year': 40, 'month': 70, 'salesDate': 75, 'office': 70, 'salesman': 120,
                    'quantity': 55, 'tot_quantity': 85, 'avg_quantity': 85, '# of products': 85, 'productName': 100,
                    'productPrice': 85, 'Total price': 85, 'avg_value': 85, 'Company': 85, 'Contacts': 85,
                    'tot_price': 85
                    }
    column_anchor = {'rowID': 'center', 'saleID': 'center', 'year': 'center', 'month': 'center', 'salesDate': 'center',
                     'office': 'w', 'salesman': 'w', 'quantity': 'center', 'tot_quantity': 'center',
                     'avg_quantity': 'center', '# of products': 'center', 'productName': 'w', 'productPrice': 'e',
                     'Total price': 'e', 'avg_value': 'e', 'Company': 'w', 'Contacts': 'w', 'tot_price': 'e'
                     }

    def __init__(self, controller):
        super().__init__()
        self.ctrl = controller
        self.value_var = tk.StringVar()
        self.window_height = 700
        self.window_width = 650

    def main(self):
        self._root_frame_config()
        self._make_title()
        self._make_calender_box()
        self._make_radio_buttons_period()
        self._make_treeview()
        self.update_treeview()
        self.mainloop()

    def _root_frame_config(self):
        self.title("Sales")
        self.geometry("{}x{}".format(self.window_width, self.window_height))
        self.root = ttk.Frame(self)
        self.root.pack(padx=30)

    def _make_title(self):
        title_lable = Label(self.root, text="Sales", font=("Times", "24", "bold roman"))
        title_lable.pack()

    def _make_calender_box(self):
        calendar_frame = Frame(self.root)
        calendar_frame.pack(pady=15)
        now = datetime.now()
        self.cal_start = Calendar(calendar_frame, selectmode="day", year=2020, month=1, day=1,
                                  date_pattern='y-mm-dd')
        self.cal_end = Calendar(calendar_frame, selectmode="day", year=now.year, month=now.month, day=now.day,
                                date_pattern='y-mm-dd')
        self.cal_start.bind('<<CalendarSelected>>',
                            lambda event: self._on_selection_update_query(0))
        self.cal_end.bind('<<CalendarSelected>>',
                          lambda event: self._on_selection_update_query(0))

        self.cal_start.grid(row=1, column=0, padx=10)
        self.cal_end.grid(row=1, column=1, padx=10)

    def _make_treeview(self):
        tree_frame = Frame(self.root)
        tree_frame.pack(pady=10, fill="both", expand=1)

        # Treeview Scrollbar
        tree_scroll = Scrollbar(tree_frame)
        tree_scroll.pack(side=RIGHT, fill=Y)

        self.tree = ttk.Treeview(tree_frame, yscrollcommand=tree_scroll.set)

        # Configure the scrollbar
        tree_scroll.config(command=self.tree.yview)

        # Style (required for stripped rows too
        style_tree = ttk.Style()
        # style_tree.theme_use("clam")
        style_tree.configure("Treeview", background="white", foreground="black", rowheight=25,
                             fieldbackground="#d3d3d3")
        style_tree.map('Treeview', background=[('selected', 'blue')])

        # Create stripped row tags
        self.tree.tag_configure('odd', background="white")
        self.tree.tag_configure('even', background="#9b7dff")
        self.tree.pack(fill="both", expand=YES)

    def update_treeview(self):
        # Clear tree
        for row in self.tree.get_children():
            self.tree.delete(row)

        # Update data from controller (mySql)
        self.ctrl.update_view()

        # Define columns
        columns = self.ctrl.get_view_column_names()
        self.tree['columns'] = columns

        # Format columns & create headings
        self.tree.column("#0", width=0, stretch=NO)
        self.tree.heading("#0", text="")
        for column in columns:
            self.tree.column(column, width=self.column_width.get(column), anchor=self.column_anchor.get(column),
                             stretch=YES)
            self.tree.heading(column, text=column, command=lambda col=column: self._on_selection_update_treeview(col))

        # Add data
        rows = self.ctrl.get_view_rows()
        count = 0
        for row in rows:
            if count % 2 == 0:
                self.tree.insert(parent='', index='end', iid=count, text=columns, values=row, tags=('even',))
            else:
                self.tree.insert(parent='', index='end', iid=count, text=columns, values=row, tags=('odd',))
            count += 1

    def _on_selection_update_treeview(self, column):
        pass
        # TODO: Dosent work with average, avg
        # self.ctrl.set_order_by(column)
        # self.update_treeview()

    def _make_radio_buttons_period(self):
        # Period radio buttons on period frame
        radiobutton_frame = LabelFrame(self.root, text="filters")
        radiobutton_frame.pack(pady=5)
        self.reset = IntVar()
        self.reset.set(1)
        self.period = IntVar()
        self.office_salesman = IntVar()
        self.total_average = IntVar()

        Radiobutton(radiobutton_frame, text="year", variable=self.period, value=1,
                    command=lambda: self._on_selection_update_query(1)
                    ).grid(row=0, column=0)
        Radiobutton(radiobutton_frame, text="month", variable=self.period, value=2,
                    command=lambda: self._on_selection_update_query(1)
                    ).grid(row=0, column=1)
        Radiobutton(radiobutton_frame, text="day", variable=self.period, value=3,
                    command=lambda: self._on_selection_update_query(1)
                    ).grid(row=0, column=2)

        Radiobutton(radiobutton_frame, text="office", variable=self.office_salesman, value=1,
                    command=lambda: self._on_selection_update_query(2)
                    ).grid(row=1, column=0)
        Radiobutton(radiobutton_frame, text="salesman", variable=self.office_salesman, value=2,
                    command=lambda: self._on_selection_update_query(2)
                    ).grid(row=1, column=1)
        Radiobutton(radiobutton_frame, text="products", variable=self.office_salesman, value=3,
                    command=lambda: self._on_selection_update_query(5)
                    ).grid(row=1, column=2)
        Radiobutton(radiobutton_frame, text="Top clients", variable=self.office_salesman, value=4,
                    command=lambda: self._on_selection_update_query(5)
                    ).grid(row=1, column=3)
        Radiobutton(radiobutton_frame, text="total price", variable=self.total_average, value=1,
                    command=lambda: self._on_selection_update_query(3)
                    ).grid(row=2, column=0)
        Radiobutton(radiobutton_frame, text="average", variable=self.total_average, value=2,
                    command=lambda: self._on_selection_update_query(3)
                    ).grid(row=2, column=1)
        Radiobutton(radiobutton_frame, text="no filter", variable=self.reset, value=1,
                    command=lambda: self._on_selection_update_query(4)
                    ).grid(row=3, column=0)

    def _on_selection_update_query(self, trigger_row):
        # set 0 = off, set 1 = on
        if trigger_row == 4:
            self.period.set(0)
            self.office_salesman.set(0)
            self.total_average.set(0)
            self.reset.set(1)
            opcode = 0

        elif trigger_row == 5:
            self.reset.set(0)
            self.period.set(0)
            self.total_average.set(1)
            opcode = 100 * self.total_average.get() + 10 * self.period.get() + self.office_salesman.get()

        else:
            # if its not a reset and no options are picked, set defaults.
            self.reset.set(0)
            if self.period.get() == 0:
                self.period.set(1)
            if self.office_salesman.get() == 0 or self.office_salesman.get() == 3 or self.office_salesman.get() == 4:
                self.office_salesman.set(1)
            if self.total_average.get() == 0:
                self.total_average.set(1)

            opcode = 100 * self.total_average.get() + 10 * self.period.get() + self.office_salesman.get()

        # Set query
        self.ctrl.set_query(opcode)

        # add period to query,  WHERE ...
        self.ctrl.set_query_date(self.cal_start.get_date(), self.cal_end.get_date())

        # if query is a sub query, then wrap it
        if self.total_average.get() == 2 or opcode % 10 == 3 or opcode % 10 == 4:
            opcode = 10 * self.period.get() + self.office_salesman.get()
            self.ctrl.set_query_with_sub_query(opcode)

        self.update_treeview()
