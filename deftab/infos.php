<?php
// Start the session
session_start();

if(!isset($_SESSION['user'])){
  header('Location: ../users/login.php?src=../deftab/index.php');
  exit;
}
if (!empty($_GET)){
  if ($_GET["log"] === "out"){
    unset($_SESSION['user']);
    // printf(json_encode($_SESSION["user"]));
    header('Location: ../users/login.php?src=../deftab/index.php');
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
  <title>Infotexte</title>
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
  </div>
  <h1>Infotexte</h1>
  <div id="infoform">
    <form action="infos.php"  method="post">
      <?php
      $jobtypes = fetch_it(get_jobtypes_sql());
      $style = "style='grid-template-columns:";
      for ($i=0; $i<count($jobtypes); $i++){
        $style .= "auto ";
      }
      if (!($style === "style=grid-template-columns:")){
        $style = rtrim($style, " ");
        $style .= "';";
      }
      else{
        $style = "";
      }
      echo "<div class='texts' $style>";
      ?>
      <?php
        foreach ($jobtypes as $j) {
          $id = $j["id"];
          printf("<div class='jt_txt' ><textarea id='jt_txt$id' name='jt_txt$id' rows='100' cols='50' ></textarea></div>");
//                 <textarea id="story" name="story"
//           rows="5" cols="33">
// It was a dark and stormy night...
// </textarea>
        }
      ?>
        </div>
        <div id="submit_infos_div">
          <p>
            <!-- <input name="show_only_new_jobs" type="checkbox" value="true">Show only new -->
            <input id="submit_infos" type="submit" value="Zur Schichttabelle.">
          </p>
        </div>
    </form>
  </div>
  <div id="prio_link">
    <a href="../prios/index.php">
      <button class="logbtn">Zur Präferenzeneingabe. </button>
    </a>
  </div>

  <?php

  ?>

</body>

</html>
