import sqlite3

import os, sys

db = """

PRAGMA foreign_keys=OFF;

BEGIN TRANSACTION;

CREATE TABLE Users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT, 
    password TEXT, 
    admin BOOL
);

INSERT INTO Users (name, password, admin) VALUES('admin','coffee',1);

INSERT INTO Users (name, password, admin) VALUES('bob','passwd',0);

CREATE TABLE Posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT, 
    body TEXT, 
    image_url TEXT, 
    creator INTEGER,
    created_on DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY(creator) REFERENCES Users(id)
);

INSERT INTO Posts 
    (title, body, image_url, creator) 
    VALUES(
        'First post', 
        'This is my first post', 
        'https://i.kym-cdn.com/photos/images/newsfeed/000/096/044/trollface.jpg?1296494117', 
        1
    );

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
