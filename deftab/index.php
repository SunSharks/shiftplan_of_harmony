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
      display: inline;
      padding: 100;

    }
    .day {
      padding: 100;
      margin: 100;
    }
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

  <!-- <script src="./p5/p5.min.js"></script> -->
  <?php include("db.php"); ?>

  <script src=def.js></script>
</head>

<body>
  <div id="definition">
    <form action="tab.html"  method="get">
      <div class="day">
        <!-- Fetch predefined days. -->
        <?php
          $pdo = connect();
          $days = perform_query($pdo, get_days_sql());
          foreach ($days as $d) {
            printf(get_daybox_html_readonly($day_cnt, $d["name"]));
            // echo $day_cnt;
            $day_cnt++;
          }
          $day_cnt++;
          echo $day_cnt;
        ?>


        <script> js_variable_name = "<?php echo $php_variable; ?>";</script>
        <script> set_numdays(<?php echo $day_cnt; ?>);</script>
        <div id="add_day"><button type="button" onclick="create_daybox();">+</button></div>
        <div id="del_day"><button type="button" onclick="delete_daybox();">-</button><br></div>
      </div>
      <div id="job">
        <!-- Fetch predefined jobs. -->
        <?php
          $pdo = connect();
          $jobs = perform_query($pdo, get_job_def_sql());
          foreach ($jobs as $j) {
            printf(get_jobbox_html($j["id"], $j["name"], $j["special"]));
          }
        ?>
        <div id="add_job"><button type="button" onclick="create_jobbox();">+</button><br></div>
      </div>
  <div><p><input type="submit" value="Show me the table!"></p></div>
    </form>
  </div>

<!-- <main>
</main> -->

</body>

</html>
