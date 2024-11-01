CREATE TABLE scores (
    id TEXT PRIMARY KEY,
    avatar INTEGER,
    playername TEXT UNIQUE,
    points INTEGER
);

