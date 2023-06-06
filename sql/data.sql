PRAGMA foreign_keys = ON;

INSERT INTO users(username, fullname, email, filename, password, created, admin)
VALUES 
('ananyaj', 'Ananya Joshi', 'ananyaj@umich.edu', 'IMG_4669.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8', (datetime('now')), 1),
('userjack', 'Jack Black', 'gotyournose@gmail.com', 'pp.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8', (datetime('now')), 0),
('usernatalie', 'Natalie Portman', 'starwarsbaddie@yahoo.com', 'pp.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8', (datetime('now')), 1),
('userjonas', 'Joe Jonas', 'shorterthanmywife@gmail.com', 'pp.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8', (datetime('now')), 0),
('userallison', 'Allison Brie', 'communitychest@gmail.com', 'pp.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8', (datetime('now')), 0),
('usersophia', 'Sophia Vegara', 'highheels@yahoo.com', 'pp.jpeg', 'sha512$a45ffdcc71884853a2cba9e6bc55e812$c739cef1aec45c6e345c8463136dc1ae2fe19963106cf748baf87c7102937aa96928aa1db7fe1d8da6bd343428ff3167f4500c8a61095fb771957b4367868fb8', (datetime('now')), 0);
INSERT INTO items(filename, owner, available, created, name, price)
VALUES 
('jewel1.jpg', 'ananyaj', 1, (datetime('now')), 'Ocean Earrings', 7.5),
('jewel2.jpg', 'usernatalie', 1, (datetime('now')), 'Lightly used jacket', 19.9),
('jewel3.jpg', 'ananyaj', 0, (datetime('now')), 'Vintage pleated skirt', 29.0),
('jewel4.jpg', 'ananyaj', 1, (datetime('now')), 'Sheep skin belt', 11.4);

 INSERT INTO comments(owner, itemid, text, created)
 VALUES
 ('userjack', 3, 'I bought this a while ago! Highly recommend', (datetime('now'))),
 ('usersophia', 3, 'Do you have this piece in red?', (datetime('now'))),
 ('ananyaj', 3, 'Sold already!', (datetime('now'))), 
 ('userjonas', 2, '<3', (datetime('now'))),
 ('userjack', 2, 'oh this is cool', (datetime('now'))), 
 ('usersophia', 1, 'SO PRETTY', (datetime('now'))), 
 ('userallison', 4, 'I just ordered this! So excited', (datetime('now'))), 
 ('userjonas', 4, 'My wife would love this', (datetime('now')));
 INSERT INTO likes(owner, itemid, created)
 VALUES
 ('ananyaj', 1, (datetime('now'))),
 ('userjack', 1, (datetime('now'))),
 ('userjonas', 1, (datetime('now'))),
 ('userallison', 1, (datetime('now'))),
 ('usernatalie', 2, (datetime('now'))),
 ('userjack', 2, (datetime('now'))),
 ('userjonas', 2, (datetime('now'))),
 ('userjonas', 3, (datetime('now'))),
 ('ananyaj', 3, (datetime('now'))),
 ('usersophia', 4, (datetime('now')));