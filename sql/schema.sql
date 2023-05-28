PRAGMA foreign_keys = ON;
CREATE TABLE users(
  username VARCHAR(20) NOT NULL,
  fullname VARCHAR(40) NOT NULL,
  email VARCHAR(40) NOT NULL,
  filename VARCHAR(64) NOT NULL,
  password VARCHAR(256) NOT NULL, 
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  admin INTEGER NOT NULL,
  PRIMARY KEY(username)
);
CREATE TABLE items(
  itemid INTEGER PRIMARY KEY AUTOINCREMENT, 
  filename VARCHAR(64) NOT NULL,
  owner VARCHAR(20) NOT NULL,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY(owner)
    REFERENCES users
    ON DELETE CASCADE
);

CREATE TABLE comments(
  commentid INTEGER PRIMARY KEY AUTOINCREMENT,
  owner VARCHAR(20) NOT NULL,
  itemid INTEGER NOT NULL,
  text CHAR(1024) NOT NULL,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT owner_cs
    FOREIGN KEY(owner)
    REFERENCES users
    ON DELETE CASCADE
  CONSTRAINT item_cs
    FOREIGN KEY(itemid)
    REFERENCES items
    ON DELETE CASCADE
);
CREATE TABLE likes(
  likeid INTEGER PRIMARY KEY AUTOINCREMENT,
  owner VARCHAR(20) NOT NULL,
  itemid INTEGER NOT NULL,
  created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT owner_cs
    FOREIGN KEY(owner)
    REFERENCES users
    ON DELETE CASCADE
  CONSTRAINT item_cs
    FOREIGN KEY(itemid)
    REFERENCES items
    ON DELETE CASCADE
);