CREATE DATABASE Testplan CHARACTER SET utf8 COLLATE utf8_general_ci;

--
-- DROP TABLE Days;
-- DROP TABLE Jobtypes;
-- DROP TABLE Jobs;
-- DROP TABLE Users;


CREATE TABLE Days (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NULL,
  date          DATE NOT NULL UNIQUE
);
CREATE TABLE Jobtypes (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NOT NULL,
  competences   TEXT NULL,
  special       BOOLEAN NOT NULL DEFAULT 0,
  helper        BOOLEAN NOT NULL DEFAULT 0,
  user_id       INT NOT NULL
);

CREATE TABLE Twins (
  id            INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  name          VARCHAR(255) NOT NULL,
  competences   TEXT NULL,
  special       BOOLEAN NOT NULL DEFAULT 0,
  helper        BOOLEAN NOT NULL DEFAULT 0,
  jt_primary    INT NOT NULL
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
CREATE TABLE Users (
    id           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    fullname_id  INT                NOT NULL UNIQUE,
    pw           VARCHAR(255)       NOT NULL,
    nickname     VARCHAR(255)       NOT NULL UNIQUE,
    email        VARCHAR(255)       NULL,
    bias         INT                NOT NULL DEFAULT 0,
    break        INT                NOT NULL DEFAULT 4
);

CREATE TABLE Names (
  id         INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  surname    VARCHAR(255)     NOT NULL,
  famname    VARCHAR(255)     NOT NULL,
  registered BOOLEAN          NULL DEFAULT 0,
  helper     BOOLEAN          NOT NULL DEFAULT 0
);

CREATE TABLE Helpers (
  id           INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  fullname_id  INT                NOT NULL UNIQUE,
  pw           VARCHAR(255)       NOT NULL,
  nickname     VARCHAR(255)       NOT NULL UNIQUE,
  email        VARCHAR(255)       NULL,
  ticketnumber INT                NULL UNIQUE,
  workload     INT                NOT NULL DEFAULT 4,
  break        INT                NOT NULL DEFAULT 4
);

CREATE TABLE Exlusives (
  id          INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
  jt_name     VARCHAR(255)       NOT NULL,
  fullname_id     INT            NOT NULL UNIQUE,
  user_id       INT              NULL UNIQUE
);
