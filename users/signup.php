<?php
// Start the session
session_start();
?>
<?php
$REDIRECT = false;
include("db.php");
regain_integrity();
$names_db = fetch_it(get_names_sql());
$full_names = [];
for ($i=0; $i<count($names_db); $i++){
  array_push($full_names, $names_db[$i]["surname"]." ".$names_db[$i]["famname"]);
}
// printf(json_encode($full_names));
$nicknames_db = fetch_it(get_nicknames_sql());
$nicknames = [];
for ($i=0; $i<count($nicknames_db); $i++){
  array_push($nicknames, $nicknames_db[$i]["nickname"]);
}
// printf(json_encode($nicknames));
 ?>
<?php
if (isset($_POST["fullname"])){
  printf(recover_umlauts(json_encode($_POST), "\\"));
  if ($_POST["psw"] != $_POST["psw-repeat"]){
    $alert = "Die beiden eingegebenen Passwörter sind nicht identisch.\\r\\nGib bitte zweimal dasselbe Passwort ein.";
    echo "<script>alert('$alert');</script>";
  }
  else{
    if (empty($_POST["nickname"])){
      $nickname = $_POST["fullname"];
    }
    else{
      $nickname = $_POST["nickname"];
    }
    $sql = insert_user_sql($_POST["fullname"], $_POST["psw"], $nickname);
    if ($sql != "INDB"){
      $pdo = connect();
      perform_query($pdo, $sql);
      $pdo = null;
      $suc_txt = "<div id='suc_text'>
        <p>
        Hallo $nickname.
          Du wurdest erfolgreich registriert.
      </p>
    </div>";
      // printf($suc_txt);
      header('Location: login.php');
      exit;
    }
    else{
      $alert = "Du bist bereits registriert.";
      $alerthtml = "<script>alert('$alert');</script>";
      echo $alerthtml;
    }
  }
}
if ($REDIRECT === false){
  echo "
  <!DOCTYPE html>
  <html lang='de'>
  <head>
    <meta charset='utf-8'>
    <meta http-equiv='Content-Type' content='text/html; charset=UTF-8' />
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <title>signup</title>
";
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
<link rel="stylesheet" type="text/css" href="signupstyle.css">
</head>


<body>
  <div id="head_row" class="head_row">
    <a href="login.php">
      <button>Login</button>
    </a>
  </div>
  <h1>Initialisierung</h1>
  <form action="signup.php" method="post" style="border:1px solid #ccc">
    <div class="container">
      <!-- LANG! -->
      <p>Herzlich Willkommen. <br>
        Damit niemand anderes deine Präferenzen einsehen oder verändern kann, teile bitte dem Programm mit, wer du bist und setze ein Passwort.
        Optional kannst du ebenfalls eine E-Mail setzen, damit du unkompliziert und schnell dein Passwort zurücksetzen kannst, falls du es vergessen hast.
        Optional kannst du dir auch einen Spitznamen geben, mit dem du dich künftig einloggen kannst und der dann auch dem Rest der Crew angezeigt wird.
        Dieser muss einzigartig sein.
      </p>
      <hr>

      <label for="fullname"><b>Dein Name</b></label>   <!-- LANG! -->
    <?php
      $regex_fn = join("|", $full_names);
      $s = "<input type='text' pattern='$regex_fn' placeholder='Dein Name' name='fullname' accept-charset='utf-8' required>";
      printf($s);
      ?>
      <label for="nickname"><b>Spitzname</b></label>  <!-- LANG! -->
      <?php
      //       ^(?!(WordA|WordB)$)[a-z A-Z0-9\s]+$
        $regex_nn = "(?!(";
        $regex_nn = $regex_nn . join("|", $nicknames) . ")$)[a-z A-Z0-9\s]+$";
        $s = "<input type='text' pattern='$regex_nn' placeholder='[optional] Spitzname' name='nickname' accept-charset='utf-8'>"; //<!-- LANG! -->
        printf($s);
        ?>

      <label for="psw"><b>Passwort</b></label>  <!-- LANG! -->
      <!-- $name, $pw, $nickname, $email -->
      <input type="password" placeholder="Enter Password" name="psw" accept-charset="utf-8" required>

      <label for="psw-repeat"><b>Zur Sicherheit nochmal das Passwort</b></label>
      <input type="password" placeholder="Repeat Password" name="psw-repeat" accept-charset="utf-8" required>
      <!-- LANG! -->
      <!-- <label for="email"><b>E-Mail</b></label>
      <input type="text" placeholder="[optional] Deine Mailadresse" name="email">   -->

      <!-- <label>
        <input type="checkbox" checked="checked" name="remember" style="margin-bottom:15px"> Remember me
      </label> -->

      <!-- <p>By creating an account you agree to our <a href="#" style="color:dodgerblue">Terms & Privacy</a>.</p> -->

      <div class="clearfix">
        <button type="button" class="cancelbtn">Cancel</button>
        <button type="submit" class="signupbtn">Sign Up</button>
      </div>
    </div>
  </form>

</body>
</html>
