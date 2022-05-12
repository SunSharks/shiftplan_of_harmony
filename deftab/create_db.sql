DROP TABLE Jobs;

CREATE TABLE Jobs (
    id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name          VARCHAR(255) NOT NULL,
    abs_start     INT,
    abs_end       INT,
    during        INT,
    start_day     VARCHAR(255),
    end_day       VARCHAR(255),
    dt_start      INT,
    dt_end        INT,
    jt_primary    INT
);

CREATE TABLE Days (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NOT NULL
);

DROP TABLE Jobtypes;
CREATE TABLE Jobtypes (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NOT NULL,
  competences   INT NULL,
  special       BOOLEAN NOT NULL
);

DROP TABLE Jobs_without_Jobtypes;
CREATE TABLE Jobs_without_Jobtypes (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    abs_start     INT,
    abs_end       INT,
    during        INT,
    start_day     VARCHAR(255),
    end_day       VARCHAR(255),
    dt_start      INT,
    dt_end        INT,
    special		    BOOLEAN NOT NULL
);
