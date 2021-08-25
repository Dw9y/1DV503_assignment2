import enum


class MySQLParam(enum.Enum):
    TABLE_CLIENTS = (
        "CREATE TABLE clients ("
        "  `clientID` smallint NOT NULL AUTO_INCREMENT PRIMARY KEY ,"
        "  `name` varchar(37) NOT NULL"
        ") ENGINE=InnoDB;"
    )
    INSERT_CLIENTS = (
        "INSERT INTO clients (`clientID`,`name`) VALUES(%s,%s);"
    )
    TABLE_CLIENTS_REFERENCES = (
        "CREATE TABLE clientReferences ("
        "  `referenceID` smallint NOT NULL AUTO_INCREMENT PRIMARY KEY ,"
        "  `clientID` smallint NOT NULL ,"
        "  `referenceName` varchar(22) NOT NULL ,"
        "  CONSTRAINT `fk_clientReferences_client` FOREIGN KEY (clientID)"
        "  REFERENCES clients(clientID) ON UPDATE CASCADE ON DELETE RESTRICT"
        ") ENGINE=InnoDB;"
    )
    INSERT_CLIENTS_REFERENCES = (
        "INSERT INTO clientReferences (referenceID, clientID, referenceName) "
        " VALUES(%s,%s,%s);"
    )
    TABLE_OFFICES = (
        "CREATE TABLE offices ("
        "  `officeID` smallint NOT NULL AUTO_INCREMENT PRIMARY KEY ,"
        "  `city` varchar(9) NOT NULL "
        ") ENGINE=InnoDB;"
    )
    INSERT_OFFICES = (
        "INSERT INTO offices (officeID, city) "
        " VALUES(%s,%s);"
    )
    TABLE_SALESMEN = (
        "CREATE TABLE salesmen ("
        "  `salesmanID` smallint NOT NULL AUTO_INCREMENT PRIMARY KEY ,"
        "  `name` varchar(20) NOT NULL ,"
        "  `officeID` smallint NOT NULL ,"
        "  CONSTRAINT `fk_salesmen_offices` FOREIGN KEY (officeID)"
        "  REFERENCES offices(officeID) ON UPDATE CASCADE ON DELETE RESTRICT"
        ") ENGINE=InnoDB;"
    )
    INSERT_SALESMEN = (
        "INSERT INTO salesmen (salesmanID, name, officeID) "
        " VALUES(%s,%s,%s);"
    )
    TABLE_SALES = (
        "CREATE TABLE sales ("
        "  `saleID` smallint NOT NULL AUTO_INCREMENT PRIMARY KEY ,"
        "  `salesDate` date NOT NULL ,"
        "  `referenceID` smallint NOT NULL ,"
        "  `salesmanID` smallint NOT NULL ,"
        "  CONSTRAINT `fk_sales_clientReference` FOREIGN KEY (referenceID)"
        "  REFERENCES clientReferences(referenceID) ON UPDATE CASCADE ON DELETE RESTRICT ,"
        "  CONSTRAINT `fk_sales_salesmen` FOREIGN KEY (salesmanID)"
        "  REFERENCES salesmen(salesmanID) ON UPDATE CASCADE ON DELETE RESTRICT"
        ") ENGINE=InnoDB;"
    )
    INSERT_SALES = (
        "INSERT INTO sales (saleID, salesDate, referenceID, salesmanID) "
        " VALUES(%s,%s,%s,%s);"
    )
    TABLE_PRODUCTS = (
        "CREATE TABLE products ("
        "  `productID` smallint NOT NULL AUTO_INCREMENT PRIMARY KEY ,"
        "  `productName` varchar(15) NOT NULL ,"
        "  `price` smallint NOT NULL "
        ") ENGINE=InnoDB;"
    )
    INSERT_PRODUCTS = (
        "INSERT INTO products (productID, productName, price) "
        " VALUES(%s,%s,%s);"
    )
    TABLE_SALES_LINE_ITEM = (
        "CREATE TABLE salesLineItem ("
        "  `saleID` smallint NOT NULL ,"
        "  `productID` smallint NOT NULL ,"
        "  `quantity` smallint NOT NULL ,"
        "  CONSTRAINT `fk_salesLineItem_sales` FOREIGN KEY (saleID)"
        "  REFERENCES sales(saleID) ON UPDATE CASCADE ON DELETE RESTRICT ,"
        "  CONSTRAINT `fk_salesLineItem_products` FOREIGN KEY (productID)"
        "  REFERENCES products(productID) ON UPDATE CASCADE ON DELETE RESTRICT"
        ") ENGINE=InnoDB;"
    )
    INSERT_SALES_LINE_ITEM = (
        "INSERT INTO salesLineItem (saleID, productID, quantity) "
        " VALUES(%s,%s,%s);"
    )
    # SELECT_YEARS = (
    #     "SELECT  distinct(year(salesDate)) FROM sales;"
    # )
    # SELECT_MONTHS = (
    #     "SELECT  distinct(month(salesDate)) FROM sales"
    #     " where year(salesDate) = 2020 & 2021"
    #     " order by salesDate ASC;"
    # )
