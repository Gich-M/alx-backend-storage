-- Creates a table `users` with given attributes
DROP TABLE IF EXISTS users;
CREATE TABLE users (
	id INT NOT NULL AUTO_INCREMENT PRIMARY_KEY,
	email VARCHAR(255) NOT NULL UNIQUE,
	name VARCHAR(255)
);
