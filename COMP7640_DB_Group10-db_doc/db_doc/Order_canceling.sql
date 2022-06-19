delimiter //
CREATE TRIGGER Order_canceling
AFTER DELETE ON Orders
FOR EACH ROW
BEGIN
UPDATE Item SET Item_qty=Item_qty+OLD.Order_qty WHERE iid=OLD.iid and sid=OLD.sid; 
IF OLD.oid NOT IN (SELECT DISTINCT(oid) FROM Orders) THEN
DELETE FROM Order_info WHERE oid=OLD.oid;
END IF;
END//
delimiter ;

-- 查看所有触发器
-- select * from information_schema.triggers;


-- 查看Order_canceling触发器
-- select * from information_schema.triggers where trigger_name='Order_canceling';


-- 撤销触发器
-- drop  trigger Order_canceling;
