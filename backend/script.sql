CREATE TABLE IF NOT EXISTS pokemon (
	ID INT(4) NOT NULL AUTO_INCREMENT,
	name VARCHAR(32) NOT NULL UNIQUE,
	gen INT(4) NOT NULL,
	species VARCHAR(255) NOT NULL,
	height FLOAT NOT NULL,
	weight FLOAT NOT NULL,
	description VARCHAR(255) NOT NULL,
	base_experience SMALLINT(4) unsigned NOT NULL,
	hp INT NOT NULL,
	attack INT NOT NULL,
	defense INT NOT NULL,
	special_attack INT NOT NULL,
	special_defense INT NOT NULL,
	speed INT NOT NULL,
	male float,
	female float,
	PRIMARY KEY (ID)
);

CREATE TABLE IF NOT EXISTS abilities (
	ID INT NOT NULL AUTO_INCREMENT,
	ability VARCHAR(255) UNIQUE,
	abilityType VARCHAR(255),
	PRIMARY KEY (ID)
);


CREATE TABLE IF NOT EXISTS relAbilitiesPokemon (
	ID INT NOT NULL AUTO_INCREMENT,
	pokemonID INT NOT NULL,
	abilityID INT NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (pokemonID) REFERENCES pokemon(ID),
	FOREIGN KEY (abilityID) REFERENCES abilities(ID)
);


CREATE TABLE IF NOT EXISTS types (
	ID INT NOT NULL AUTO_INCREMENT,
	type VARCHAR(255) NOT NULL UNIQUE,
	PRIMARY KEY (ID)
);


CREATE TABLE IF NOT EXISTS relTypesPokemon (
	ID INT NOT NULL AUTO_INCREMENT,
	pokemonID INT NOT NULL,
	typeID INT NOT NULL,
	PRIMARY KEY (ID),
	FOREIGN KEY (pokemonID) REFERENCES pokemon(ID),
	FOREIGN KEY (typeID) REFERENCES types(ID)
);