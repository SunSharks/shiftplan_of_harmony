<?php
// Start the session
session_start();
if (!empty($_GET)){
  $_SESSION["src"] = $_GET["src"];
}
if(isset($_SESSION['user'])){
  $src = $_SESSION["src"];
  header("Location: https://schichtplan.funkloch-festival.de/$src");
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
$_SESSION["days"] = fetch_it(get_days_sql());
$_SESSION["jts"] = fetch_it(get_jobtypes_sql());
$_SESSION["num_timecols"] = 24 * count($_SESSION["days"]);
 ?>
<!-- <link rel="stylesheet" type="text/css" href="style.php"> -->
<?php
if (isset($_POST["username"])){
  // printf(json_encode($_POST));
  $users_db = fetch_it(get_users_sql());
  // printf(json_encode($users_db));
  $usernames = array();
  for ($i=0; $i<count($users_db); $i++){
    $usernames[$users_db[$i]["nickname"]] = $users_db[$i];
    // if ()
  }
  if (!array_key_exists($_POST["username"], $usernames)){
    $n = $_POST["username"];
    $alert = "User $n wurde nicht gefunden."; // LANG!
    echo "<script>alert('$alert');</script>";
  }
  else{
    $user = $usernames[$_POST["username"]];
    if (password_verify($_POST["password"], $user['pw'])){
      /* The password is correct. */
      $login = true;
      $_SESSION["user"] = $user;
      $suc_txt = "<div id='suc_text'>
        <p>
        Hallo.
          Du wurdest erfolgreich eingeloggt.
      </p>
    </div>";
      printf($suc_txt);
      $src = $_SESSION["src"];
      header("Location: https://schichtplan.funkloch-festival.de/$src");
      exit;
    }
    else{
      $fail_txt = "<div id='suc_text'>
        <p>
        Das hat nicht geklappt.
      </p>
    </div>";
      printf("$fail_txt");
    }
  }
}

?>

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
 form {
        border: 3px solid #f1f1f1;
    }
 input[type=text], input[type=password] {
        width: 100%;
        margin: 8px 0;
        padding: 12px 20px;
        display: inline-block;
        border: 2px solid green;
        box-sizing: border-box;
    }
 button:hover {
        opacity: 0.7;
    }
  .cancelbtn {
        width: auto;
        padding: 10px 18px;
        margin: 10px 5px;
    }


 .container {
        padding: 25px;
        background-color: lightblue;
    }
</style>
</head>


<body>
  <div id="head_row" class="head_row">
    <a href="signup.php">
      <button>Create Account</button>
    </a>
  </div>

  <h1>Login</h1>
    <form action="login.php" method="post" style="border:1px solid #ccc">
     <div class="container">
       <!-- LANG! -->
         <label>Username : </label>
         <input type="text" placeholder="Enter Username" name="username" title="Falls du einen Spitznamen angegeben hast, ist es der, falls nicht, ist es einfach dein Vor- und Nachname (unter Beachtung von Groß-/Kleinschreibung und mit Leerzeichen getrennt)." required>
         <label>Password : </label>
         <input type="password" placeholder="Enter Password" name="password" required>
         <button type="submit">Login</button>
         <input type="checkbox" checked="checked"> Remember me
         <button type="button" class="cancelbtn"> Cancel</button>
         <!-- Forgot <a href="#"> password? </a> -->
     </div>
     </form>

</body>
</html>
