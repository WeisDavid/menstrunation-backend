CREATE TABLE users(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    username varchar(20) UNIQUE,
    email varchar(50),
    password varchar(64),
    age INT,
    weight FLOAT,
    height FLOAT
);

CREATE TABLE buddies(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    userID1 INT,
    FOREIGN KEY(userID1) REFERENCES users(ID) ON DELETE CASCADE,
    userID2 INT,
    FOREIGN KEY(userID2) REFERENCES users(ID) ON DELETE CASCADE
    );

CREATE TABLE diaryDays (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    painlvl INT,
    content TEXT,
    date DATE,
    isPeriod BOOLEAN,
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(ID)
);
