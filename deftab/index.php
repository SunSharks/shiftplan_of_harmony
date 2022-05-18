<!DOCTYPE html>
<html lang="de">

<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>schedule definition</title>
  <style>
    body {
      padding: 0;
      margin: 0;
    }
    h1 {text-align: center;}
    p {text-align: center;}
    .daybox {
      float:left;
      padding: 100;
    }
    .inner_daybox {
      display: block;
      padding: 100;
    }


    /* .day {
      padding: 100;
      margin: 100;
    } */
    /* .jobbox {
      display: inline;
    } */
    #del_day {
      display: inline;
    }
    #add_day {
      display: inline;
    }
    /* #test {
      background-color: yellow;
    } */
    /* div {text-align: center;} */
  </style>

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

  <p id="demo"></p>


</head>

<body>
  <div id="definition">
    <form action="tab.php"  method="get">
      <div class="day">
        <!-- Fetch predefined days. -->
        <?php
          $pdo = connect();
          $days = perform_query($pdo, get_days_sql());
          $max_dayid = 0;
          foreach ($days as $d) {
            printf(get_daybox_html_readonly($d["id"], $d["name"], $d["date"]));
            if ($d["id"] > $max_dayid){
              $max_dayid = $d["id"];
            }
          }
        ?>


        <script> set_days(<?php echo json_encode($days); ?>);</script>
        <div id="add_day"><button type="button" onclick="create_daybox();">+</button></div>
        <div id="del_day"><button type="button" onclick="delete_daybox();">-</button><br></div>
      </div>
      <div id="job">
        <!-- Fetch predefined jobtypes. -->
        <?php
          $pdo = connect();
          $jobtypes = perform_query($pdo, get_jobtypes_sql());
          $maxid = 0;
          foreach ($jobtypes as $j) {
            printf(get_jobbox_html($j["id"], $j["name"], $j["special"]));
            $job_cnt++;
            if ($maxid < (int)$j["id"]){
              $maxid = (int)$j["id"];
            }
          }
        ?>
        <script>
        let test = set_jobs(<?php echo json_encode($jobtypes); ?>);
        // console.log(test);
        </script>
        <br>
        <div id="add_job"><button type="button" onclick="create_jobbox();">+</button><br></div>
      </div>
  <div><p><input type="submit" value="Show me the table!"></p></div>
    </form>
  </div>

</body>

</html>
