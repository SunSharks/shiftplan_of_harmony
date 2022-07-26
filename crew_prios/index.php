<?php
// Start the session
session_start();
$_SESSION["src"] = "crew_prios";
if(!isset($_SESSION['user'])){
  header('Location: https://'. $_SERVER["HTTP_HOST"]. '/users/logout.php');
  exit;
}
if (!empty($_GET)){
  if (isset($_GET["log"])){
    if ($_GET["log"] === "out"){
      unset($_SESSION['user']);
      // printf(json_encode($_SESSION["user"]));
      unset($_SESSION["prios"]);
      header('Location: https://'. $_SERVER["HTTP_HOST"]. '/users/logout.php?log=out');
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
  <!-- <link rel="icon" type="image/x-icon" href="../images/fl_logo.png"> -->
  <title>crew preferences</title>


<?php
include("../users/db.php");
perform(create_preferences_table_sql(""));
regain_integrity();
// printf("test1");
regain_preference_integrity();
// printf("test2");
$_SESSION["days"] = fetch_it(get_days_sql());
$_SESSION["jts"] = fetch_it(get_jobtypes_sql("false"));
// if (empty($_SESSION["jts"]) || empty($_SESSION["days"])){
//   header('Location: ../deftab/index.php');
//   exit;
// }
$_SESSION["num_timecols"] = 24 * count($_SESSION["days"]);
// printf(json_encode($_SESSION["user"]));
$_SESSION["prios"] = fetch_prios($_SESSION["user"]["fullname_id"]);
// printf(json_encode($_SESSION["prios"]));
include("stats.php");
 ?>
<link rel="stylesheet" type="text/css" href="style.php">
<?php
// $tst = substr("Hund", 0, -1);
if (!empty($_POST)){
  // printf(json_encode($_POST));
  // perform(insert_prios_sql());
  if (isset($_POST["breakinp"])){
    $_SESSION["user"]["break"] = $_POST["breakinp"];
  }
  perform(insert_prios_sql($_POST));
  $_SESSION["prios"] = fetch_prios($_SESSION["user"]["fullname_id"]);
}
?>

<script src=insert_prios.js></script>
</head>


<body>
  <div id="head_row" class="head_row">
    <a href="index.php?log=out">
      <button>logout</button>
    </a>
    <!-- <a href="../deftab/index.php">
      <button>shiftplandef</button>
    </a> -->
  </div>
  <h1>Prioritäten</h1>
  <div class="mantxt">
    <?php
    if(file_exists('_indexmantxt.txt')){
        include '_indexmantxt.txt';
      }
    else if(file_exists('indexmantxt.txt')){
      include 'indexmantxt.txt';
    }
      ?>
  </div>
  <div id="prios" class="prios">
    <form name="prioform" action="index.php"  method="post" onsubmit="placeholder_to_value()">
      <div id='breakdiv' class='breakinpdiv'><label id='breakinplabel' for='breakinp'>Mindestpause zwischen 2 Schichten</label>
      <?php
      $break = $_SESSION["user"]["break"];
      echo "<div class='breakinpdiv'><input type='number' id='breakinp' name='breakinp' placeholder='$break' min='0' max='8'></input></div>";
      ?>
      </div>

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
              $res = $jt["restricted_access"];
              $readonly = "";
              $disabled = "";
              if ($res == 1){
                $readonly = " readonly ";
                $disabled = " disabled ";
              }
              if ($res == 1 && in_array($jt["name"], $_SESSION["access_jobs"])){
                $readonly = "";
                $disabled = "";
              }
              $jt_id = $jt["id"];
              // printf("---".json_encode($_SESSION["access_jobs"]));
              $rowidstr = "id='row$jt_id'";
              $row_class = $jt['name'];
              $style = $odd_style;
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
                $selbut = "<div class='prioselbut'><button type='button' class='selbtn' id='selbtn$id' onclick='select_entry($id)' $disabled>select</button></div>";
                $unselbut = "<div class='priounselbut'><button type='button' class='unselbtn' id='unselbtn$id' style='display:none' onclick='unselect_entry($id)' $disabled>unselect</button></div>";
                $inp = "<div class='prioinputfield'><input type='number' id='prioinp$id' name='prioinp$id' onchange='on_input($id)' placeholder='$val' min='1' max='5' $readonly></div>";
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
