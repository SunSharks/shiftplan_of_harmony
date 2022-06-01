<?php header("Content-type: text/css");
// Start the session
session_start();
$num_days = count($_SESSION["days"]);
$num_jts = count($_SESSION["days"]);
$grid_template_columns = str_repeat(" auto ", $num_days+1);
$grid_template_rows = str_repeat(" auto ", $num_jts+1);
 ?>

<!--
#priotab {
  width: auto;
  overflow: scroll;
  table-layout: fixed;
} -->

table {
  border-collapse: separate;
  border-spacing: 0;
  border-top: 1px solid #000;
}
td, th {
  margin: 0;
  border: 1px solid #000;
  white-space: nowrap;
  border-top-width: 0px;
}
div {
  overflow-x: scroll;
  margin-left: 0;
  overflow-x: visible;
  padding: 0;
}
.rowhead {
  background-color: rgba(134, 180, 105, 0.57);
  position: absolute;
  width: fit-content;
  left: 0;
  top: auto;
  border: none;
  margin-top: -1px;
}
.headcol:before {
  content: 'Row ';
}
.long {
  background: #8cdba3;
  letter-spacing: 1em;
}

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
