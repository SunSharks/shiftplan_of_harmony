let name_special = "Helper";
const daynames = [ "Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
let days = [];
let dates_qs = [];
let day_instances = [];
let day_maxid = 0;
let numdays = 0;
let numjobs = 0;
let abs_numjobs = 0;
let jobtypes = new Map();
let num_db_jobs = 0;
let maxid = 0;


function set_days(d, maxid){
  console.log(d);
  day_instances.push(new Day(d.date));
  day_maxid = maxid;
  numdays = d.length;
}

function set_jobs(j){
  // console.log(j);
  let _maxid = 0;
  for (let i=0; i<j.length; i++){
    jobtypes[i.id] = j[i];
    // console.log(jobtypes[i.id].id);
    if (_maxid < jobtypes[i.id].id){
      _maxid = jobtypes[i.id].id;
    }
  }
  maxid = _maxid;
  numjobs = j.length;
  abs_numjobs = j.length;
  num_db_jobs = j.length;
  return "yes";
}

function hide_it() {
  const btn = document.getElementById("hidebtn");
  btn.addEventListener("click", ()=>{
    if(btn.innerText === "HIDE DEFINITIONS"){
        btn.innerText = "SHOW DEFINITIONS";
    }else{
        btn.innerText = "HIDE DEFINITIONS";
    }
  });

  var x = document.getElementById("definition");
  if (x.style.display === "none") {
    x.style.display = "block";
  } else {
    x.style.display = "none";
  }
}
function create_daybox(){
    // First create a DIV element.
  // console.log(parseInt(numdays) + days.length);
  let id = ++day_maxid;
  let new_box = document.createElement('div');
  new_box.setAttribute("id", "daybox"+id.toString());
  new_box.setAttribute("class", "daybox");

  let innerdaydate = document.createElement('div');
  innerdaydate.setAttribute("id", "divday"+id.toString());
  innerdaydate.setAttribute("class", "inner_daybox");

  let innerdayinput = document.createElement('date');
  innerdayinput.setAttribute("id", "day"+id.toString());
  // innerdayinput.setAttribute("onchange", "show_date(" + id.toString() + ")");
  innerdayinput.innerHTML = "<br><input type='date' name='day" + id.toString() + "' required>";

  let innerdaylabel = document.createElement('div');
  innerdaylabel.setAttribute("id", "day_label"+id.toString());
  innerdaylabel.setAttribute("class", "inner_daybox");
  // innerdaylabel.innerHTML = "<label for='day" + id.toString() + "'></label>"


  console.log(innerdayinput.id);
  // Finally put it where it is supposed to appear.
  innerdaydate.appendChild(innerdayinput);
  new_box.appendChild(innerdaylabel);
  new_box.appendChild(innerdaydate);
  document.getElementById("add_day").appendChild(new_box);
  days.push(new_box);


  const input = document.querySelector("#"+innerdayinput.id);
  const log = document.getElementById("day_label"+id.toString());
  input.addEventListener('onchange', updateValue);
  dates_qs.push(input);

}

function updateValue(e) {
  console.log(e.target.value);
  log.textContent = e.target.value;
}

function create_jobbox(){
  let id = ++maxid;
  // console.log(maxid);
  var check_box = document.createElement('checkbox');
  check_box.setAttribute("class", "jobbox");
  check_box.setAttribute("id", "special"+id.toString());
  check_box.setAttribute("name", "special"+id.toString());
  check_box.setAttribute("value", "special"+id.toString());
  check_box.innerHTML = "<input type='checkbox' name='special" + id.toString() + "'>";
  let label = document.createElement('label');
  label.setAttribute("for", "checkbox");
  label.setAttribute("name", "cb_label"+id.toString());
  label.setAttribute("id", "cb_label"+id.toString());
  label.innerHTML = name_special;
// <label for="smoking" name="yesnos" id="yesnos">No</label>
  let new_box = document.createElement('div');
  new_box.setAttribute("id", "jobbox"+id.toString());
  new_box.setAttribute("class", "jobbox");
  let btn_box = document.createElement('button');
  btn_box.setAttribute("id", "jobdelbtn"+id.toString());
  btn_box.innerHTML = "<button type='button' class='inlinebtn' onclick='delete_jobbox(" + id.toString() + ");'>-</button>";
  // print("<button type='button' content='-' onclick='delete_jobbox(" + id.toString() + ");'>");
  new_box.innerHTML = "<input type='text' name='job" + id.toString() + "' id='job"   + id.toString() + "' required><br>";
  // alert(id.toString());
  jobtypes[id] = new_box;
  numjobs++;
  abs_numjobs++;
    // Finally put it where it is supposed to appear.
  label.appendChild(check_box);
  document.getElementById("add_job").appendChild(label);
  document.getElementById("add_job").appendChild(btn_box);
  document.getElementById("add_job").appendChild(new_box);
}

function delete_daybox(){
  // console.log(days);
  id = days[days.length-1].id;
  let d = days.pop();
  const element = document.getElementById(d.id);
  element.remove();
}

function delete_jobbox(id){
  const element = document.getElementById("jobbox"+id.toString());
  element.remove();
  const el = document.getElementById("jobdelbtn"+id.toString());
  el.remove();
  numjobs--;
  const e = document.getElementById("cb_label"+id.toString());
  e.remove();
  delete jobtypes[id];
}

function remove(elem){
elem.parentNode.removeChild(elem);
}

function write_to_file(){
  const writer = createWriter("jobs_days.json");
  let d = [];
  for (let i=0; i<days.length; i++){
    // console.log(document.getElementById("day"+i.toString()).value);
    // console.log(jobtypes);
    d.push(document.getElementById("day"+i.toString()).value);
  }
  let j = [];
  for (const [key, value] of Object.entries(jobtypes)) {
    // console.log(`${key}: ${value}`);
    // console.log(document.getElementById("job"+key.toString()).value);
    j.push(document.getElementById("job"+key.toString()).value);
  }
  writer.write(JSON.stringify(d));
  writer.write(JSON.stringify(j));
  writer.close();
}

class Day{
  constructor(date, indb=false, name=null, id=null){
    this.date = date;
    this.indb = indb;
    // console.log(this.date);
    this.date_date = new Date(this.date);
    this.name = name;
    this.id = id;
    this.calculate_dayname();
    // console.log(this.name);
  }

  calculate_dayname(){
    this.name = daynames[this.date_date.getDay()];
  }

  set_indb(){
    this.indb = true;
  }
}

function make_day_instances(d){
  for (let i=0; i<d.length; i++){
    // console.log(d[i]);
    let tmp = new Day(d[i]);
    // console.log(tmp);
  }
}

function show_date(id){
  console.log("day" + id);
  console.log(document.getElementById("day" + id).value);
  let date = document.getElementById("day" + id).value;
  let tmp = new Date(date);
  document.getElementById("day_label"+id).setAttribute("value", daynames[tmp.getDay()]);
  return daynames[tmp.getDay()];
}
