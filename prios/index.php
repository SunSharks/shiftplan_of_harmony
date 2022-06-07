<?php
// Start the session
session_start();

if(!isset($_SESSION['user'])){
  header('Location: login.php');
  exit;
}
if (!empty($_GET)){
  if ($_GET["log"] === "out"){
    unset($_SESSION['user']);
    // printf(json_encode($_SESSION["user"]));
    unset($_SESSION["prios"]);
    header('Location: login.php');
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


<?php
include("db.php");
// perform(create_preferences_table_sql());
regain_integrity();
regain_preference_integrity();
$_SESSION["days"] = fetch_it(get_days_sql());
$_SESSION["jts"] = fetch_it(get_jobtypes_sql());
$_SESSION["num_timecols"] = 24 * count($_SESSION["days"]);
// printf(json_encode($_SESSION["user"]));
$_SESSION["prios"] = fetch_prios($_SESSION["user"]["fullname_id"]);
// printf(json_encode($_SESSION["prios"]));
 ?>
<link rel="stylesheet" type="text/css" href="style.php">
<?php
$tst = substr("Hund", 0, -1);
if (!empty($_POST)){
  // printf(json_encode($_POST));
  // perform(insert_prios_sql());
  insert_prios_sql($_POST);
}
?>
</head>


<body>
  <div id="head_row" class="head_row">
    <a href="index.php?log=out">
      <button>logout</button>
    </a>
  </div>
  <h1>Prioritäten</h1>
  <div id="prios" class="prios">
    <form action="index.php"  method="post">
      <table id="priotab" border="5" cellspacing="0" align="center">
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
            $odd_style = "style='background-color:#edf9e1'";
            $even_style = "style='background-color:#d3e3c4'";
            foreach ($_SESSION["jts"] as $jt){
              $jt_id = $jt["id"];
              $rowidstr = "id='row$jt_id'";
              echo "<tr $rowidstr $row_class $style>";
              $n = $jt["name"];
              echo "<th class='rowhead' align='left' height='50'><b>$n</b></th>";
              $jt_jobs = fetch_jobtype_jobs($jt["id"]);
              $idx = 0;
              foreach ($jt_jobs as $j){
                $id = $j["id"];
                $span_hours = $j["during"];
                while ($idx < $j["abs_start"]){
                  if ($idx % 2 === 0){
                    $style = $even_style;
                  }
                  else{
                    $style = $odd_style;
                  }
                  $inp = "";
                  echo "<td $style align='center' width='20px' height='50'>$inp</td>";
                  $idx++;
                }
                if ($idx % 2 === 0){
                  $style = $even_style;
                }
                else{
                  $style = $odd_style;
                }
                $val = $_SESSION["prios"][$id];
                $inp = "<input type='number' id='prioinp$id' name='prioinp$id' value='$val' min='1' max='5'>";
                echo "<td $style colspan='$span_hours' align='center' height='50'>$inp</td>";
                $idx = $j["abs_end"];
              }
              while ($idx <= $_SESSION["num_timecols"]){
                if ($idx % 2 === 0){
                  $style = $even_style;
                }
                else{
                  $style = $odd_style;
                }
                $inp = "";
                echo "<td $style align='center'  height='50'>$inp</td>";
                $idx++;
              }
              echo "</tr>";
            }
          ?>
      </table>
      <div id="submitdiv">
          <p>
            <!-- <input name="show_only_new_jobs" type="checkbox" value="true">Show only new -->
            <?php
            $name_id = $_SESSION["user"]["fullname_id"];
            echo "<input id='name_id' name='name_id' value='$name_id' hidden >";
            ?>
            <input id="submitdivbtn" type="submit" value="Speichern">
          </p>
        </div>
    </form>
  </div>

</body>
</html>
