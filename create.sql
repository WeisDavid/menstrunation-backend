CREATE TABLE users(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    username varchar(20),
    email varchar(50),
    password varchar(64),
    age INT,
    weight FLOAT,
    height FLOAT
);
  
CREATE TABLE cycles(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    ovulation DATE,
    userID INT,
    FOREIGN KEY (userID) REFERENCES users(ID)
);

CREATE TABLE fertileDays(
    ID INT AUTO_INCREMENT PRIMARY KEY,
    pregnancy_probability FLOAT,
    cycleID INT,
    FOREIGN KEY (cycleID) REFERENCES cycles(ID)
);
 
CREATE TABLE buddys(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    userID1 INT,
    FOREIGN KEY(userID1) REFERENCES users(ID),
    userID2 INT,
    FOREIGN KEY(userID2) REFERENCES users(ID)
    );
 
CREATE TABLE chillDays(
  ID INT PRIMARY KEY AUTO_INCREMENT,
  date DATE,
  cycleID INT,
  FOREIGN KEY (cycleID) REFERENCES cycles(ID)
);
 
CREATE TABLE diaryDays(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    painlvl INT,
    content TEXT,
    periodday BOOLEAN,
    date DATE,
    cycleID INT,
    FOREIGN KEY (cycleID) REFERENCES cycles(ID)
); 