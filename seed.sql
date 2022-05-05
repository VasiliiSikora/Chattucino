INSERT INTO users(name, password, email, fav_coffee, beans) VALUES ('Vasilii Sikora', 'Apples1', 'vasiliisikora@example.com', 'Flat White', 0);


INSERT INTO posts(user_id, street_address, location, state, flair, date, max_people) VALUES (1, 'Gatehouse Drive', 'Kensington', 'Victoria', 'Just Chat', '2022-05-04', 3);

INSERT INTO user_page(user_id, about, hometown, age) VALUES (3, 'I enjoy long walks on the beach and sunsets. I love coffee and I want to share my love of coffee with others!', 'Kensington', 27);

-- SELECT COUNT(*) FROM interested WHERE (post_id=1 AND (going='P' OR going='Y'));

-- SELECT name FROM interested INNER JOIN users ON users.user_id=interested.interested_user WHERE (post_id=1 AND (going='P' OR going='Y'));

SELECT name, users.user_id FROM interested INNER JOIN users ON interested.interested_user=users.user_id WHERE (post_id=1 AND going='P');

UPDATE posts SET date='2022-05-08' WHERE post_id=1;
UPDATE posts SET date='2022-05-09' WHERE post_id=2;
UPDATE posts SET date='2022-05-06' WHERE post_id=3;