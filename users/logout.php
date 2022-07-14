<?php
// Start the session
session_start();
$logouttxt = "<div id='logouttxt'><p>Du wurdest erfolgreich ausgeloggt.</p></div>";
if (!empty($_GET)){
  $_SESSION["src"] = $_GET["src"];
  $src = $_SESSION["src"];
  if (isset($_GET["log"])){
    echo $logouttxt;
  }
}
if(isset($_SESSION['user'])){
  $src = $_SESSION["src"];
  header("Location: $src");
  exit;
}
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>login</title>

<?php
include("db.php");
regain_integrity();
 ?>
<!-- <link rel="stylesheet" type="text/css" href="style.php"> -->

<style>
Body {
  font-family: Calibri, Helvetica, sans-serif;
  background-color: rgba(140, 133, 130, 0.79);
}
button {
       background-color: #4CAF50;
       width: 100%;
        color: orange;
        padding: 15px;
        margin: 10px 0px;
        border: none;
        cursor: pointer;
         }
 button:hover {
        opacity: 0.7;
    }


 .container {
        padding: 25px;
        background-color: lightblue;
    }

  #buttons {
    width: 100%;
    margin: 8px 0;
    padding: 12px 20px;
    border: 2px solid green;
    box-sizing: border-box;
  }
</style>
</head>


<body>
  <div id="buttons">
  <div id="login" class="head_row">
    <p> Hast du dich bereits registriert? Dann kannst du dich hier einloggen. </p>

    <a href=<?php echo "login.php?src=$src";?>>
      <button>Login</button>
    </a>
  </div>

  <div id="signup" class="head_row">
    <p> Falls du diese Seite zum ersten Mal besuchst, registriere dich bitte. Intern ist eine Liste mit allen Namen aus der Crew hinterlegt. Dieses Vorgehen hat technische Gründe. </p>
    <a href=<?php echo "signup.php?src=$src";?>>
      <button>Create Account</button>
    </a>
  </div>
</div>

</body>
</html>
