<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
<?php
if (!function_exists('str_starts_with')) {
  function str_starts_with($str, $start) {
    return (@substr_compare($str, $start, 0, strlen($start))==0);
  }
}
include("../db/db_base.php");

error_reporting(-1); // reports all errors
ini_set("display_errors", "1"); // shows all errors
ini_set("log_errors", 1);
ini_set("error_log", "php-error.log");

// echo json_encode(unpack_singleton_fetch(perform("SELECT COUNT(id) FROM Jobtypes WHERE id=1 AND special=1;SELECT COUNT(id) FROM Jobtypes WHERE id=2 AND special=1;"))[0]);
// echo "___";
// echo json_encode(unpack_singleton_fetch(perform("SELECT COUNT(id) FROM Jobtypes WHERE id=2 AND special=1;"))[0]);

// =============================================================================
// Functions, that return SQL-statements as strings.
function get_days_sql(){
  $ret = "SELECT * FROM Days ORDER BY date ASC";
  return $ret;
}

function get_jobtypes_sql($helper='all'){
  if ($helper === 'all'){
    return "SELECT id, name, helper, special, competences FROM Jobtypes";
  }
  else if ($helper === 'true'){
    return "SELECT id, name, helper, special, competences FROM Jobtypes WHERE helper=1";
  }
  else if ($helper === 'false'){
    return "SELECT id, name, helper, special, competences FROM Jobtypes WHERE helper=0";
  }
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

function create_preferences_table_sql($drop="DROP TABLE Preferences;"){
  // CREATE TABLE TBL_CD( CDnr int, CDTitel varchar(80) NOT NULL, CDduur int, CDprijs varchar(255) check( CDprijs > 0 and CDprijs < 6) )
  $job_ids = unpack_singleton_fetch(fetch_it("SELECT id from Jobs"));
  if ($job_ids === -1){
    printf("No Jobs defined.");
    return;
  }
  $ret = $drop . 'CREATE TABLE IF NOT EXISTS'.' Preferences (
    name_id INT NOT NULL PRIMARY KEY';
  for ($i=0; $i<count($job_ids); $i++){
    // TODO!
    if(unpack_singleton_fetch(perform("SELECT COUNT(id) FROM Jobtypes WHERE id=$job_ids[$i] AND special=1;"))[0] === "1"){
      $def = 5;
    }
    else{
      $def = 3;
    }
    $ret = $ret . ",
    job$job_ids[$i] INT NOT NULL DEFAULT $def check( job$job_ids[$i] > 0 and job$job_ids[$i] < 6)
    ";
  }
  $ret .= ");";
  $ret .= "INSERT INTO Preferences (name_id) SELECT id FROM Names WHERE Names.registered = 1;";
  // printf($ret);
  return $ret;
}

function get_names_sql(){
  return "SELECT * from Names";
}

function get_name_id_sql($name){
  $surname = explode(" ", $name, 2)[0];
  $famname = explode(" ", $name, 2)[1];
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

function insert_user_sql($name, $pw, $nickname){
  $name_id = fetch_it(get_name_id_sql($name))[0]["id"];
  $registered_ids = fetch_it(get_registered_name_ids_sql());
  for ($i=0; $i<count($registered_ids); $i++){
    if ($registered_ids[$i]["id"] === $name_id){
      return "INDB";
    }
  }
  $hash = password_hash($pw, PASSWORD_DEFAULT);
  $ret = "";
  $ret = $ret . "INSERT INTO Users (fullname_id, pw, nickname) VALUES ($name_id, '$hash', '$nickname')";
  $ret = $ret . ";" . set_name_registered_sql($name_id);
  $ret = $ret . ";" . initial_prio_insert_sql($name_id);
  return $ret;
}
// INSERT INTO Users (fullname_id, pw, nickname, email) SELECT id, "bla", "downlord", "la@bla.py" FROM Names WHERE Names.surname="Lysanne";

function set_name_registered_sql($name_id){
  return "UPDATE Names SET registered = true WHERE Names.id=$name_id";
}

function initial_prio_insert_sql($name_id){
  return "INSERT INTO Preferences (name_id) VALUES ($name_id)";
}

function get_prios_sql($name_id){
  return "SELECT * FROM Preferences WHERE name_id = $name_id";
}

//
// INSERT INTO Preferences
// SELECT COLUMN_NAME
// FROM INFORMATION_SCHEMA.COLUMNS
// WHERE TABLE_NAME= 'Preferences' AND COLUMN_NAME LIKE 'job9%'
// AND DATA_TYPE = 'int'
// VALUES (1,2,3,4,5)
// ;

function insert_prios_sql($prioinps){
  $sql1 = "UPDATE Preferences SET ";
  $sql2 = " WHERE name_id = ";
  $breaksql = "UPDATE Users SET break = ";
  $endsql = ";";

  // $userid = unpack_singleton_fetch(get_name_id())[0];
  // $prioinps["username"] = $userid;
  // echo json_encode($prioinps);
  foreach ($prioinps as $key=>$val){
    // echo "$key -> $val <br>";
    if ($key === "name_id"){
      // $sql1 .= " name_id = $val,";
      $sql2 .= "$val";
      $name_id = $val;
    }
    else if (str_starts_with($key, "prioinp")){
      $jobid = substr($key, 7);
      $sql1 .= " job$jobid = $val,";
    }
    else if (str_starts_with($key, "breakinp")){
      $breaksql .= $val;
    }
  }
  $breaksql .= " WHERE fullname_id = $name_id;";
  $sql1 = substr($sql1, 0, -1);
  $sql = $breaksql . $sql1 . $sql2 .  $endsql;
  // printf($sql);
  return $sql;
}

// =============================================================================
// Helper functions.
function unpack_singleton_fetch($fetch, $default='lst'){
  // $fetch = json_encode($fetch);
  // $regex = "id: |id:";
  // $rawstr = preg_grep($fetch);
  // printf(json_encode($fetch));
  // printf("unpack");
  if ($default === 'lst'){
    $out = [];
    for ($i=0; $i<count($fetch); $i++){
      foreach ($fetch[$i] as $key=>$val){
        array_push($out, $fetch[$i][$key]);
      }
    }
  }
  else{
    $out = array();
    for ($i=0; $i<count($fetch); $i++){
      foreach ($fetch[$i] as $key=>$val){
        $out["$key"] = $fetch[$i][$key];
      }
    }
    // printf("$default");
  }

  if (empty($out)){
    return -1;
  }
  return $out;
}

// ==============================
// Fetch functions.

function fetch_prios($name_id){
  $fetch = unpack_singleton_fetch(fetch_it(get_prios_sql($name_id)), 'arr');
  $ret = array();
  if ($fetch === -1){
    printf("No prios defined. ");
    return;
  }
  foreach ($fetch as $key=>$val){
    if ($key === "name_id"){
      unset($fetch[$key]);
      continue;
    }
    else{
      $new_key = substr($key, 3);
      $ret[$new_key] = $val;
    }
  }
  // printf(json_encode($ret));
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
?>
</body>
</html>
