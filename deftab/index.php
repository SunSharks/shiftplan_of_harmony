<?php
// Start the session
session_start();
$_SESSION["src"] = "../deftab/index.php";
if(!isset($_SESSION['user'])){
  header('Location: ../users/logout.php?src=../deftab/index.php');
  exit;
}
if (!empty($_GET)){
  if ($_GET["log"] === "out"){
    unset($_SESSION['user']);
    // printf(json_encode($_SESSION["user"]));
    header('Location: ../users/logout.php?src=../deftab/index.php&log=out');
    exit;
  }
}
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>schedule definition</title>
  <link rel="stylesheet" type="text/css" href="style.css">

  <!-- <script>
    const input = document.querySelector('input');
    const log = document.getElementById('values');
    input.addEventListener('input', updateValue);
    function updateValue(e) {
      log.textContent = e.target.value;
    }
  </script> -->

  <?php
  include("db.php");
  regain_integrity();
  $_SESSION["deleted"] = "none";
   ?>
  <script src=def.js></script>
</head>

<body>
  <div id="head_row" class="head_row">
    <a href="index.php?log=out">
      <button class="logbtn">logout</button>
    </a>
    <a href="edit_existing_jobs.php">
      <button class="logbtn">Bearbeiten bereits in der Datenbank befindlicher Schichten.</button>
    </a>
  </div>
  <h1>Definitionen</h1>
  <div id="definition">
    <form action="tab.php"  method="get">
      <div id="inform">
        <div class="day">
          <!-- Fetch predefined days. -->
          <?php
            $_SESSION["days"] = fetch_it(get_days_sql());
            $max_dayid = fetch_maxid("Days");
            foreach ($_SESSION["days"] as $d) {
              printf(get_daybox_html_readonly($d["id"], $d["name"], $d["date"]));
            }
            if (empty($_SESSION["days"])){
              $max_dayid = 0;
            }
          ?>
          <script> set_days(<?php echo json_encode($_SESSION["days"]).", ".$max_dayid; ?>);</script>
          <div id="add_day"><button id="add_day_btn" type="button" onclick="create_daybox();">+</button></div>
          <div id="del_day"><button id="del_day_btn" type="button" onclick="delete_daybox();">-</button><br></div>
        </div>

        <div id="job">
          <!-- Fetch predefined jobtypes. LANG!-->
          <br><h2>Schichten</h2><br>
          <div id="add_predef_jobs">
            <!-- LANG! -->
            <p>
            Folgende Schichten sind bereits in der Datenbank. <br>
          </p>
            <?php
              $jobtypes = fetch_it(get_jobtypes_sql());
              foreach ($jobtypes as $j) {
                printf(get_jobbox_html($j["id"], $j["name"], $j["helper"], $j["competences"], $j["special"]));
              }
            ?>
            <script>
            set_jobs(<?php echo json_encode($jobtypes); ?>);
            console.log(<?php echo json_encode($jobtypes); ?>);
            </script>
          </div>
          <div id="add_job">
            <!-- LANG! -->
            <p>Klicke auf den Button "Neue Tätigkeit", um ein Eingabefeld für die neue Tätigkeit erscheinen zu lassen.
                In das Textfeld gib bitte den Namen der Schicht ein. Setze einen Haken in die entsprechende Checkbox, falls die neue Schicht für Helfende bzw. sensibel ist. </p>
            <button id="add_job_btn" type="button" onclick="create_jobbox();">Neue Tätigkeit</button>
            <!-- <br> -->
            <!-- <div id="new_j"></div> -->
          </div>
        </div>
        <div id="submitdiv">
          <p>
            <!-- <input name="show_only_new_jobs" type="checkbox" value="true">Show only new -->
            <input id="submitdivbtn" type="submit" value="Bestätigen und zur Schichttabelle.">
          </p>
        </div>
      </div>
    </form>
  </div>
  <div id="prio_link">
    <a href="../crew_prios/index.php">
      <button class="logbtn">Zur Präferenzeneingabe. </button>
    </a>
  </div>
  <div class="enddiv">
  </div>

  <?php
  $_SESSION["days_indb"] = false;
  $_SESSION["jts_indb"] = false;
  $_SESSION["jobs_indb"] = false;
  if ($_SESSION["deleted"] === false){
    $_SESSION["days_indb"] = true;
    $_SESSION["jts_indb"] = true;
    $_SESSION["jobs_indb"] = true;
  }
  ?>

</body>

</html>
