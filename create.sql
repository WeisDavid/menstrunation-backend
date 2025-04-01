CREATE TABLE benutzer(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    username varchar(20),
    `alter` INT,
    gewicht FLOAT,
    groesse FLOAT
);

CREATE TABLE produkt(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    name varchar(20),
    beschreibung TEXT
);

CREATE TABLE haendler( 
	ID INT PRIMARY KEY AUTO_INCREMENT, 
	name varchar(20), 
	registerNr INT 
);

CREATE TABLE bewertung(
     ID INT PRIMARY KEY AUTO_INCREMENT,
     punktzahl INT, 
     beschreibung VARCHAR(255), 
     produktID INT,
     benutzerID INT,
     FOREIGN KEY (benutzerID) REFERENCES benutzer (ID),
     FOREIGN KEY (produktID) REFERENCES produkt (ID)
 ); 

CREATE TABLE kauf(
    ID INT PRIMARY KEY AUTO_INCREMENT,
    benutzerID INT,
    FOREIGN KEY(benutzerID) REFERENCES benutzer (ID),
    produktID INT,
    FOREIGN KEY(produktID) REFERENCES produkt (ID),
    haendlerID INT,
    FOREIGN KEY(haendlerID) REFERENCES haendler (ID)
    );

CREATE TABLE angebot (
 
    ID int PRIMARY KEY AUTO_INCREMENT,
    preis float,
    produktID int,
    FOREIGN KEY(produktID) REFERENCES produkt (ID),
    haendlerID int
);

ALTER TABLE angebot
	ADD FOREIGN KEY (haendlerID) REFERENCES haendler(ID);

CREATE TABLE zyklus (
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

CREATE TABLE chillTag (
  ID INT PRIMARY KEY AUTO_INCREMENT,
  datum DATE,
  zyklusID INT,
  FOREIGN KEY (zyklusID) REFERENCES zyklus (ID)
);

CREATE TABLE periodenTag (
    ID INT PRIMARY KEY AUTO_INCREMENT,
    schmerzlevel INT,
    befinden TEXT,
    datum DATE,
    zyklusID INT,
    FOREIGN KEY (zyklusID) REFERENCES zyklus(ID)
);
