<?php
// Start the session
session_start();
$_SESSION["src"] = "../helper_prios/index.php";
if(!isset($_SESSION['helper'])){
  header('Location: login.php?src=../helper_prios/index.php');
  exit;
}
if (!empty($_GET)){
  if (isset($_GET["log"])){
    if ($_GET["log"] === "out"){
      unset($_SESSION['helper']);

      unset($_SESSION["prios"]);
      header('Location: login.php?src=../helper_prios/index.php');
      exit;
    }
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
// printf("test1");
regain_preference_integrity();
// printf("test2");
$_SESSION["days"] = fetch_it(get_days_sql());
$_SESSION["jts"] = fetch_it(get_jobtypes_sql("true"));
if (empty($_SESSION["jts"]) || empty($_SESSION["days"])){
  echo "Irgendwas ist komisch.. ";
}
$_SESSION["num_timecols"] = 24 * count($_SESSION["days"]);
// printf(json_encode($_SESSION["helper"]));
$_SESSION["prios"] = fetch_prios($_SESSION["helper"]["fullname_id"]);
// printf(json_encode($_SESSION["prios"]));
 ?>
<link rel="stylesheet" type="text/css" href="style.php">
<?php
// $tst = substr("Hund", 0, -1);
if (!empty($_POST)){
  // printf(json_encode($_POST));
  // perform(insert_prios_sql());
  perform(insert_prios_sql($_POST));
  $_SESSION["prios"] = fetch_prios($_SESSION["helper"]["fullname_id"]);
  if (isset($_POST["workload"])){
    $_SESSION["helper"]["workload"] = $_POST["workload"];
  }
  if (isset($_POST["breakinp"])){
    $_SESSION["helper"]["break"] = $_POST["breakinp"];
  }
}
?>

<script src=insert_prios.js></script>
</head>


<body>
  <div id="head_row" class="head_row">
    <a href="index.php?log=out">
      <button>logout</button>
    </a>
  </div>
  <h1>Prioritäten</h1>
    <form name="prioform" action="index.php"  method="post" onsubmit="placeholder_to_value()">
      <div id="workload_div">
        <?php
        $wl = $_SESSION["helper"]["workload"];
        $break = $_SESSION["helper"]["break"];
        // echo "$break\r\n";
        echo "<label for='workload'>Wie viele Stunden möchtest du maximal arbeiten?</label>";
        echo "<input id='workload' name='workload' type='number' placeholder='$wl' min='4' title='Eine Schicht dauert mindestens 4 Stunden'>";
        ?>
      </div>
      <div class='breakinpdiv'><label id='breakinplabel' for='breakinp'>Mindestpause zwischen 2 Schichten</label></div>
      <?php
      echo "<div class='breakinpdiv'><input type='number' id='breakinp' name='breakinp' placeholder='$break' min='0' max='8'></input></div>";
      ?>
      <div id="prios" class="prios">
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
                if($i < 10){
                  $b = "&nbsp;$i";
                }
                else{
                  $b = $i;
                }
                echo "<td align='center' height='50'><b>$b</b></td>";
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
              $title = "title='".$jt["competences"]. "'";
              echo "<tr $rowidstr $row_class $style>";
              $n = $jt["name"];
              echo "<th $title class='rowhead' align='left' height='50'><b>$n</b></th>";
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
                $selbut = "<div class='prioselbut'><button type='button' class='selbtn' id='selbtn$id' onclick='select_entry($id)'>+</button></div>";
                $unselbut = "<div class='priounselbut'><button type='button' class='unselbtn' id='unselbtn$id' style='display:none' onclick='unselect_entry($id)'>-</button></div>";
                $inp = "<div class='prioinputfield'><input type='number' id='prioinp$id' name='prioinp$id' onchange='on_input($id)' placeholder='$val' min='1' max='5'></div>";
                echo "<div class='priotd'><td $style colspan='$span_hours' align='center' height='50'>$selbut$unselbut$inp</td></div>";
                echo "<script>add_prio_id($id);</script>";
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
      <div class='unselall'><button type='button' id='unselall' onclick='unselect_all()'>Unselect All</button></div>
      <div id="submitdiv">
          <p>
            <!-- <input name="show_only_new_jobs" type="checkbox" value="true">Show only new -->
            <?php
            $name_id = $_SESSION["helper"]["fullname_id"];
            echo "<input id='name_id' name='name_id' value='$name_id' hidden >";
            ?>
            <input id="submitdivbtn" type="submit" value="Speichern">
          </p>
        </div>
        </div>
    </form>


</body>
</html>
