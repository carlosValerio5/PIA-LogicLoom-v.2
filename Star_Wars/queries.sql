CREATE DATABASE starwars;

CREATE TABLE planets(
                        id_planet SERIAL PRIMARY KEY,
                        planet TEXT NOT NULL,
                        diameter NUMERIC,
                        population BIGINT,
                        density NUMERIC
);

CREATE TABLE people(
    id_people INT PRIMARY KEY,
    person TEXT NOT NULL,
    homeworld INT REFERENCES planets (id_planet),
    mass numeric NOT NULL DEFAULT 0
);

CREATE TABLE species(
    id_species SERIAL PRIMARY KEY,
    species TEXT
);

CREATE TABLE people_species(
    id_people INT REFERENCES people (id_people) ON UPDATE CASCADE ON DELETE CASCADE,
    id_species INT REFERENCES species (id_species) ON UPDATE CASCADE,
    CONSTRAINT people_species_pkey PRIMARY KEY (id_people, id_species)
);

CREATE TABLE films(
    id_film SERIAL PRIMARY KEY,
    film TEXT NOT NULL
);

CREATE TABLE people_films(
    id_people INT REFERENCES people (id_people) ON UPDATE CASCADE ON DELETE CASCADE,
    id_film INT REFERENCES films (id_film) ON UPDATE CASCADE,
    CONSTRAINT people_films_pkey PRIMARY KEY (id_people, id_film)
);



ALTER TABLE species ADD CONSTRAINT species_unique UNIQUE (species);


ALTER TABLE films ADD CONSTRAINT film_unique UNIQUE (film);


ALTER TABLE planet_climate
ADD CONSTRAINT fk_planet_climate FOREIGN KEY (id_planet)
REFERENCES planets (id_planet);

ALTER TABLE planet_climate
ADD CONSTRAINT fk_climate FOREIGN KEY (id_climate)
REFERENCES climate (id);




CREATE TABLE planet_climate (
    id_planet INT,
    id_climate INT,
    CONSTRAINT planet_climate_pkey PRIMARY KEY (id_planet, id_climate)
);

CREATE TABLE climate (
    id SERIAL PRIMARY KEY,
    name TEXT
);


ALTER TABLE climate
ADD CONSTRAINT climate_name_unique UNIQUE (name);


