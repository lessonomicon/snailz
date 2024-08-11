'''Generate database from data files.'''

import json
import polars as pl
import sqlite3


ISO_DATE = '%Y-%m-%d'
SCHEMA = '''\
DROP TABLE IF EXISTS site;
CREATE TABLE site (
	site_id TEXT PRIMARY KEY,
	lon FLOAT NOT NULL,
	lat FLOAT NOT NULL
);
DROP TABLE IF EXISTS survey;
CREATE TABLE survey (
	survey_id INTEGER PRIMARY KEY,
	site_id TEXT NOT NULL,
	date DATE,
	FOREIGN KEY(site_id) REFERENCES site(site_id)
);
DROP TABLE IF EXISTS sample;
CREATE TABLE sample (
	sample_id INTEGER PRIMARY KEY,
	survey_id INTEGER NOT NULL,
	lon FLOAT NOT NULL,
	lat FLOAT NOT NULL,
	sequence TEXT NOT NULL,
	size FLOAT NOT NULL,
	FOREIGN KEY(survey_id) REFERENCES survey(survey_id)
);
DROP TABLE IF EXISTS experiment;
CREATE TABLE experiment (
	sample_id INTEGER PRIMARY KEY,
	kind TEXT NOT NULL,
	start DATE NOT NULL,
	"end" DATE,
	FOREIGN KEY(sample_id) REFERENCES sample(sample_id)
);
DROP TABLE IF EXISTS staff;
CREATE TABLE staff (
	staff_id INTEGER PRIMARY KEY,
	personal TEXT NOT NULL,
	family TEXT NOT NULL
);
DROP TABLE IF EXISTS performed;
CREATE TABLE performed (
	staff_id INTEGER NOT NULL,
	sample_id INTEGER NOT NULL,
	PRIMARY KEY(staff_id, sample_id)
);
DROP TABLE IF EXISTS plate;
CREATE TABLE plate (
	plate_id INTEGER PRIMARY KEY,
	sample_id INTEGER NOT NULL,
	date DATE NOT NULL,
	filename TEXT NOT NULL,
	FOREIGN KEY(sample_id) REFERENCES sample(sample_id)
);
DROP TABLE IF EXISTS invalidated;
CREATE TABLE invalidated (
	plate_id INTEGER NOT NULL,
	staff_id INTEGER NOT NULL,
	date DATE,
	FOREIGN KEY(plate_id) REFERENCES plate(plate_id),
	FOREIGN KEY(staff_id) REFERENCES staff(staff_id),
	UNIQUE(plate_id, staff_id)
);
'''


def db(options):
    '''Main driver.'''
    _create_schema(options.dbfile)

    url = f'sqlite:///{options.dbfile}'

    _csv_to_db(url, 'staff', options.staff)
    _csv_to_db(url, 'sample', options.samples)
    _csv_to_db(url, 'site', options.sites)
    _csv_to_db(url, 'survey', options.surveys, dates=['date'], columns=['survey_id', 'site_id', 'date'])

    assays = json.load(open(options.assays, 'r'))
    _json_to_db(url, assays, 'experiment', dates=['start', 'end'])
    _json_to_db(url, assays, 'performed')
    _json_to_db(url, assays, 'plate', dates=['date'])
    _json_to_db(url, assays, 'invalidated', dates=['date'])


def _create_schema(dbfile):
    '''Create database schema.'''
    connection = sqlite3.connect(dbfile)
    connection.executescript(SCHEMA)


def _csv_to_db(url, name, source, dates=[], columns=[]):
    '''Create table from CSV.'''
    df = pl.read_csv(source)
    if columns:
        df = df[columns]
    df = _convert_dates(df, dates)
    df.write_database(name, url, if_table_exists='append')


def _json_to_db(url, data, name, dates=[]):
    '''Create table from JSON.'''
    df = pl.DataFrame(data[name])
    df = _convert_dates(df, dates)
    df.write_database(name, url, if_table_exists='append')


def _convert_dates(df, dates):
    '''Convert text columns to dates.'''
    for colname in dates:
        df = df.with_columns(pl.col(colname).str.to_date(ISO_DATE))
    return df
