<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
<?php
// (A) SETTINGS - CHANGE TO YOUR OWN !
error_reporting(E_ALL & ~E_NOTICE);
define("DB_HOST", "localhost");
define("DB_NAME", "Testplan");
define("DB_CHARSET", "utf8");
define("DB_USER", "root");
define("DB_PASSWORD", "");



// =============================================================================
// REPAIR UTF8 - ENCODING (brute force and ugly.)
function repair_umlauts($s){
  $umlaute = array('%C3%A4', '%C3%B6', '%C3%BC', '%C3%9F', '%C3%84', '%C3%96', '%C3%9C', '%20');
  $ersetze = array('ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü', " ");
  return str_replace($umlaute, $ersetze, $s);
}

function recover_umlauts($s, $bef=""){
  $umlaute = array('u00e4', 'u00f6', 'u00fc', 'u00df', 'u00c4', 'u00d6', 'u00dc');
  if ($bef != ""){
    for ($i=0; $i<count($umlaute); $i++){
      $umlaute[$i] = $bef.$umlaute[$i];
    }
  }
  $ersetze = array('ä', 'ö', 'ü', 'ß', 'Ä', 'Ö', 'Ü');
  return str_replace($umlaute, $ersetze, $s);
}


// =============================================================================
// REGAIN INTEGRITY OF DB TABLES.
function regain_integrity(){
  /* Regain integrity of Jobs and Days.
  - Deletes Jobs from table Jobs, if it's jt_primary is not in Jobtypes.
  - Deletes Jobs from table Jobs, if it's start_day_id or end_day_id is not in Days.
  */
  $pdo = connect();
  $sql = "DELETE FROM Jobs WHERE jt_primary NOT IN (SELECT id FROM Jobtypes);";

  perform_query($pdo, $sql);
  $sql = "DELETE FROM Jobs WHERE start_day_id NOT IN (SELECT id FROM Days);";
  perform_query($pdo, $sql);
  $sql = "DELETE FROM Jobs WHERE end_day_id NOT IN (SELECT id FROM Days);";
  perform_query($pdo, $sql);
  $pdo = null;
}

function regain_preference_integrity(){
  /* Regain integrity of Jobs and Preferences.
  - Adds Column job$id for every new job in table Jobs.
  - Drops Column job$id if that id is not in Jobs.
  */
  $job_ids = unpack_singleton_fetch(fetch_it("SELECT id from Jobs"));
  if ($job_ids === -1){
    return;
  }
  $prefcols = unpack_singleton_fetch(fetch_it("SELECT COLUMN_NAME FROM INFORMATION_SCHEMA.COLUMNS WHERE TABLE_NAME = N'Preferences'"));
  $pref_cols = [];

  for ($i=1; $i<count($prefcols); $i++){
    array_push($pref_cols, substr($prefcols[$i], 3));
  }
  $new_jobs = array_values(array_diff($job_ids, $pref_cols));
  $del_jobs = array_values(array_diff($pref_cols, $job_ids));
  // printf(json_encode($job_ids));
  // printf("--------\r\n");
  // printf(json_encode($pref_cols));
  // printf("\n--------\r\n");
  // printf(json_encode($new_jobs));
  // printf("--------\r\n");
  // printf(json_encode($del_jobs));
  $sql = "";
  for ($i=0; $i<count($del_jobs); $i++){
    $sql = $sql . "ALTER TABLE Preferences DROP COLUMN job$del_jobs[$i];
    ";
  }
  for ($i=0; $i<count($new_jobs); $i++){
    // check if jobtype special or not
    $sql = $sql . "
    " . add_job_to_preferences_sql($new_jobs[$i]) . ";
    ";
  }
  // printf($sql);
  if ($sql != ""){
    $pdo = connect();
    perform_query($pdo, $sql);
    $pdo = null;
  }
}


function add_job_to_preferences_sql($id){
  $jtid = unpack_singleton_fetch(perform("SELECT jt_primary FROM Jobs WHERE id=$id;"))[0];
  // printf(json_encode(fetch_it("SELECT COUNT(id) FROM Jobtypes WHERE id=$jtid AND special=1;")[0]["COUNT(id)"]));
  if (fetch_it("SELECT COUNT(id) FROM Jobtypes WHERE id=$jtid AND special=1;")[0]["COUNT(id)"] === 1){
    return "ALTER TABLE Preferences ADD job$id INT NOT NULL DEFAULT 5";
  }
  return "ALTER TABLE Preferences ADD job$id INT NOT NULL DEFAULT 3";
}

function fetch_it($sql){
  $pdo = connect();
  $sql_ret = perform_query($pdo, $sql);
  $pdo = null;
  $vals = [];
  foreach ($sql_ret as $s){
    $tmp = array();
    foreach ($s as $key=>$val){
      if (strlen($key) > 1){
        $tmp[$key] = $val;
      }
    }
    array_push($vals, $tmp);
  }
  return $vals;
}

function get_table_maxid_sql($table){
  return "SELECT MAX(id) FROM $table";
}

function fetch_maxid($table){
  $pdo = connect();
  $sql = get_table_maxid_sql($table);
  $ret = perform_query($pdo, $sql);
  $ret = $ret[0]["MAX(id)"];
  return $ret;
}

function perform($sql){
  $pdo = connect();
  $ret = perform_query($pdo, $sql);
  $pdo = null;
  return $ret;
}

function connect(){
  // CONNECT TO DATABASE
  try {
    $pdo = new PDO(
      "mysql:host=" . DB_HOST . ";charset=" . DB_CHARSET . ";dbname=" . DB_NAME,
      DB_USER, DB_PASSWORD
    );
  } catch (Exception $ex) { exit($ex->getMessage()); }
  return $pdo;
}

function perform_query($pdo, $sql){
  // echo $sql;
  // echo "<br> ___";
  try{
    $stmts = $pdo->prepare('SET NAMES utf8');
    $stmts->execute();
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $res = $stmt->fetchAll();
    return $res;
    // foreach ($res as $u) {
    //   printf("<div>[%s] %s</div>", $u['name'], $u['start']);
    // }
  } catch(PDOException $e) {
    echo $sql . "<br>" . $e->getMessage();
  }
}

function get_min_jobduring_sql(){
  return "SELECT MAX(during) FROM Jobs";
}

?>
</body>
</html>
