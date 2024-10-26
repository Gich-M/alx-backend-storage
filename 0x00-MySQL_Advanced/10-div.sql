-- Creates a function SafeDiv that safely divides two numbers
-- Returns 0 if the denominator is 0

DROP FUNCTION IF EXISTS `safeDiv`;
DELIMITER $$

CREATE OR REPLACE FUNCTION SafeDiv(a INT, b INT) 
RETURNS DECIMAL(65,20)
BEGIN
    IF b = 0 THEN
        RETURN 0;
    END IF;
    RETURN a / b;
END $$

DELIMITER ;