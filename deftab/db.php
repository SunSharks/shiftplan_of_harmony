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

function get_days_sql(){
  return "SELECT * FROM Days";
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

function insert_jobtype_sql($jt){
  // echo $jt->name;
  // echo "<br>";
  if ($jt->indb == 1){
    // echo "indb";
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
  $ret = "DELETE FROM Jobtypes WHERE id = $jt_id;
  DELETE FROM Jobs WHERE jt_primary = $jt_id";
  return $ret;
}

function get_jobs_sql(){
  return "SELECT id, abs_start, abs_end, during, start_day_id, end_day_id, dt_start, dt_end, jt_primary FROM Jobs";
}

function insert_job_sql($job_json){
  if ($jt->indb == 1){
    return "";
  }
    return "INSERT INTO Jobs (abs_start, abs_end, during, start_day_id, end_day_id, dt_start, dt_end, jt_primary) VALUES ($job_json->start, $job_json->end, $job_json->during, $job_json->start_day_id, $job_json->end_day_id, $job_json->dt_start, $job_json->dt_end, $job_json->jobtype_id)";
}



function test(){
  echo "testitest";
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
//   <label for="start">Start date:</label>
//
// <input type="date" id="start" name="trip-start"
//        value="2018-07-22"
//        min="2018-01-01" max="2018-12-31">
  // $html = "<div id='daybox$id' class='daybox'>
  // <input type='text' name='day$id' id='day$id' value='$dayname' readonly>
  // <br>
  // <input type='date' name='date$id' id='date$id' value='$date'>
  // </div>";
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
  printf($html);
}

function get_jobbox_html($id, $jobname, $special){
  if ($special){
    $checked = "checked";
  }
  else{
    $checked = "";
  }
  $html = "<div id='jobbox$id' class='jobbox'>
<label for='checkbox' name='cb_label$id' id='cb_label$id'>Helper</label>
<input type='checkbox' class='jobbox' id='special$id' name='special$id' value='special$id' $checked>
<input name='PREjob$id' type=hidden>
<input type='text' name='job$id' id='job$id' value='$jobname' readonly></div> ";
  $job_cnt++;
  return $html;
}
?>
