DROP TYPE IF EXISTS platform_type_state;

CREATE TYPE platform_type_state AS ENUM('home', 'handheld', 'hybrid');

CREATE TABLE IF NOT EXISTS platforms(
	platform_id VARCHAR(15),
	platform_name VARCHAR(30),
	manufacturer VARCHAR(30),
	platform_type platform_type_state DEFAULT 'home',
	generation SMALLINT,
	CONSTRAINT platforms_pkey PRIMARY KEY (platform_id)
);

CREATE TABLE IF NOT EXISTS games(
	game_id SERIAL,
	game_token VARCHAR(255) NOT NULL,
	title VARCHAR(255) NOT NULL,
	platform_id VARCHAR(15),
	release_date VARCHAR(10) NOT NULL,
	status status_state,
	notes TEXT,
	CONSTRAINT games_pkey PRIMARY KEY (game_id),
	CONSTRAINT platforms_fkey FOREIGN KEY (platform_id) REFERENCES platforms (platform_id)
);

CREATE TABLE IF NOT EXISTS genres(
	genre_id VARCHAR(30),
	CONSTRAINT genres_pkey PRIMARY KEY (genre_id)
);

CREATE TABLE IF NOT EXISTS game_genres(
	game_id INT,
	genre_id VARCHAR(30),
	CONSTRAINT game_genres_pkey PRIMARY KEY (game_id, genre_id),
	CONSTRAINT game_fkey FOREIGN KEY (game_id) REFERENCES games (game_id),
	CONSTRAINT genre_fkey FOREIGN KEY (genre_id) REFERENCES genres (genre_id)
);

INSERT INTO genres (genre_id)
VALUES
('action'),
('arcade'),
('platformer'),
('fighting'),
('adventure'),
('shooter'),
('beat ''em up'),
('shoot ''em up'),
('survival'),
('horror'),
('rpg'),
('online'),
('metroidvania'),
('soulslike'),
('slasher'),
('visual novel'),
('interactive movie'),
('puzzle'),
('quest'),
('jrpg'),
('roguelike'),
('simulation'),
('strategy'),
('racing'),
('music'),
('unique');

INSERT INTO platforms (platform_id, platform_name, manufacturer, platform_type, generation)
VALUES
	('pc', 'PC', NULL, 'home', NULL),
	('dendy', 'Dendy', NULL, 'home', 3),
	('fc', 'Famicom/NES', 'Nintendo', 'home', 3),
	('sms', 'Master System', 'Sega', 'home', 3),
	('smd', 'Mega Drive', 'Sega', 'home', 4),
	('sfc', 'Super Famicom/SNES', 'Nintendo', 'home', 4),
	('gb', 'Game Boy', 'Nintendo', 'handheld', 4),
	('gg', 'Game Gear', 'Sega', 'handheld', 4),
	('strn', 'Saturn', 'Sega', 'home', 5),
	('ps1', 'PlayStation', 'Sony', 'home', 5),
	('n64', 'Nintendo 64', 'Nintendo', 'home', 5),
	('gbc', 'Game Boy Color', 'Nintendo', 'handheld', 5),
	('dc', 'Dreamcast', 'Sega', 'home', 6),
	('ps2', 'PlayStation 2', 'Sony', 'home', 6),
	('gc', 'GameCube', 'Nintendo', 'home', 6),
	('xbox', 'Xbox', 'Microsoft', 'home', 6),
	('gba', 'Game Boy Advance', 'Nintendo', 'handheld', 6),
	('x360', 'Xbox 360', 'Microsoft', 'home', 7),
	('ps3', 'PlayStation 3', 'Sony', 'home', 7),
	('wii', 'Wii', 'Nintendo', 'home', 7),
	('ds', 'Nintendo DS', 'Nintendo', 'handheld', 7),
	('psp', 'PlayStation Portable', 'Sony', 'handheld', 7),
	('wiiu', 'Wii U', 'Nintendo', 'home', 8),
	('ps4', 'PlayStation 4', 'Sony', 'home', 8),
	('xone', 'Xbox One', 'Microsoft', 'home', 8),
	('sw', 'Switch', 'Nintendo', 'hybrid', 8),
	('3ds', 'Nintendo 3DS', 'Nintendo', 'handheld', 8),
	('psv', 'PlayStation Vita', 'Sony', 'handheld', 8),
	('xs', 'Xbox Series', 'Microsoft', 'home', 9),
	('ps5', 'PlayStation 5', 'Sony', 'home', 9),
	('sw2', 'Switch 2', 'Nintendo', 'hybrid', 9);

CREATE TABLE game_catalog2 AS SELECT * FROM game_catalog;

UPDATE game_catalog2
SET platform = 'fc'
WHERE platform = 'famicom';

UPDATE game_catalog2
SET platform = 'sms'
WHERE platform = 'master system';

UPDATE game_catalog2
SET platform = 'smd'
WHERE platform = 'mega drive';

UPDATE game_catalog2
SET platform = 'sfc'
WHERE platform = 'super famicom';

UPDATE game_catalog2
SET platform = 'gb'
WHERE platform = 'game boy';

UPDATE game_catalog2
SET platform = 'gg'
WHERE platform = 'game gear';

UPDATE game_catalog2
SET platform = 'strn'
WHERE platform = 'saturn';

UPDATE game_catalog2
SET platform = 'n64'
WHERE platform = 'nintendo 64';

UPDATE game_catalog2
SET platform = 'gbc'
WHERE platform = 'game boy color';

UPDATE game_catalog2
SET platform = 'dc'
WHERE platform = 'dreamcast';

UPDATE game_catalog2
SET platform = 'gc'
WHERE platform = 'gamecube';

UPDATE game_catalog2
SET platform = 'gba'
WHERE platform = 'game boy advance';

UPDATE game_catalog2
SET platform = 'x360'
WHERE platform = 'xbox 360';

UPDATE game_catalog2
SET platform = 'wiiu'
WHERE platform = 'wii u';

UPDATE game_catalog2
SET platform = 'xone'
WHERE platform = 'xbox one';

UPDATE game_catalog2
SET platform = 'sw'
WHERE platform = 'switch';

UPDATE game_catalog2
SET platform = 'psv'
WHERE platform = 'ps vita';

UPDATE game_catalog2
SET platform = 'xs'
WHERE platform = 'xbox series';

UPDATE game_catalog2
SET platform = 'sw2'
WHERE platform = 'switch 2';



INSERT INTO games (game_token, title, platform_id, release_date, status, notes)
SELECT game_id, title, platform, release_date, status, notes
FROM game_catalog2;

INSERT INTO game_genres
SELECT g.game_id, UNNEST(genres)
FROM games AS g
JOIN game_catalog2 AS gc ON g.game_token = gc.game_id;

DROP TABLE game_catalog2;

CREATE TABLE IF NOT EXISTS migrations(
	migration_id INT PRIMARY KEY,
	migration_name TEXT NOT NULL,
	applied_at TIMESTAMP NOT NULL
);

INSERT INTO migrations (migration_id, migration_name, applied_at)
VALUES (1, '001_5-table_structure_implemented', NOW());