<?php
// Start the session
session_start();
$_SESSION["src"] = "../crew_prios/change_user_settings.php";
if(!isset($_SESSION['user'])){
  header('Location: ../users/login.php?src=../crew_prios/change_user_settings.php');
  exit;
}
if (!empty($_GET)){
  if (isset($_GET["log"])){
    if ($_GET["log"] === "out"){
      unset($_SESSION['user']);
      // printf(json_encode($_SESSION["user"]));
      unset($_SESSION["prios"]);
      header('Location: ../users/login.php?src=../crew_prios/change_user_settings.php');
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
include("../users/db.php");
// perform(create_preferences_table_sql());
regain_integrity();
// printf("test1");
regain_preference_integrity();
// printf("test2");
$_SESSION["days"] = fetch_it(get_days_sql());
$_SESSION["jts"] = fetch_it(get_jobtypes_sql("false"));
if (empty($_SESSION["jts"]) || empty($_SESSION["days"])){
  header('Location: ../deftab/index.php');
  exit;
}
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
}
?>

<script src=insert_prios.js></script>
</head>


<body>
  <div id="head_row" class="head_row">
    <a href="index.php?log=out">
      <button>logout</button>
    </a>
    <a href="../deftab/index.php">
      <button>shiftplandef</button>
    </a>
  </div>
  <h1>Settings</h1>
  <div id="prios" class="prios">
    <form name="settings" action="change_user_settings.php"  method="post" onsubmit="placeholder_to_value()">
      <div class='change_nickname'><label id='change_nickname_label' for='change_nickname'>Neuer Nickname: </label></div>
      <?php
      $break = $_SESSION["user"]["break"];
      $nn = $_SESSION["user"]["nickname"];
      echo "<div class='change_nickname'><input type='text' id='change_nickname' name='change_nickname' placeholder='$nn'></input></div>";
      ?>


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
