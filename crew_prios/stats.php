<?php
// include("db.php");
printf(json_encode(fetch_it("SELECT sum(during) FROM Jobs WHERE Jobs.jt_primary IN (SELECT id FROM Jobtypes WHERE helper=0);")));
$jobs_count = fetch_it("SELECT count(id) FROM Jobs WHERE Jobs.jt_primary IN (SELECT id FROM Jobtypes WHERE helper=0);")[0]["count(id)"];
$work_hours_sum = fetch_it("SELECT sum(during) FROM Jobs WHERE Jobs.jt_primary IN (SELECT id FROM Jobtypes WHERE helper=0);")[0]["sum(during)"];
$num_persons = fetch_it("SELECT count(id) FROM Names WHERE Names.helper = 0;")[0]["count(id)"];
$work_hours_avg = $work_hours_sum / $num_persons;
$num_registered_users = fetch_it("SELECT count(id) FROM Users;")[0]["count(id)"];
if($work_hours_sum % $num_persons === 0){
  $jobs_div_pers = "nicht so";
}
else{
  $jobs_div_pers = "so";
}
?>
