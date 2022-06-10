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
?>
</body>
</html>
