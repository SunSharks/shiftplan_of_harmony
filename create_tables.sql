CREATE TABLE Days (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NULL,
  date          DATE NOT NULL UNIQUE
);

CREATE TABLE Jobtypes (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NOT NULL,
  competences   INT NULL,
  special       BOOLEAN NOT NULL
);

CREATE TABLE Jobs (
    id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    abs_start     INT,
    abs_end       INT,
    during        INT,
    start_day_id  INT,
    end_day_id    INT,
    dt_start      INT,
    dt_end        INT,
    jt_primary    INT
);
