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
// =============================================================================
// Texts
$add_job_btn_txt = "Add new jobtype.";
$logout_txt = "logout";
$edit_existing_jobs_txt = "Bearbeiten bereits in der Datenbank befindlicher Schichten.";
$prio_link_txt = "Zur Präferenzeneingabe.";
$tab_link_txt = "Bestätigen und zur Schichttabelle.";
if(file_exists('texts.php')){
    include 'texts.php';
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
      <button class="logbtn"><?php echo "$edit_existing_jobs_txt";?></button>
    </a>
  </div>
  <h1>Definition des Schichtplanes</h1>
  <div class="mantxt">
    <?php
    if(file_exists('_indexmantxt.txt')){
        include '_indexmantxt.txt';
      }
      ?>
  </div>
  <div id="definition">
    <form action="tab.php"  method="get">
      <div id="inform">
        <span class="day">
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
        </span>

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
            <p>Klicke auf den Button "<?php echo "$add_job_btn_txt";?>", um ein Eingabefeld für die neue Tätigkeit erscheinen zu lassen.
                In das Textfeld gib bitte den Namen der Schicht ein. Setze einen Haken in die entsprechende Checkbox, falls die neue Schicht für Helfende bzw. sensibel ist. </p>
            <button id="add_job_btn" type="button" onclick="create_jobbox();"><?php echo "$add_job_btn_txt";?></button>
          </div>
        </div>
        <div id="submitdiv">
          <p>
            <!-- <input name="show_only_new_jobs" type="checkbox" value="true">Show only new -->
            <input id="submitdivbtn" type="submit" value="<?php echo "$tab_link_txt";?>">
          </p>
        </div>
      </div>
    </form>
  </div>
  <div id="prio_link">
    <a href="../crew_prios/index.php">
      <button class="logbtn"><?php echo "$prio_link_txt";?></button>
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
