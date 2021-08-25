import enum


class ControllerQueries(enum.Enum):
    # A view that the users (GUI) can query on
    CREATE_VIEW = (
        "create view sales_report as "
        "select sales.saleID, sales.salesDate, offices.city as office, salesmen.name as salesman, "
        "saleslineitem.quantity, products.productName, "
        "products.price as productPrice "
        "from sales "
        "join salesmen on sales.salesmanID = salesmen.salesmanID "
        "join offices on salesmen.officeID = offices.officeID "
        "join saleslineitem on sales.saleID = saleslineitem.saleID "
        "join products on saleslineitem.productID = products.productID"
    )

    # Default query, if no or wrongs parameters are set.
    DEFAULT_VIEW = (
        "SELECT row_number() over (order by salesDate) as 'rowID', salesDate, office, salesman, quantity, productname, "
        "productPrice \n"
        "FROM sales_report \n"
    )

    # total quantity and total sales value per office or salesman.
    YEAR_OFFICE = (
        "SELECT row_number() over (order by salesDate) as 'rowID', year(salesDate) as 'year', office, "
        "sum(quantity) as '# of products', format(sum(quantity * productPrice),0) as 'Total price' \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by year(salesDate), sales_report.office \n"
    )
    YEAR_SALESMAN = (
        "SELECT row_number() over (order by salesDate) as 'rowID', year(salesDate) as 'year', office, salesman, "
        "sum(quantity) as '# of products', format(sum(quantity * productPrice),0) as 'Total price' \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by year(salesDate), sales_report.salesman \n"
    )
    MONTH_OFFICE = (
        "SELECT row_number() over (order by salesDate) as 'rowID', monthname(salesDate) as 'month', office, "
        "sum(quantity) as '# of products', format(sum(quantity * productPrice),0) as 'Total price' \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by monthname(salesDate), sales_report.office \n"
    )
    MONTH_SALESMAN = (
        "SELECT row_number() over (order by salesDate) as 'rowID', monthname(salesDate) as 'month', office, salesman, "
        "sum(quantity) as '# of products', format(sum(quantity * productPrice),0) as 'Total price' \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by monthname(salesDate), sales_report.salesman \n"
    )
    DAY_OFFICE = (
        "SELECT row_number() over (order by salesDate) as 'rowID', salesDate, office, "
        "sum(quantity) as '# of products', format(sum(quantity * productPrice),0) as 'Total price' \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by salesDate, sales_report.office \n"
    )
    DAY_SALESMAN = (
        "SELECT row_number() over (order by salesDate) as 'rowID', salesDate, office, salesman, "
        "sum(quantity) as '# of products', format(sum(quantity * productPrice),0) as 'Total price' \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by salesDate, sales_report.salesman \n"
    )

    # Average quantity and sales value per office. Combine head, inner and tail to make a query
    OUTER_AVG_YEAR_OFFICE_HEAD = (
        "SELECT row_number() over (order by salesDate) as 'rowID', year(salesDate) as 'year', office, "
        "format((avg(tot_quantity)),1) as avg_quantity, format((avg(totalprice)),0) as avg_value \n"
        "FROM (\n"
    )

    OUTER_AVG_MONTH_OFFICE_HEAD = (
        "SELECT row_number() over (order by salesDate) as 'rowID', monthname(salesDate) as 'month', office, "
        "format((avg(tot_quantity)),1) as avg_quantity, format((avg(totalprice)),0) as avg_value \n"
        "FROM (\n"
    )

    OUTER_AVG_DAY_OFFICE_HEAD = (
        "SELECT row_number() over (order by salesDate) as 'rowID', salesDate, office, "
        "format((avg(tot_quantity)),1) as avg_quantity, format((avg(totalprice)),0) as avg_value \n"
        "FROM (\n"
    )

    INNER_AVG_OFFICE = (
        "SELECT saleID, salesDate, office, sum(quantity) as tot_quantity, "
        "sum(quantity * productPrice) as totalprice \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by saleID, office \n"
    )
    OUTER_PRODUCT_HEAD = (
        "SELECT products.productName, sum(saleslineitem.quantity) as tot_quantity, "
        "sum(products.price * quantity) as 'Total price' \n"
        "from (\n"
    )

    INNER_PRODUCT = (
        "SELECT sales.saleID, sales.salesDate \n"
        "from sales \n"
        )

    OUTER_PRODUCT_TAIL = (
        ") as sub \n"
        "join saleslineitem on sub.saleID = saleslineitem.saleID \n"
        "join products on saleslineitem.productID = products.productID \n"
        "group by products.productName \n"
    )

    OUTER_TOPCLIENTS_HEAD = (
        "select clients.name as Company, group_concat(clientreferences.referenceName) as Contacts, "
        "sum(sub.quantity) as tot_quantity, sum(sub.totalprice) as tot_price \n"
        "from (\n"
    )

    INNER_TOPCLIENTS = (
        "select sales.referenceID, sum(saleslineitem.quantity) as quantity, "
        "sum(saleslineitem.quantity * products.price) as totalprice \n"
        "from sales \n" 
        "join saleslineitem on sales.saleID = saleslineitem.saleID \n"
        "join products on saleslineitem.productID = products.productID \n"
        "group by sales.referenceID \n"
    )
    OUTER_TOPCLIENTS_TAIL = (
        ") as sub \n"
        "join clientreferences on sub.referenceID = clientreferences.referenceID \n"
        "join clients on clientreferences.clientID = clients.clientID \n"
        "group by clients.name \n"
        "order by tot_price desc \n"
    )

    OUTER_AVG_YEAR_OFFICE_TAIL = (
        ") as sub \n"
        "group by year(salesDate), office \n"
    )

    OUTER_AVG_MONTH_OFFICE_TAIL = (
        ") as sub \n"
        "group by monthname(salesDate), office \n"
    )

    OUTER_AVG_DAY_OFFICE_TAIL = (
        ") as sub \n"
        "group by salesDate, office \n"
    )

    # Average quantity and sales value per salesman. Combine head, inner and tail to make a query
    OUTER_AVG_YEAR_SALESMAN_HEAD = (
        "SELECT row_number() over (order by salesDate) as 'rowID', year(salesDate) as 'year', salesman, "
        "format((avg(tot_quantity)),1) as avg_quantity, format((avg(totalprice)),0) as avg_value \n"
        "FROM (\n"
    )

    OUTER_AVG_MONTH_SALESMAN_HEAD = (
        "SELECT row_number() over (order by salesDate) as 'rowID', monthname(salesDate) as 'month', salesman, "
        "format((avg(tot_quantity)),1) as avg_quantity, format((avg(totalprice)),0) as avg_value \n"
        "FROM (\n"
    )

    OUTER_AVG_DAY_SALESMAN_HEAD = (
        "SELECT row_number() over (order by salesDate) as 'rowID', salesDate, salesman, "
        "format((avg(tot_quantity)),1) as avg_quantity, format((avg(totalprice)),0) as avg_value \n"
        "FROM (\n"
    )

    INNER_AVG_SALESMAN = (
        "SELECT saleID, salesDate, salesman, sum(quantity) as tot_quantity, "
        "sum(quantity * productPrice) as totalprice \n"
        "FROM sf222vs_sales.sales_report \n"
        "group by saleID, salesman \n"
    )

    OUTER_AVG_YEAR_SALESMAN_TAIL = (
        ") as sub \n"
        "group by year(salesDate), salesman \n"
    )

    OUTER_AVG_MONTH_SALESMAN_TAIL = (
        ") as sub \n"
        "group by monthname(salesDate), salesman \n"
    )

    OUTER_AVG_DAY_SALESMAN_TAIL = (
        ") as sub \n"
        "group by salesDate, salesman \n"
    )
