-- Creates a stored procedure `ComputeAverageScoreForUser` that
-- computes and store the average score for a student.
-- An average score can be a decimal

DROP PROCEDURE IF EXISTS `ComputeAverageScoreForStudent`;

DELIMITER $$

CREATE PROCEDURE ComputeAverageScoreForUser (
IN user_id INT
)
BEGIN
    UPDATE users
    SET average_score = (
        SELECT AVG(score)
        FROM corrections
        WHERE corrections.user_id = user_id
    )
    WHERE id = user_id;
END $$

DELIMITER ;