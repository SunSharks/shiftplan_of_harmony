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
  <?php
  // foreach ($_SESSION["days"] as $d){
  //   $n = $d["name"];
  //   echo "<div class='normal_gridit'>$n</div>";
  // }
  // foreach ($_SESSION["jts"] as $jt){
  //   $n = $jt["name"];
  //   echo "<div class='normal_gridit'>$n</div>";
  //   foreach ($_SESSION["days"] as $d){
  //     echo "<div class='inner_grid'>";
  //     $inp = "<input type='number' id='prioinp' name='prioinp' min='1' max='5'>";
  //     echo "<div class='grid-item'>INPUT</div>";
  //     echo "</div>";
  //   }
  // }
  ?>
  <h1>Prioritäten</h1>
  <div id="prios" class="prios">
    <table border="5" cellspacing="0" align="center">
        <!--<caption>Timetable</caption>-->
        <tr> <!-- DAYNAME ROW -->
          <td rowspan="2" align="center" height="50">
              <b>Job/Time</b></br>
          </td>
          <?php
          foreach ($_SESSION["days"] as $d){
            $n = $d["name"];
            echo "<td colspan='24' align='center' height='50'><b>$n</b></td>";
          }
          ?>
        </tr>

        <tr> <!-- DAYTIME ROW -->
          <?php
          foreach ($_SESSION["days"] as $d){
            for ($i=0; $i<24; $i++){
              echo "<td align='center' height='50'><b>$i</b></td>";
            }
          }
          ?>
        </tr>
        <?php
        foreach ($_SESSION["jts"] as $jt){
          echo "<tr>";
          $n = $jt["name"];
          echo "<td align='center' height='50'><b>$n</b></td>";
          foreach ($_SESSION["days"] as $d){
            for ($i=0; $i<24; $i++){
              echo "<td align='center' height='50'><b>.</b></td>";
            }
          }
          echo "</tr>";
        }
        ?>


      </table>
  </div>

</body>
</html>
