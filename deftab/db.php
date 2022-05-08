<?php
// (A) SETTINGS - CHANGE TO YOUR OWN !
error_reporting(E_ALL & ~E_NOTICE);
define("DB_HOST", "localhost");
define("DB_NAME", "Testplan");
define("DB_CHARSET", "utf8");
define("DB_USER", "root");
define("DB_PASSWORD", "");

function get_days(){
  return "SELECT * FROM Days";
}

function get_job_names(){
  return "SELECT * FROM `Jobs`";
}

function get_jobs(){

}

function insert_day($day){
  return "INSERT INTO `Days` (name) VALUES ($day)";
}

function insert_job($job){
  return "INSERT INTO `Jobs` (name) VALUES ($job)";
}

// (B) CONNECT TO DATABASE
try {
  $pdo = new PDO(
    "mysql:host=" . DB_HOST . ";charset=" . DB_CHARSET . ";dbname=" . DB_NAME,
    DB_USER, DB_PASSWORD
  );
} catch (Exception $ex) { exit($ex->getMessage()); }

// (C) GET USERS
$sql = get_days();//"INSERT INTO Days (name) VALUES ('Mittwoch')";
try{
  $stmt = $pdo->prepare($sql);
  $stmt->execute();
  $users = $stmt->fetchAll();
  foreach ($users as $u) {
    printf("<div>[%s] %s</div>", $u['name'], $u['start']);
  }
} catch(PDOException $e) {
  echo $sql . "<br>" . $e->getMessage();
}
// echo "yea";

// (D) CLOSE DATABASE CONNECTION
$pdo = null;
$stmt = null;
