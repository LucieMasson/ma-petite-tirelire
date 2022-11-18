DROP DATABASE IF EXISTS tirelire;
DROP ROLE IF EXISTS test_user;
CREATE ROLE test_user LOGIN ENCRYPTED PASSWORD 'test';
CREATE DATABASE tirelire OWNER test_user;

\c tirelire test_user

CREATE TYPE monnaie_type AS ENUM ('piece', 'billet');

CREATE TABLE tirelire (
    id serial,
    name text,
    broken bool DEFAULT FALSE
);

CREATE TABLE monnaie (
    id serial,
    kind monnaie_type NOT NULL,
    value int NOT NULL
);

CREATE TABLE richesse (
    tirelire_id bigint,
    monnaie_id bigint,
    count int DEFAULT 0
);

CREATE UNIQUE INDEX ON tirelire (id);

CREATE UNIQUE INDEX ON monnaie (id);

ALTER TABLE richesse ADD CONSTRAINT richesse_tirelire_id_fkey FOREIGN KEY (tirelire_id) REFERENCES tirelire(id);
ALTER TABLE richesse ADD CONSTRAINT richesse_monnaie_id_fkey FOREIGN KEY (monnaie_id) REFERENCES monnaie(id);

COPY monnaie (kind, value) FROM stdin;
piece	1
piece	2
piece	5
piece	10
piece	20
piece	50
piece	100
piece	200
billet	500
billet	1000
billet	2000
billet	5000
billet	10000
billet	20000
billet	50000
\.
