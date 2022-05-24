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
    $days = fetch_it(get_days_sql());
    $_SESSION['num_days'] = count($days);
    $_SESSION["view_days"] = $days;
  ?>

  <script src="./p5/p5.min.js"></script>
  <script src=deftabsketch.js></script>
  <script> set_deletion_mode(); </script>
  <script> make_day_instances(<?php echo json_encode($_SESSION["view_days"]); ?>); </script>


  <?php
    $jobs = fetch_it(get_jobs_sql());
    $jsjobs = json_encode($jobs);
    $_SESSION["jobs"] = $jsjobs;
    echo "<script> insert_predefined_jobs($jsjobs);</script>";
    $jts = fetch_it(get_jobtypes_sql());
    $jsjobs = json_encode($jts);
    $_SESSION["jts"] = $jsjobs;
  ?>


  <script language="javascript">
  function insertarrayintohiddenformfield(){
    let deljobs = [];
    for (var [key, value] of jobtypes.entries()){
      console.log(jobtypes.get(key).delete);
      if (jobtypes.get(key).delete === true){
        deljobs.push(jobtypes.get(key).id);
      }
    }
    document.Form.deljobs.value = JSON.stringify(deljobs);
    console.log(JSON.stringify(deljobs));
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

  $djs = $_POST['deljobs'];
  if (isset($djs)){
    $djs = ltrim($djs, "[");
    $djs = rtrim($djs, "]");
    $deljobs = explode(",", $djs);
    $pdo = connect();
    for ($i=0; $i<count($deljobs); $i++){
      perform_query($pdo, delete_jobtype_sql(json_decode($deljobs[$i])));
    }
    $pdo = null;
    $_SESSION["deleted"] = true;
    unset($_POST['deljobs']);
    $jobs = fetch_it(get_jobs_sql());
    $jsjobs = json_encode($jobs);
    $_SESSION["jobs"] = $jsjobs;
    $jts = fetch_it(get_jobtypes_sql());
    $jsjobs = json_encode($jts);
    $_SESSION["jts"] = $jsjobs;
  }
  ?>

</head>

<body>
  <a href="./tab.php">Back to Table.</a>
  <div style='position:absolute;top:500px;left:450px'>
    <?php
    for ($i=0; $i<$_SESSION['num_days']; $i++){
      echo "<button type='button' onclick='create_dayview($i)'>DAY $i</button>";
    }
    ?>
    <button type="button" onclick="resume_default_view()">WHOLE VIEW</button>
  <form name="Form" method="post" onsubmit="insertarrayintohiddenformfield()" action="delete_jobtype.php">
    <input name="deljobs" type=hidden>
    <input name="DELETE" type="submit" value="DELETE">
  </form>
  </div>
  <?php
    $_SESSION["jobs"] = json_encode(fetch_it(get_jobs_sql()));
    $d_s = json_encode($_SESSION["days"]);
    $jt_s = $_SESSION["jts"];
    $j_s = $_SESSION["jobs"];
    echo "<script>set_post_request_mode();</script>";
    echo "<script>get_params_readonly($d_s, $jt_s, $j_s);</script>";
    echo "<script>unset_edit_mode();</script>";
  ?>
  <main>
  </main>


</body>
</html>
