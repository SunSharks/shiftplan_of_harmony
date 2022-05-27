<?php
// Start the session
session_start();
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>schedule definition</title>
  <link rel="stylesheet" type="text/css" href="tabstyle.css">

  <?php
  include("db.php");
  regain_integrity();
   ?>

  <script language="javascript">
  function insertarrayintohiddenformfield(){
    let day_values = [];
    let job_values = [];
    let jt_values = [];
    save_data();
    for (let i=0; i<days_arr.length; i++){
      day_values.push(JSON.stringify(days_arr[i]));
    }
    for (var [key, value] of jobtypes.entries()){
      jt_values.push(JSON.stringify(value));
    }
    for (let i=0; i<job_instances.length; i++){
      job_values.push(JSON.stringify(job_instances[i]));
    }
    console.log(job_values);
    console.log(job_instances);
    document.Form.days.value = day_values;
    document.Form.jobtypes.value = jt_values;
    document.Form.jobs.value = job_values;
  }
  </script>

  <script src="./p5/p5.min.js"></script>
  <script src=deftabsketch.js></script>
  <script> unset_deletion_mode(); </script>

  <?php
  $tage = array('Sonntag','Montag','Dienstag','Mittwoch','Donnerstag','Freitag','Samstag');
  $monate = array('','Januar','Februar','März','April','Mai','Juni','Juli','August','September','Oktober','November','Dezember');
  ?>
  <?php
  if (!empty($_GET)){
    $days = [];
    $new_days = [];
    foreach($_GET as $key=>$val){
      if (str_starts_with($key, "day")){
        $tmp = array();
        $tmp["date"] = $val;
        $tmp["name"] = $tage[date("w", strtotime($val))];
        $tmp["id"] = substr($key, 3);
        array_push($days, $tmp);
        array_push($new_days, $tmp);
      }
      else if (str_starts_with($key, "PREday")){
        $tmp = array();
        $tmp["date"] = $val;
        $tmp["name"] = $tage[date("w", strtotime($val))];
        $tmp["id"] = substr($key, 6);
        // echo $tmp["name"];
        array_push($days, $tmp);
      }
    }
    $_SESSION["new_days"] = $new_days;
    $_SESSION["days"] = $days;
  }
  else{
    $days = fetch_it(get_days_sql());
    $_SESSION['days'] = $days;
  }
  ?>

  <script> make_day_instances(<?php echo json_encode($new_days); ?>); </script>


  <?php
    $jobs = fetch_it(get_jobs_sql());
    $jsjobs = json_encode($jobs);
    $_SESSION["jobs"] = $jsjobs;
    echo "<script> insert_predefined_jobs($jsjobs);</script>";
  ?>





<?php
// // WARNINGS
// ini_set('display_errors', 1);
// ini_set('display_startup_errors', 1);
// error_reporting(E_ALL);

  function process_postval($postar){
    $js = explode("}", $postar);
    $vals = [];
    if (isset($postar)){
      // echo count($js);
      for ($i=0;$i<count($js);$i++){
        $j = json_encode(utf8_encode($js[$i]));
        if (str_ends_with($j, '"') || str_ends_with($j, '"')){
          $j = substr($j, 0, -1);
        }
        if ($j[0] == '"'){
          $j = ltrim($j, '"');
        }
        if ($j[0] == ','){
          $j = ltrim($j, ',');
        }
        if ($j == ""){
          break;
        }
        $j = $j."}";
        $j = json_decode(stripslashes($j));
        array_push($vals, $j);
      }
      return $vals;
    }
  }

    $dayar = $_POST['days'];
    if (isset($dayar) && !$_SESSION["days_indb"]){
      $days = array();
      $dayvals = process_postval($dayar);
      for ($i=0; $i<count($dayvals); $i++){
        $daysql = insert_day_sql($dayvals[$i]);
        if ($daysql != ""){
          // echo "<br".$daysql;
          $pdo = connect();
          perform_query($pdo, $daysql);
          $pdo = null;
          $d = json_encode($dayvals[$i]);
          array_push($days, $dayvals[$i]->date);
          echo $dayvals[$i]->date;
          // echo "<script>insert_day_indb($d);</script>";
        }
      }
      $days = fetch_it(get_days_sql());
      $_SESSION['days'] = $days;
      $_SESSION["days_indb"] = true;
      unset($_POST['days']);
    }

    // echo count($vals);
    $jtar = $_POST['jobtypes'];
    if (isset($jtar) && !$_SESSION["jts_indb"]){
      $jtvals = process_postval($jtar);
      $jt_names = array();
      for ($i=0; $i<count($jtvals); $i++){
        $jobsql = insert_jobtype_sql($jtvals[$i]);
        $jt_names[$jtvals[$i]->name] = $jtvals[$i];
        if ($jobsql != ""){
          $pdo = connect();
          perform_query($pdo, $jobsql);
          $pdo = null;
          $d = json_encode($jtvals[$i]);
        }
      }
      $_SESSION["jts_indb"] = true;
      $_SESSION["jts"] = $jtvals;
      unset($_POST['jobtypes']);
    }

    $jar = $_POST['jobs'];
    if (isset($jar) && !$_SESSION["jobs_indb"]){
      $jvals = process_postval($jar);
      for ($i=0; $i<count($jvals); $i++){
        $jobsql2 = insert_job_sql($jvals[$i]);
        if ($jobsql2 != ""){
          $pdo2 = connect();
          perform_query($pdo2, $jobsql2);
          $d = json_encode($jvals[$i]);
          // printf($jobsql2);
        }
      }
      $_SESSION["jobs_indb"] = true;
      unset($_POST['jobs']);
    }
  ?>

</head>

<body>
  <div style='position:absolute;top:0px;left:0px'>
    <p>
    <div id="daybtns" style='position:absolute;top:0px;left:0px'>
      <button id="wholeviewbtn" type="button" onclick="resume_default_view()">WHOLE VIEW</button>
      <?php
      for ($i=0; $i<count($_SESSION['days']); $i++){
        $in = $_SESSION["days"][$i]["name"]."<br>".$_SESSION["days"][$i]["date"];
        echo "<button class=daybtn id=daybtn$i type='button' onclick='create_dayview($i)'>$in</button>";
      }
      ?>
  </div>
  </p>
  <div style='position:absolute;top:0px;left:0px;width:90px'>
  <a href="./index.php">Back to definitions</a>
  <?php
  if ($_SESSION["jobs_indb"] || (empty($_GET) && empty($_POST))){
    echo "Geschafft.";
    $_SESSION["jobs"] = json_encode(fetch_it(get_jobs_sql()));
    $d_s = json_encode($_SESSION["days"]);
    $jt_s = json_encode($_SESSION["jts"]);
    $j_s = $_SESSION["jobs"];
    echo "<script>set_post_request_mode();</script>";
    echo "<script>get_params_readonly($d_s, $jt_s, $j_s);</script>";
    echo "<script>unset_edit_mode();</script>";
  }
  ?>
</div>
  <br><br><br>
  <div id="p5tab"></div>
    <main>
    </main>
    <div id="insertform">
      <form name="Form" method="post" onsubmit="insertarrayintohiddenformfield()" action="tab.php">
        <input name='days' type=hidden>
        <input name='jobs' type=hidden>
        <input name='jobtypes' type=hidden>
        <input id="insertbtn" name="INSERT INTO DB" type="submit" onclick="return confirm('Deine Eingaben werden nun gespeichert.Bist du sicher, dass alle Eingaben korrekt sind?')" value="INSERT INTO DB">
      </form>
    </div>
    <div id="delete_link_div">
      <a href="./delete_jobtype.php" id="delete_link">Delete a Jobtype</a>
    </div>
</div>
<!-- <br> -->
<!-- <p>
<div>

</div>
</p> -->
</body>
</html>
