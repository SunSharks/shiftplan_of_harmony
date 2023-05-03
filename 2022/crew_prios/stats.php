<?php
// include("db.php");
$jobs_count = fetch_it("SELECT count(id) FROM Jobs WHERE Jobs.jt_primary IN (SELECT id FROM Jobtypes WHERE helper=0);")[0]["count(id)"];
$work_hours_sum = fetch_it("SELECT sum(during) FROM Jobs WHERE Jobs.jt_primary IN (SELECT id FROM Jobtypes WHERE helper=0);")[0]["sum(during)"];
$bias_work_hours = fetch_it("SELECT sum(bias) FROM Users;")[0]["sum(bias)"];
$num_persons = fetch_it("SELECT count(id) FROM Names WHERE Names.helper = 0;")[0]["count(id)"];
$work_hours_avg = ($work_hours_sum + $bias_work_hours) / $num_persons;
$num_registered_users = fetch_it("SELECT count(id) FROM Users;")[0]["count(id)"];
if($work_hours_sum % $num_persons === 0){
  $jobs_div_pers = "nicht so"; // LANG!
}
else{
  $jobs_div_pers = "so";  // LANG!
}
?>
