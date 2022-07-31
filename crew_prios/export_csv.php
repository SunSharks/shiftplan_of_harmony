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
  $pdo = connect();
  $stmt = $pdo->prepare($sql);
  $stmt->execute();
  while ($row = $stmt->fetch()) {
    // print_r($row);
    fputcsv($handle, [$row["user_id"], $row["user_email"], $row["user_name"]]);
  }
  fclose($handle);
  echo "DONE!";
  }
  export_csv();
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <!-- <link rel="icon" type="image/x-icon" href="../images/fl_logo.png"> -->
  <title>crew preferences</title>
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
