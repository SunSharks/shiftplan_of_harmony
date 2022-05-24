<?php
// Start the session
session_start();
?>

<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>schedule definition</title>
  <link rel="stylesheet" type="text/css" href="style.css">

  <!-- <script>
    const input = document.querySelector('input');
    const log = document.getElementById('values');
    input.addEventListener('input', updateValue);
    function updateValue(e) {
      log.textContent = e.target.value;
    }
  </script> -->

  <?php include("db.php"); ?>
  <script src=def.js></script>
</head>

<body>
  <div id="definition">
    <form action="tab.php"  method="get">
      <div class="day">
        <!-- Fetch predefined days. -->
        <?php
          $_SESSION["days"] = fetch_it(get_days_sql());
          $max_dayid = fetch_maxid("Days");
          foreach ($_SESSION["days"] as $d) {
            printf(get_daybox_html_readonly($d["id"], $d["name"], $d["date"]));
          }
        ?>
        <script> set_days(<?php echo json_encode($_SESSION["days"]).", ".$max_dayid; ?>);</script>
        <div id="add_day"><button type="button" onclick="create_daybox();">+</button></div>
        <div id="del_day"><button type="button" onclick="delete_daybox();">-</button><br></div>
      </div>

      <div id="job">
        <!-- Fetch predefined jobtypes. -->
        <br><br>
        <?php
          $jobtypes = fetch_it(get_jobtypes_sql());
          foreach ($jobtypes as $j) {
            printf(get_jobbox_html($j["id"], $j["name"], $j["special"]));
          }
        ?>
        <script>
        set_jobs(<?php echo json_encode($jobtypes); ?>);
        // console.log(test);
        </script>
        <br>
        <div id="add_job"><button type="button" onclick="create_jobbox();">+</button><br></div>
      </div>
  <div><p><input type="submit" value="Show me the table!"></p></div>
    </form>
  </div>

  <?php
  $_SESSION["days_indb"] = false;
  $_SESSION["jts_indb"] = false;
  $_SESSION["jobs_indb"] = false;
  if ($_SESSION["deleted"] === false){
    $_SESSION["days_indb"] = true;
    $_SESSION["jts_indb"] = true;
    $_SESSION["jobs_indb"] = true;
  }
  ?>

</body>

</html>
