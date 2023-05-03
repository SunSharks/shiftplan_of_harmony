<?php
// Start the session
session_start();
if (!empty($_GET)){
  $_SESSION["src"] = $_GET["src"];
}
if(isset($_SESSION['user'])){
  $src = $_SESSION["src"];
  header("Location: https://". $_SERVER["HTTP_HOST"] ."/crew_prios/index.php");
  exit;
}
?>
