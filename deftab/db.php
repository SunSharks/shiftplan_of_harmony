


<?php
// (A) SETTINGS - CHANGE TO YOUR OWN !
error_reporting(E_ALL & ~E_NOTICE);
define("DB_HOST", "localhost");
define("DB_NAME", "Testplan");
define("DB_CHARSET", "utf8");
define("DB_USER", "root");
define("DB_PASSWORD", "");
// echo "yea";
$day_order = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"];
$day_cnt = 0;
// $days = [];
$job_cnt = 0;

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

function get_days_sql(){
  $ret = "SELECT * FROM Days ORDER BY date ASC";
  return $ret;
}

function insert_day_sql($day){
  if ($day->indb == 1){
    return "";
  }
  if ($day->name == null){
    $ret = "INSERT INTO Days (date) VALUES ('$day->date')";
  }
  else{
    $ret = "INSERT INTO Days (date, name) VALUES ('$day->date', '$day->name')";
  }
  return $ret;
}

function delete_day_sql($day_id){
  return "DELETE FROM Days WHERE id = $day_id";
}

function get_jobtypes_sql(){
  return "SELECT id, name, special FROM Jobtypes";
}

function get_jobtype_id_sql($id){
  return "SELECT id FROM Jobtypes WHERE id = $id";
}

function insert_jobtype_sql($jt){
  // echo $jt->name;
  // echo "<br>";
  if ($jt->indb == 1){
    // echo "indb";
    return "";
  }
  $pdo = connect();
  $sql = get_jobtype_id_sql($jt->id);
  // echo "$sql";
  $jt_indb = perform_query($pdo, $sql);
  if (sizeof($jt_indb) > 0){
    // printf("jaaas");
    return "";
  }

  if ($jt->special == 1){
    return "INSERT INTO Jobtypes (name, special) VALUES ('$jt->name', true)";
  }
  else{
    return "INSERT INTO Jobtypes (name, special) VALUES ('$jt->name', false)";
  }
}

function delete_jobtype_sql($jt_id){
  if ($jt_id === null){
    return "";
  }
  $ret = "DELETE FROM Jobtypes WHERE id = $jt_id;
  DELETE FROM Jobs WHERE jt_primary = $jt_id";
  return $ret;
}

function get_jobs_sql(){
  return "SELECT id, abs_start, abs_end, during, start_day_id, end_day_id, dt_start, dt_end, jt_primary FROM Jobs";
}

function get_job_id_sql($id){
  // echo "<br> $id <br>";
  return "SELECT id FROM Jobs WHERE id = $id";
}

function insert_job_sql($job_json){
  if ($job_json->indb == 1){
    // printf("<br> $job_json->indb in<br>")
    return "";
  }
  $pdo = connect();
  $sql = get_job_id_sql($job_json->id);
  $job_indb = perform_query($pdo, $sql);
  if (sizeof($job_indb) > 0){
    return "";
  }
    return "INSERT INTO Jobs (abs_start, abs_end, during, start_day_id, end_day_id, dt_start, dt_end, jt_primary) VALUES ($job_json->start, $job_json->end, $job_json->during, $job_json->start_day_id, $job_json->end_day_id, $job_json->dt_start, $job_json->dt_end, $job_json->jobtype_id)";
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

function get_daybox_html_readonly($id, $dayname, $date){
  $html = "<div id='daybox$id' class='daybox'>
  <div id='day_label$id' class='inner_daybox'>
  <label for='day$id'>$dayname</label>
  </div>
  <div id='day$id' class='inner_daybox'>
  <input type='date' name='PREday$id' id='day$id' value='$date' readonly>
  </div>
  </div>";
  return $html;
}

function get_daybox_html($id){
  $html = "<div id='daybox$id' class='daybox'> <input type='text' name='day$id' id='day$id' value=''></div> ";
  return $html;
}

function insert_daybox_html($id){
  $html = get_daybox_html($id);
  $day_cnt++;
  // printf($html);
}

function get_jobbox_html($id, $jobname, $special){
  if ($special){
    $checked = "checked";
    $helper = "Helper";
    $style = "style='background:rgb(188, 100, 153)'";
  }
  else{
    $checked = "";
    $helper = "";
    $style = "";
  }
  $html = "<div class='outerjobbox'>
<div id='jobbox$id' class='jobbox'>
<input type='text' name='job$id' id='job$id' value='$jobname' readonly></div>
<div class='jobbox'>
<input type='checkbox' class='jobbox' id='special$id' name='special$id' onclick='return false;' value='special$id' $checked></div>
<div class='jobbox'>
<label for='checkbox' $style name='cb_label$id' onclick='return false;' id='cb_label$id'>$helper</label></div>
<div class='jobbox'>
<input name='PREjob$id' type=hidden></div></div>";
  $job_cnt++;
  return $html;
}
?>
