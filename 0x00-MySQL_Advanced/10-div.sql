-- Creates a function SafeDiv that safely divides two numbers
-- Returns 0 if the denominator is 0

DROP FUNCTION IF EXISTS SafeDiv;
DELIMITER $$

CREATE FUNCTION SafeDiv(a INT, b INT) 
RETURNS FLOAT DETERMINISTIC
BEGIN
    DECLARE result FLOAT DEFAULT 0;
    
    IF b = 0 THEN
        RETURN 0;
    END IF;
    RETURN a / b;
END $$

DELIMITER ;