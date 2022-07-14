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

body {
  background: rgba(230, 220, 220, 0.79);
  padding: 20px;
  margin: 0px;
  block-size: fit-content;
}

table {
  margin-left: 100px;
  table-layout: fixed;
  border-collapse: separate;
  border-spacing: 0;
  border-top: 1px solid #000;
}
th {
  margin: 0;
  border: 1px solid #000;
  white-space: nowrap;
  border-top-width: 0px;
}
td {
  margin: 0;
  width: fit-content;
  height: fit-content;
  <!-- border: 1px solid #000;
  white-space: nowrap;
  border-top-width: 0px; -->
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

<!-- input {
        resize: horizontal;
        width: 50px;
    }

    input:active {
        width: auto;
    }

    input:focus {
        min-width: 50px;
    } -->

#prios {
  <!-- display: grid;
  grid-template-rows: <?=$grid_template_rows?>;
  grid-template-columns: <?=$grid_template_columns?>; -->
  background-color: #2196F3;
  padding: 10px;
  width: 100%;
  overflow: auto;
}

.selbtn {
  padding: 0px;
  margin: 0px;
  height: 100%;
  width: 100%;
  display: inline;
  background-color: rgb(0,200,0);
}

.unselbtn {
  padding: 0px;
  margin: 0px;
  height: 90%;
  width: 100%;
  display: inline;
  background-color: rgb(200,0,0);
}

.prioselbut {
  padding: 0px;
  margin: 0px;
  height: 100%;
  width: 100%;
  display: inline;
  background-color: rgb(0,200,0);
}
.priounselbut {
  padding: 0;
  margin: 0;
  height: 100%;
  width: 100%;
  display: inline;
  background-color: rgb(200,0,0);
}

#submitdivbtn {
  width: fit-content;
}

#breakinp {
  width: 100%;
  margin: 8px 0;
  padding: 12px 20px;
  display: inline-block;
  border: 2px solid green;
  box-sizing: border-box;
}

#breakdiv{
  width: 100%;
  margin: 8px 0;
  padding: 12px 20px;
  border: 2px solid green;
  box-sizing: border-box;
}
