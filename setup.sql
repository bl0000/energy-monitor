CREATE DATABASE energymon;

USE energymon;

CREATE TABLE power_used (
	id INT PRIMARY KEY AUTO_INCREMENT,
	watts SMALLINT,
	cost_in_pence SMALLINT,
	added DATETIME
);

CREATE TABLE total_cost (
	id INT PRIMARY KEY AUTO_INCREMENT,
	total_watts SMALLINT,
	total_cost SMALLINT,
	added DATETIME
);

CREATE USER 'energymon-admin'@'%' IDENTIFIED BY 'password'; -- change this

GRANT SELECT, INSERT, UPDATE, DELETE, CREATE, DROP, INDEX, ALTER, LOCK TABLES ON energymon.* TO 'energymon-admin'@'%';

