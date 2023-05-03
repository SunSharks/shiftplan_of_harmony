<?php
// Start the session
session_start();
$_SESSION["src"] = "../deftab/edit_existing_jobs.php";
if(!isset($_SESSION['user'])){
  header('Location: ../users/logout.php?src=../deftab/edit_existing_jobs.php');
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
  <title>edit existing</title>
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
    <a href="index.php">
      <button class="logbtn">Zurück zu Definitionen</button>
    </a>
    <a href="index.php?log=out">
      <button class="logbtn">logout</button>
    </a>
  </div>
  <h1>Gespeicherte Schichten bearbeiten</h1>
  <div class="mantxt">
      Auf dieser Seite können nur Daten bearbeitet werden, die bereits in der Datenbank gespeichert sind.
  </div>
  <div id="links">
      <div class="link">
          <a href="../deftab/infos.php">
            <button class="linkbtn" title="Gib einen Text mit näheren Informationen zu der Tätigkeit ein.">Infotexte</button>
          </a>
    </div>
    <div class="link">
        <a href="../deftab/delete_jobtype.php">
            <button class="linkbtn" title="Hier kannst du einzelne Schichten (Zeilen) löschen.">Tätigkeit löschen</button>
        </a>
      </div>
    </div>

  <div class="enddiv">
  </div>

</body>

</html>
