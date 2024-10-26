-- Creates a function SafeDiv that safely divides two numbers
-- Returns 0 if the denominator is 0

CREATE OR REPLACE FUNCTION SafeDiv(a INT, b INT)
RETURNS INT
RETURN IF(b = 0, 0, a / b);