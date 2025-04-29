CREATE TABLE IF NOT EXISTS families (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS people (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    birthday DATE,
    deathday DATE,
    description TEXT,
    family_id INTEGER,
    FOREIGN KEY (family_id) REFERENCES family (id)
);

CREATE TABLE IF NOT EXISTS family_tie_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS family_ties (
    human_id1 INTEGER,
    human_id2 INTEGER,
    type INTEGER,
    FOREIGN KEY (type) REFERENCES family_tie_types (id),
    FOREIGN KEY (human_id1) REFERENCES people (id),
    FOREIGN KEY (human_id2) REFERENCES people (id)
);

INSERT INTO family_tie_types (id, title)
VALUES
    (1, 'Vertical'),
    (2, 'Horizontal'),
    (3, 'Marriage'),
    (4, 'Civil marriage')
;
