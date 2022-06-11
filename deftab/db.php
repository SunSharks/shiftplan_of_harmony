<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
<?php
include("../db/db_base.php");
$day_order = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"];
$day_cnt = 0;
// $days = [];
$job_cnt = 0;

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
  return "SELECT id, name, helper, special, competences FROM Jobtypes";
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
  $user_id = $_SESSION["user"]["id"];
  $pdo = connect();
  $sql = get_jobtype_id_sql($jt->id);
  // echo "$sql";
  $jt_indb = perform_query($pdo, $sql);
  if (sizeof($jt_indb) > 0){
    return "";
  }
  $n = repair_umlauts(recover_umlauts(utf8_encode(rawurlencode($jt->name))));
  if ($jt->special == 1){
    $spec = "true";
  }
  else{
    $spec = "false";
  }
  if ($jt->helper == 1){
    return "INSERT INTO Jobtypes (name, helper, special, user_id) VALUES ('$n', true, $spec, $user_id)";
  }
  else{
    return "INSERT INTO Jobtypes (name, helper, special, user_id) VALUES ('$n', false, $spec,  $user_id)";
  }
}

function insert_infotext_sql($text, $id){
  return "UPDATE Jobtypes SET competences = '$text' WHERE id=$id";
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

function get_jobbox_html($id, $jobname, $helper, $infotext, $special){
  if ($helper){
    $checked = "checked";
    $helper = "Helper";
    $style = "style='background:rgb(188, 100, 153)'";
    $divstyle = ";border:2px solid #e2001e;border-radius:5px";
  }
  else{
    $checked = "";
    $helper = "";
    $style = "";
    $divstyle = "";
  }
  if ($special){
    $special = "sensibel";
    $specialchecked = "checked";
    $specialstyle = "";
  }
  else{
    $special = "";
    $specialchecked = "";
    $specialstyle = "";
  }
  $html = "<div class='outerjobbox' title='$infotext' style='height:fit-content;margin:8px;padding:8px'>
<p id='jobpar'>
<div id='jobbox$id' class='jobbox'>
<input type='text' name='job$id' id='job$id' accept-charset='utf-8' value='$jobname' readonly></div>
<div class='jobbox'>
<input type='checkbox' class='jobbox' id='helper$id' name='helper$id' onclick='return false;' value='helper$id' $checked></div>
<div class='jobbox'>
<label for='checkbox' $style name='helper_label$id' onclick='return false;' id='cb_label$id'>$helper</label></div>
<div class='jobbox'>
<input type='checkbox' class='jobbox' id='special$id' name='special$id' onclick='return false;' value='special$id' $specialchecked></div>
<div class='jobbox'>
<label for='checkbox' $specialstyle name='special_label$id' onclick='return false;' id='cb_label$id'>$special</label></div>
<div class='jobbox'>
<input name='PREjob$id' type=hidden></div></p></div>";
  $job_cnt++;
  return $html;
}
?>
</body>
</html>
