<?php header("Content-type: text/css");
// Start the session
session_start();
$num_days = count($_SESSION["days"]);
$num_jts = count($_SESSION["days"]);
$grid_template_columns = str_repeat(" auto ", $num_days+1);
$grid_template_rows = str_repeat(" auto ", $num_jts+1);
 ?>

<!-- table {
  table-layout: fixed;
} -->

input {
        resize: horizontal;
        width: 50px;
    }

    input:active {
        width: auto;
    }

    input:focus {
        min-width: 50px;
    }

.prios {
  <!-- display: grid;
  grid-template-rows: <?=$grid_template_rows?>;
  grid-template-columns: <?=$grid_template_columns?>; -->
  background-color: #2196F3;
  padding: 10px;
  overflow: auto;
}


[id^="row"] {
  cursor: pointer;
  }

[id^="row"]:hover {background-color: #3e8e41}

[id^="row"]:active {
  background-color: #82ceb4;
  transform: translateY(4px);
}

#submitdivbtn {
  width: fit-content;
}
