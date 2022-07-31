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

<?php
  include("../users/db.php");
  function export_csv(){
  // (B) CREATE EMPTY CSV FILE ON SERVER
  $csvFile = "export.csv";
  $handle = fopen($csvFile, "w");
  if ($handle === false) { exit("Error creating $csvFile"); }

  // (C) GET USERS FROM DATABASE + WRITE TO FILE
  $sql_skel = "SELECT * FROM ";
  $tablenames = ["Days", "Jobtypes", "Jobs", "Users", "Names", "Helpers", "Exclusives"];
  $sql = "";
  foreach ($tablenames as $tn){
    $sql .= $sql_skel . ";";
  }
  $stmt = $pdo->prepare($sql);
  $stmt->execute();
  while ($row = $stmt->fetch()) {
    // print_r($row);
    fputcsv($handle, [$row["user_id"], $row["user_email"], $row["user_name"]]);
  }
  fclose($handle);
  echo "DONE!";
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


</body>
</html>
