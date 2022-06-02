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
// echo "yea";
$day_cnt = 0;
// $days = [];
$job_cnt = 0;

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

// $s = rawurlencode('ärger');
// printf(repair_umlauts($s));


function regain_integrity(){
  $pdo = connect();
  $sql = "DELETE FROM Jobs WHERE jt_primary NOT IN (SELECT id FROM Jobtypes);";

  perform_query($pdo, $sql);
  $sql = "DELETE FROM Jobs WHERE start_day_id NOT IN (SELECT id FROM Days);";
  perform_query($pdo, $sql);
  $sql = "DELETE FROM Jobs WHERE end_day_id NOT IN (SELECT id FROM Days);";
  perform_query($pdo, $sql);
  $pdo = null;
}

function get_names_sql(){
  return "SELECT * from Names";
}

function get_name_id_sql($name){
  $surname = explode(" ", $name)[0];
  $famname = explode(" ", $name)[1];
  return "SELECT id from Names WHERE Names.surname = '$surname' AND Names.famname = '$famname'";
}

function get_registered_name_ids_sql(){
  return "SELECT id FROM Names WHERE registered = true";
}

function get_nicknames_sql(){
  return "SELECT nickname from Users";
}

function get_users_sql(){
  return "SELECT * FROM Users";
}



function insert_user_sql($name, $pw, $nickname, $email){
  $name_id = fetch_it(get_name_id_sql($name))[0]["id"];
  $registered_ids = fetch_it(get_registered_name_ids_sql());
  for ($i=0; $i<count($registered_ids); $i++){
    if ($registered_ids[$i]["id"] === $name_id){
      return "INDB";
    }
  }
  $hash = password_hash($pw, PASSWORD_DEFAULT);
  $ret = "";
  if (empty($email)){
    $ret = $ret . "INSERT INTO Users (fullname_id, pw, nickname) VALUES ($name_id, '$hash', '$nickname')";
  }
  else{
    $ret = $ret . "INSERT INTO Users (fullname_id, pw, nickname, email) VALUES ($name_id, '$hash', '$nickname', '$email')";
  }
  $ret = $ret . ";" . set_name_registered_sql($name_id);
  return $ret;
}
// INSERT INTO Users (fullname_id, pw, nickname, email) SELECT id, "bla", "downlord", "la@bla.py" FROM Names WHERE Names.surname="Lysanne";

function set_name_registered_sql($name_id){
  return "UPDATE Names SET registered = true WHERE Names.id=$name_id";
}
function get_days_sql(){
  $ret = "SELECT * FROM Days ORDER BY date ASC";
  return $ret;
}

function get_jobtypes_sql(){
  return "SELECT id, name, special FROM Jobtypes";
}

function get_jobtype_id_sql($id){
  return "SELECT id FROM Jobtypes WHERE id = $id";
}

function get_jobs_sql(){
  return "SELECT id, abs_start, abs_end, during, start_day_id, end_day_id, dt_start, dt_end, jt_primary FROM Jobs";
}

function get_job_id_sql($id){
  // echo "<br> $id <br>";
  return "SELECT id FROM Jobs WHERE id = $id";
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

function get_jobtype_jobs_sql($id){
  return "SELECT * FROM Jobs WHERE jt_primary = $id ORDER BY abs_start ASC";
}

function fetch_jobtype_jobs($id){
  $pdo = connect();
  $sql = get_jobtype_jobs_sql($id);
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

// function disconnect(){
//     // CLOSE DATABASE CONNECTION
//     $pdo = null;
//     $stmt = null;
// }

function perform_query($pdo, $sql){
  // echo $sql;
  // echo "<br> ___";
  try{
    $stmts = $pdo->prepare('SET NAMES utf8');
    $stmts->execute();
    $stmt = $pdo->prepare($sql);
    $stmt->execute();
    $res = $stmt->fetchAll();
    $pdo = null;
    $stmt = null;
    $stmts = null;
    return $res;
    // foreach ($res as $u) {
    //   printf("<div>[%s] %s</div>", $u['name'], $u['start']);
    // }
  } catch(PDOException $e) {
    echo $sql . "<br>" . $e->getMessage();
  }
}


?>
</body>
</html>
