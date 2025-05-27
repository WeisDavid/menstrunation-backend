CREATE TABLE users(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    username varchar(20),
    password varchar(64),
    age INT,
    weight FLOAT,
    height FLOAT
);

CREATE TABLE products(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(20),
    description TEXT
);

CREATE TABLE vendors(
	ID INT PRIMARY KEY AUTO_INCREMENT, 
	name varchar(20), 
	registerNr INT 
);

CREATE TABLE ratings(
     ID INT PRIMARY KEY AUTO_INCREMENT,
     rating INT, 
     description VARCHAR(255), 
     productID INT,
     userID INT,
     FOREIGN KEY (userID) REFERENCES users(ID),
     FOREIGN KEY (productID) REFERENCES product(ID)
 ); 

CREATE TABLE purchases(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    userID INT,
    FOREIGN KEY(userID) REFERENCES users(ID),
    productID INT,
    FOREIGN KEY(productID) REFERENCES products(ID),
    vendorID INT,
    FOREIGN KEY(vendorID) REFERENCES vendors(ID)
    );

CREATE TABLE offers(
    ID int PRIMARY KEY AUTO_INCREMENT,
    price float,
    productID int,
    FOREIGN KEY(productID) REFERENCES product(ID),
    vendorID int,
    FOREIGN KEY(vendorID) REFERENCES vendors(ID),
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

CREATE TABLE buddies(
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

CREATE TABLE periodDays(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    painlvl INT,
    condition TEXT,
    date DATE,
    cycleID INT,
    FOREIGN KEY (cycleID) REFERENCES cycles(ID)
);
