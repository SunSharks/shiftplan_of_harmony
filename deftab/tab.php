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
  <style>
    body {
      padding: 0;
      margin: 0;
    }
    h1 {text-align: center;}
    p {text-align: center;}
    .daybox {
      display: inline;
      padding: 100;

    }
    .day {
      padding: 100;
      margin: 100;
    }

  </style>

  <?php include("db.php"); ?>

  <?php
  $num_days = 0;
  if (!empty($_GET)){
    $days = array();
    foreach($_GET as $key=>$val){
      if (str_starts_with($key, "day")){
        $days[substr($key, 3)] = $val;
        $num_days++;
      }
      else if (str_starts_with($key, "PREday")){
        $num_days++;
      }
      if (str_starts_with($key, "pleace_delete_py")){
        printf($val);
        // delete_jobtype_sql((int)$val);
      }
    }
    $_SESSION["dayvals"] = $days;
    $_SESSION['num_days'] = $num_days;
  }
  else{
    $pdo = connect();
    $days = perform_query($pdo, get_days_sql());
    $_SESSION['num_days'] = count($days);
    $pdo = null;
  }
  ?>

  <script src="./p5/p5.min.js"></script>
 <!-- <script src="./p5/addons/p5.sound.js"></script> -->
  <!-- <script defer src=https://cdn.JsDelivr.net/npm/p5></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.dom.min.js></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.sound.min.js></script> -->
  <script src=deftabsketch.js></script>
  <script> unset_deletion_mode(); </script>
  <script> make_day_instances(<?php echo json_encode($days); ?>); </script>


  <?php
    $jobs = fetch_jobs();
    $jsjobs = json_encode($jobs);
    $_SESSION["jobs"] = $jsjobs;
    echo "<script> insert_predefined_jobs($jsjobs);</script>";
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
      $num_days = 0;
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
        $num_days++;
      }
      $_SESSION["days_indb"] = true;
      $_SESSION["days"] = json_encode($dayvals);
      $_SESSION["dayvals"] = $days;
      $_SESSION['num_days'] = $num_days;
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
      $_SESSION["jts"] = json_encode($jtvals);
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
        }
      }
      $_SESSION["jobs_indb"] = true;
      unset($_POST['jobs']);
    }

    // $cmd = $_POST['magic_field'];
    // if (isset($cmd)){
    //   printf($cmd);
    //   printf($jt_names);
    //   if ($cmd === "DELETE THIS"){
    //     printf()
    //   }
    // }
  ?>

</head>

<body>
  <a href="./index.php">Back to definitions</a>
  <div style='position:absolute;top:500px;left:450px'>
    <?php
    for ($i=0; $i<$_SESSION['num_days']; $i++){
      echo "<button type='button' onclick='create_dayview($i)'>DAY $i</button>";
    }
    ?>
    <button type="button" onclick="resume_default_view()">WHOLE VIEW</button>
  <form name="Form" method="post" onsubmit="insertarrayintohiddenformfield()" action="tab.php">
    <input name='days' type=hidden>
    <input name='jobs' type=hidden>
    <input name='jobtypes' type=hidden>
    <input name="INSERT INTO DB" type="submit" value="INSERT INTO DB">
  </form>
  </div>
  <?php
  if ($_SESSION["jobs_indb"]){
    echo "Geschafft.";
    $_SESSION["jobs"] = json_encode(fetch_jobs());
    $d_s = $_SESSION["days"];
    $jt_s = $_SESSION["jts"];
    $j_s = $_SESSION["jobs"];
    echo "<script>set_post_request_mode();</script>";
    echo "<script>get_params_readonly($d_s, $jt_s, $j_s);</script>";
    // echo "<script> insert_predefined_jobs($jsjobs);</script>";
    echo "<script>unset_edit_mode();</script>";
  }
  // else{
  //   if ($_SESSION["deleted"] === true){
  //     echo "<script> insert_predefined_jobs($jsjobs);</script>";
  //   }
  // }
  ?>
  <main>
  </main>
  <a href="./delete_jobtype.php">Delete a Jobtype</a>

  <!-- <form name="magic" method="post" onsubmit=<?php proof_magic()?> action="tab.php">
    <input name='magic_field'>
    <input name="send magic" type="submit" value="send">
  </form> -->

</body>
</html>
