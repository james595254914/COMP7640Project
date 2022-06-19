CREATE DATABASE IF NOT EXISTS comp7640 DEFAULT CHARACTER SET utf8;

USE comp7640;

CREATE TABLE IF NOT EXISTS Shop
(
    sid varchar (8) NOT NULL,
    sname varchar (255) NOT NULL,
    rating int,
    location varchar (255) NOT NULL,
    PRIMARY KEY(sid)
);

CREATE TABLE IF NOT EXISTS Customer
(
    cid varchar (8) NOT NULL,
    tel varchar (255) NOT NULL,
    addr varchar (255) NOT NULL,
    PRIMARY KEY(cid)
);

CREATE TABLE IF NOT EXISTS Item
(
    iid varchar (8) NOT NULL,
    sid varchar (4),
    iname varchar (255) NOT NULL,
    price int NOT NULL,
    kw1 varchar (255),
    kw2 varchar (255),
    kw3 varchar (255),
    Item_qty int,
    PRIMARY KEY(iid, sid),
    FOREIGN KEY (sid) REFERENCES Shop(sid)
);

CREATE TABLE IF NOT EXISTS Order_info
(
    oid varchar (8) NOT NULL,
    cid varchar (8) NOT NULL,
    PRIMARY KEY(oid),
    FOREIGN KEY (cid) REFERENCES Customer(cid)
);

CREATE TABLE IF NOT EXISTS Orders
(
    oid varchar (8) NOT NULL,
    sid varchar (8) NOT NULL,
    iid varchar (8) NOT NULL,
    price int NOT NULL,
    Order_qty int,
    total int,
    PRIMARY KEY(oid, sid, iid),
    FOREIGN KEY (oid) REFERENCES Order_info(oid) ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (iid, sid) REFERENCES Item(iid, sid)
);
