CREATE TABLE IF NOT EXISTS family (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS people (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name TEXT NOT NULL,
    birthday DATE,
    deathday DATE,
    description TEXT,
    family_id INT,
    FOREIGN KEY (family_id) REFERENCES family (id)
);

CREATE TABLE IF NOT EXISTSD family_tie_types (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS family_ties (
    human_id1 INT,
    human_id2 INT,
    type INT,
    FOREIGN KEY (type) REFERENCES family_tie_types (id)
);
