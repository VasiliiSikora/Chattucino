DROP TABLE IF EXISTS users;
DROP TABLE IF EXISTS posts;
DROP TABLE IF EXISTS going;

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    name TEXT,
    password TEXT,
    email TEXT,
    fav_coffee TEXT,
    beans INTEGER
);

CREATE TABLE posts (
    post_id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(user_id),
    street_address TEXT,
    location TEXT,
    state TEXT,
    flair TEXT,
    date DATE,
    max_people INTEGER
);

CREATE TABLE interested (
    post_id INTEGER REFERENCES posts(post_id),
    interested_user INTEGER REFERENCES users(user_id),
    going VARCHAR(1)
);