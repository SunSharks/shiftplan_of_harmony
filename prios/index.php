<?php
// Start the session
session_start();
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>schedule definition</title>


<?php
include("db.php");
regain_integrity();
$_SESSION["days"] = fetch_it(get_days_sql());
$_SESSION["jts"] = fetch_it(get_jobtypes_sql());
$_SESSION["jobs"] = fetch_it(get_jobs_sql());

 ?>
<link rel="stylesheet" type="text/css" href="style.php">
</head>


<body>
  <h1>Prioritäten</h1>
  <div id="prios" class="prios">
    <div id="upperleftit" class="normal_gridit">Bitte gib deine Präferenzen an.</div>
    <?php
    foreach ($_SESSION["days"] as $d){
      $n = $d["name"];
      echo "<div class='normal_gridit'>$n</div>";
    }
    foreach ($_SESSION["jts"] as $jt){
      $n = $jt["name"];
      echo "<div class='normal_gridit'>$n</div>";
      foreach ($_SESSION["days"] as $d){
        echo "<div class='inner_grid'>";
        $inp = "<input type='number' id='prioinp' name='prioinp' min='1' max='5'>";
        echo "<div class='grid-item'>INPUT</div>";
        echo "</div>";
      }
    }
    ?>

  </div>
    <!-- <form action="tab.php"  method="get">
      <div id="inform">
        <div class="day"> -->
          <!-- Fetch predefined days. -->

<p>A Grid Layout must have a parent element with the <em>display</em> property set to <em>grid</em> or <em>inline-grid</em>.</p>

<p>Direct child element(s) of the grid container automatically becomes grid items.</p>


</body>
</html>
