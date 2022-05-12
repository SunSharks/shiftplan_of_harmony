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
  <script src="./p5/p5.min.js"></script>
 <!-- <script src="./p5/addons/p5.sound.js"></script> -->
  <!-- <script defer src=https://cdn.JsDelivr.net/npm/p5></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.dom.min.js></script>
  <script defer src=https://cdn.JsDelivr.net/npm/p5/lib/addons/p5.sound.min.js></script> -->
  <script src=deftabsketch.js></script>
  <script language="javascript">
  function insertarrayintohiddenformfield(){
    let job_values = [];
    let jt_values = [];
    for (var [key, value] of jobtypes.entries()){
      jt_values.push(JSON.stringify(value));
      console.log(jt_values);
    }
    for (let i=0; i<job_instances.length; i++){
      job_values.push(JSON.stringify(job_instances[i]));
    }
    console.log(job_values);
    console.log(jt_values);
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
    echo "postval";
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

  // echo count($vals);
  $jtar = $_POST['jobtypes'];
  if (isset($jtar)){
    $jtvals = process_postval($jtar);
    for ($i=0; $i<count($jtvals); $i++){
      $jobsql = insert_jobtype_sql($jtvals[$i]);
      // echo $jobsql;
      if ($jobsql != ""){
        $pdo = connect();
        perform_query($pdo, $jobsql);
        $pdo = null;
      }
    }
  }

  $jar = $_POST['jobs'];
  if (isset($jar)){
    $jvals = process_postval($jar);
    for ($i=0; $i<count($jvals); $i++){
      $jobsql2 = insert_job_sql($jvals[$i]);
      // echo $jobsql;
      if ($jobsql2 != ""){
        $pdo2 = connect();
        perform_query($pdo2, $jobsql2);
      }
    }
  }


  echo "----_______----";

  ?>

</head>

<body>
  <a href="./index.php">Back to definitions</a>
  <div style='position:absolute;top:500px;left:450px'>
  <form name="Form" method="post" onsubmit="insertarrayintohiddenformfield()" action="tab.php">
  <input name='jobs' type=hidden>
  <input name='jobtypes' type=hidden>
  <input name="INSERT INTO DB" type="submit" value="INSERT INTO DB">

  </form>
  </div>

  <main>
  </main>

</body>
</html>
