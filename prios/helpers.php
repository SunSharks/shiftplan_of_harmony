<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
</head>
<body>
  <?php
  $users_db = fetch_it(get_users_sql());
  function name_in_names($val){

  }

  printf(json_encode($users_db));
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
      $_SESSION["login"] = true;
      $suc_txt = "<div id='suc_text'>
        <p>
        Hallo $nickname.
          Du wurdest erfolgreich eingeloggt.
      </p>
    </div>";
      printf($suc_txt);
    }

    ?>
  <body>
</html>
