import sqlite3

import os, sys

db = """

PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

CREATE TABLE Users (name TEXT, password TEXT, admin BOOL);

INSERT INTO Users VALUES('admin','coffee',1);

INSERT INTO Users VALUES('bob','passwd',0);

CREATE TABLE Tasks (name TEXT, body TEXT);

INSERT INTO Tasks VALUES('bob','become admin');

INSERT INTO Tasks VALUES('admin','good to be king');

INSERT INTO Tasks VALUES('bob','profit');

COMMIT;

"""


pathname = os.path.dirname(sys.argv[0])        
full_path = os.path.abspath(pathname)

if os.path.exists(f"{full_path}/db.sqlite3"):
	print('db.sqlite3 already exists')
else:
	conn = sqlite3.connect(f"{full_path}/db.sqlite3")
	conn.cursor().executescript(db)
	conn.commit()
