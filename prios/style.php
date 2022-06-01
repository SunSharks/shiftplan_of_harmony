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

.prios {
  <!-- display: grid;
  grid-template-rows: <?=$grid_template_rows?>;
  grid-template-columns: <?=$grid_template_columns?>; -->
  background-color: #2196F3;
  padding: 10px;
  overflow: auto;
}
.normal_gridit {
  background-color: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(0, 0, 0, 0.8);
  padding: 10px;
  font-size: 10px;
  text-align: center;
}
