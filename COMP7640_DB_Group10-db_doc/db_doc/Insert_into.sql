SET FOREIGN_KEY_CHECKS=0;
DELETE FROM Shop;
DELETE FROM Customer;
DELETE FROM Item;
DELETE FROM Order_info;

INSERT INTO Shop  VALUES
('S1', 'Fruit shop', '5', 'Lok Fu'),
('S2', 'Phone shop', '5', 'Mong Kok'),
('S3', 'Book shop', '4', 'Kowloon Tong');

INSERT INTO Customer VALUES
('C1', '1111', 'Tuen Mun'),
('C2', '2222', 'Diamond Hill'),
('C3', '3333', 'Tai Wai');

INSERT INTO Item VALUES
('I1', 'S1', 'Apple',10,	'Red',	'Sweet','',200),
('I2', 'S1', 'Orange',8,	'Yellow','Fresh','Australia',100),
('I3', 'S2', 'Apple',8000,'Red',	'256G','',50),
('I4', 'S2', 'Samsung',7000,	'Black','128G','Folding',20),
('I5', 'S3', 'DB',500,	'Paperback','Relational','SQL',90),
('I3', 'S3', 'AI',400,'Paperback','Deep learning','Python',95);

SET FOREIGN_KEY_CHECKS=1;
