DROP DATABASE IF EXISTS tirelire;
DROP ROLE IF EXISTS test_user;
CREATE ROLE test_user LOGIN ENCRYPTED PASSWORD 'test';
CREATE DATABASE tirelire OWNER test_user;

\c tirelire test_user

CREATE TYPE change_type AS ENUM ('coin', 'note');

CREATE TABLE piggybank (
    id serial,
    name text,
    broken bool DEFAULT FALSE
);

CREATE TABLE change (
    id serial,
    kind change_type NOT NULL,
    value int NOT NULL
);

CREATE TABLE wealth (
    id serial,
    piggybank_id bigint,
    change_id bigint
);

CREATE UNIQUE INDEX ON piggybank (id);

CREATE UNIQUE INDEX ON change (id);

ALTER TABLE wealth ADD CONSTRAINT wealth_piggybank_id_fkey FOREIGN KEY (piggybank_id) REFERENCES piggybank(id);
ALTER TABLE wealth ADD CONSTRAINT wealth_change_id_fkey FOREIGN KEY (change_id) REFERENCES change(id);
CREATE INDEX ON wealth ((piggybank_id));

\i /sql/changes.sql

\i /sql/data-test.sql
