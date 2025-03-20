-- auto-generated definition
create database starwars
    with owner carlitos;


CREATE TABLE people(
    id_people SERIAL PRIMARY KEY,
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
        amount INT NOT NULL DEFAULT 1,
        CONSTRAINT people_species_pkey PRIMARY KEY (id_people, id_species)
);

CREATE TABLE films(
    id_film SERIAL PRIMARY KEY,
    film TEXT NOT NULL
);

CREATE TABLE people_films(
    id_people INT REFERENCES people (id_people) ON UPDATE CASCADE ON DELETE CASCADE,
    id_film INT REFERENCES species (id_species) ON UPDATE CASCADE,
    amount INT NOT NULL DEFAULT 1,
    CONSTRAINT people_films_pkey PRIMARY KEY (id_people, id_film)
);

CREATE TABLE planets(
    id_planet SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    diameter NUMERIC,
    population INT,
    density NUMERIC
);