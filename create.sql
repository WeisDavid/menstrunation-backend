CREATE TABLE user(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    username varchar(20),
    `alter` INT,
    gewicht FLOAT,
    groesse FLOAT
);

CREATE TABLE product(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(20),
    beschreibung TEXT
);

CREATE TABLE handler( 
	ID INT PRIMARY KEY AUTO_INCREMENT, 
	name varchar(20), 
	registerNr INT 
);

CREATE TABLE rating(
     ID INT PRIMARY KEY AUTO_INCREMENT,
     punktzahl INT, 
     beschreibung VARCHAR(255), 
     produktID INT,
     benutzerID INT,
     FOREIGN KEY (benutzerID) REFERENCES benutzer (ID),
     FOREIGN KEY (produktID) REFERENCES produkt (ID)
 ); 

CREATE TABLE buy(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    benutzerID INT,
    FOREIGN KEY(benutzerID) REFERENCES benutzer (ID),
    produktID INT,
    FOREIGN KEY(produktID) REFERENCES produkt (ID),
    haendlerID INT,
    FOREIGN KEY(haendlerID) REFERENCES haendler (ID)
    );

CREATE TABLE offer (
 
    ID int PRIMARY KEY AUTO_INCREMENT,
    preis float,
    produktID int,
    FOREIGN KEY(produktID) REFERENCES produkt (ID),
    haendlerID int
);

ALTER TABLE angebot
	ADD FOREIGN KEY (haendlerID) REFERENCES haendler(ID);

CREATE TABLE cycle (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    eisprung DATE,
    benutzerID INT,
    FOREIGN KEY (benutzerID) REFERENCES benutzer (ID)
);
 
CREATE TABLE fruchtbarerTag (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    schwangerschaftswahrscheinlichkeit FLOAT,
    zyklusID INT,
    FOREIGN KEY (zyklusID) REFERENCES zyklus(ID)
);

CREATE TABLE buddy(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    benutzerID1 INT,
    FOREIGN KEY(benutzerID1) REFERENCES benutzer (ID),
    benutzerID2 INT,
    FOREIGN KEY(benutzerID2) REFERENCES benutzer (ID)
    );

CREATE TABLE chillDay (
  ID INT PRIMARY KEY AUTO_INCREMENT,
  datum DATE,
  zyklusID INT,
  FOREIGN KEY (zyklusID) REFERENCES zyklus (ID)
);

CREATE TABLE periodDay (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    schmerzlevel INT,
    befinden TEXT,
    datum DATE,
    zyklusID INT,
    FOREIGN KEY (zyklusID) REFERENCES zyklus(ID)
);
