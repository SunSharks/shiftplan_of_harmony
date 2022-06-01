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
$_SESSION["num_timecols"] = 24 * count($_SESSION["days"]);
 ?>
<link rel="stylesheet" type="text/css" href="style.php">
</head>


<body>
  <h1>Prioritäten</h1>
  <div id="prios" class="prios">
    <form action="index.php"  method="post">
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
          <!-- JOBTYPE ROWS -->
          <?php
            foreach ($_SESSION["jts"] as $jt){
              $jt_id = $jt["id"];
              $rowidstr = "id='row$jt_id'";
              echo "<tr $rowidstr $row_class $style>";
              $n = $jt["name"];
              echo "<td align='center' height='50'><b>$n</b></td>";
              $jt_jobs = fetch_jobtype_jobs($jt["id"]);
              $idx = 0;
              foreach ($jt_jobs as $j){
                $id = $j["id"];
                $span_hours = $j["during"];
                while ($idx < $j["abs_start"]){
                  if ($idx % 2 === 0){
                    $style = "style='background-color:#d3e3c4'";
                  }
                  else{
                    $style = "style='background-color:#edf9e1'";
                  }
                  $inp = "<input type='number' id='prioinp$id' name='prioinp$id' min='1' max='5' hidden>";
                  echo "<td $style align='center' height='50'>$inp</td>";
                  $idx++;
                }
                if ($idx % 2 === 0){
                  $style = "style='background-color:#d3e3c4'";
                }
                else{
                  $style = "style='background-color:#edf9e1'";
                }
                $inp = "<input type='number' id='prioinp$id' name='prioinp$id' value='3' min='1' max='5'>";
                echo "<td $style colspan='$span_hours' align='center' height='50'>$inp</td>";
                $idx = $j["abs_end"];
              }
              while ($idx <= $_SESSION["num_timecols"]){
                if ($idx % 2 === 0){
                  $style = "style='background-color:#d3e3c4'";
                }
                else{
                  $style = "style='background-color:#edf9e1'";
                }
                $inp = "<input type='number' id='prioinp$id' name='prioinp$id' min='1' max='5' hidden>";
                echo "<td $style align='center' height='50'>$inp</td>";
                $idx++;
              }
              echo "</tr>";
            }
          ?>
      </table>
      <div id="submitdiv">
          <p>
            <!-- <input name="show_only_new_jobs" type="checkbox" value="true">Show only new -->
            <input id="submitdivbtn" type="submit" value="Speichern">
          </p>
        </div>
    </form>
  </div>

</body>
</html>
