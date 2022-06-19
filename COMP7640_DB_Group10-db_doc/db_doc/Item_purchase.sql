delimiter //
CREATE TRIGGER Item_purchase
AFTER INSERT ON Orders
FOR EACH ROW
BEGIN
UPDATE Item SET Item_qty=Item_qty-NEW.Order_qty WHERE iid=NEW.iid;
END
//
delimiter ;

-- 查看所有触发器
-- select * from information_schema.triggers

-- 查看Item_purchase触发器
-- select * from information_schema.triggers where trigger_name='Item_purchase';

-- 撤销触发器
-- drop  trigger Item_purchase;













