const daynames = [ "Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"];
let days = [];
let dates_qs = [];
let day_instances = [];
let day_maxid = 0;
let numdays = 0;
let numjobs = 0;
let abs_numjobs = 0;
let jobtypes = new Map();
let jobboxes = new Map();
let twins = new Map();
let twin_ids = [];
let twin_maxid = 0;

let num_db_jobs = 0;
let job_maxid = 0;


function set_days(d, maxid){
  // console.log(d);
  day_instances.push(new Day(d.date));
  day_maxid = maxid;
  numdays = d.length;
}

function set_jobs(j){
  console.log(j);
  let _maxid = 0;
  for (let i=0; i<j.length; i++){
    let id = parseInt(j[i].id);
    jobtypes[id] = j[i];
    if (_maxid < parseInt(jobtypes[id].id)){
      _maxid = parseInt(jobtypes[id].id);
    }
  }
  console.log(_maxid);
  job_maxid = _maxid;
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


  // console.log(innerdayinput.id);
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
  // console.log(e.target.value);
  log.textContent = e.target.value;
}

function delete_daybox(){
  // console.log(days);
  id = days[days.length-1].id;
  let d = days.pop();
  const element = document.getElementById(d.id);
  element.remove();
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
  // console.log("day" + id);
  // console.log(document.getElementById("day" + id).value);
  let date = document.getElementById("day" + id).value;
  let tmp = new Date(date);
  document.getElementById("day_label"+id).setAttribute("value", daynames[tmp.getDay()]);
  return daynames[tmp.getDay()];
}


class Basic_Jobbox{
  constructor(mode){
    this.mode = mode;
    this.base_html;
  }

  create_basic_jobbox(id, outer_div, basic_name){
    // Creates skeleton of jobbox for new jobs consisting of:
    // name input field, helper checkbox, sensitive checkbox
    let inp_inner_html = "<input type='text' name='" + basic_name + id.toString() + "' id='" + basic_name  + id.toString() + "' required>";
    let input_div = this.create_jobbox_elem("div", "jobbox", basic_name+"box"+id.toString(), inp_inner_html);
    outer_div.appendChild(input_div);
    let prefix = "";
    if (basic_name === "job"){
      jobtypes[id] = input_div;
    }
    if (basic_name.endsWith("twin")){
        twins[id] = input_div;
        prefix = "twin_";
    }
    let helper_check_box_div = this.create_jobbox_elem("div", "jobbox");
    inp_inner_html = "<input type='checkbox' name='" + prefix + "helper" + id.toString() + "'>";
    let helper_check_box = this.create_jobbox_elem("checkbox", "jobbox", prefix+"helper"+id.toString(), inp_inner_html, prefix+"helper"+id.toString(), prefix+"helper"+id.toString());
    helper_check_box_div.appendChild(helper_check_box);
    outer_div.appendChild(helper_check_box_div);

    let helper_label_div = this.create_jobbox_elem("div", "jobbox", prefix+"helper_label_div"+id.toString());
    let helper_label = this.create_jobbox_elem("label", "jobbox", prefix+"helper_label"+id.toString(), "Helper", prefix+"helper_label"+id.toString(), "", prefix+"helper"+id.toString());
    helper_label_div.appendChild(helper_label);
    outer_div.appendChild(helper_label_div);

    let special_check_box_div = this.create_jobbox_elem("div", "jobbox");
    special_check_box_div.setAttribute("class", "jobbox");
    inp_inner_html = "<input type='checkbox' name='special" + id.toString() + "'>";
    let special_check_box = this.create_jobbox_elem("checkbox", "jobbox", prefix+"special"+id.toString(), inp_inner_html, prefix+"special"+id.toString(), prefix+"special"+id.toString());
    special_check_box_div.appendChild(special_check_box);
    outer_div.appendChild(special_check_box_div);

    let special_label_div = this.create_jobbox_elem("div", "jobbox");
    let special_label = this.create_jobbox_elem("label", "jobbox", prefix+"special_label"+id.toString(), "sensibel", prefix+"special_label"+id.toString(), "", prefix+"special"+id.toString());
    special_label_div.appendChild(special_label);
    outer_div.appendChild(special_label_div);
  }

  create_jobbox_elem(elem_type, cls="", id="", inner_html="", name="", value="", forstr=""){
    let elem = document.createElement(elem_type);
    elem.setAttribute("id", id);
    elem.setAttribute("class", cls);
    if (!(name.length === 0)){
      elem.setAttribute("name", name);
    }
    if (!(value.length === 0)){
      elem.setAttribute("value", value);
    }
    if (!(forstr.length === 0)){
      elem.setAttribute("for", forstr);
    }
    elem.innerHTML = inner_html;
    return elem;
  }
}

class Jobbox extends Basic_Jobbox{
  constructor(){
    super("job");
    this.id = ++job_maxid;
    this.outer_div = this.create_jobbox_elem("div", "outerjobbox", "outerjobbox"+this.id.toString());
    this.twins = new Map();
    this.create_basic_jobbox(this.id, this.outer_div, "job");
    this.create_jobbox_addons();
    jobboxes.set(this.id, this);
    console.log(jobboxes);
    this.twins_ids = document.getElementById("twins_ids"+this.id.toString());
  }

  create_jobbox_addons(){
    let inp_inner_html = "<button id='add_twin_btn"+this.id.toString() + "' type='button' onclick='add_twinbox(" + this.id.toString() + ");'>Add twin</button>"; // LANG!!
    let add_twin_div = this.create_jobbox_elem("div", "jobbox", "add_twin_div"+this.id.toString(), inp_inner_html);

    let new_twins_box = this.create_jobbox_elem("div", "new_twins_box", "new_twins_box"+this.id.toString());
    add_twin_div.appendChild(new_twins_box);
    this.outer_div.appendChild(add_twin_div);
    inp_inner_html = "<button id='jobdelbtn"+this.id.toString() + "' type='button' onclick='delete_jobbox(" + this.id.toString() + ");'>Löschen</button>"; // LANG!!
    let btn_box = this.create_jobbox_elem("div", "jobbox", "delbtndiv"+ this.id.toString(), inp_inner_html);
    this.outer_div.appendChild(btn_box);
    inp_inner_html = "<input type='text' name='" + "twins_ids"+this.id.toString() + "' id='" + "twins_ids"+this.id.toString() + "' hidden>";
    let twins_ids_div = this.create_jobbox_elem("div", "jobbox", "twins_ids_div"+this.id.toString(), inp_inner_html);
    this.outer_div.appendChild(twins_ids_div);
    numjobs++;
    abs_numjobs++;
    document.getElementById("add_job").appendChild(this.outer_div);
  }

}

function delete_jobbox(jobid){
  jobboxes.get(parseInt(jobid)).outer_div.innerHTML = "";
  jobboxes.get(parseInt(jobid)).outer_div.innerHTML = "";
  // const element = document.getElementById("jobbox"+this.id.toString());
  // element.remove();
  // const el = document.getElementById("jobdelbtn"+this.id.toString());
  // el.remove();
  // numjobs--;
  // const e = document.getElementById("helper_label"+this.id.toString());
  // e.remove();
  // const cb = document.getElementById("helper"+this.id.toString());
  // cb.remove();
  // const sp = document.getElementById("special_label"+this.id.toString());
  // sp.remove();
  // const spd = document.getElementById("special"+this.id.toString());
  // spd.remove();
  // const outer = document.getElementById("outerjobbox"+this.id.toString());
  // outer.remove();
  delete jobboxes.get(parseInt(jobid));
  delete jobboxes.get(parseInt(jobid));
}
function create_jobbox(){
  let nj = new Jobbox();
}

function add_twinbox(jobid){
  let new_twin = new Twinbox(jobid);
  console.log("add twinbox");
  console.log(jobboxes.get(parseInt(jobid)).twins_ids);
  jobboxes.get(parseInt(jobid)).twins.set(parseInt(new_twin.id), new_twin);
  let tids = Array.from(jobboxes.get(parseInt(jobid)).twins.keys() );
  jobboxes.get(parseInt(jobid)).twins_ids.value = JSON.stringify(tids);
}

function delete_twinbox(jobid, twinid){
  console.log("del twin");
  console.log(jobboxes.get(parseInt(jobid)).twins);
  console.log("__del twin");
  jobboxes.get(parseInt(jobid)).twins.get(parseInt(twinid)).outer_div.innerHTML = "";
  jobboxes.get(parseInt(jobid)).twins.delete(parseInt(twinid));
  let tids = Array.from(jobboxes.get(parseInt(jobid)).twins.keys() );
  jobboxes.get(parseInt(jobid)).twins_ids.value = JSON.stringify(tids);
}


class Twinbox extends Basic_Jobbox{
  constructor(jobbox_id){
    super("twin");
    this.jobbox_id = jobbox_id;
    this.id = twin_maxid++;
    console.log(twin_maxid);
    this.mother_div = document.getElementById("new_twins_box"+this.jobbox_id.toString()); // Jobbox div
    this.outer_div = this.create_jobbox_elem("div", "twin", "new_twin_"+ this.id.toString());
    this.outer_div.style.width = "200px";
    this.create_twinbox_addons();
  }

  create_twinbox_addons(){
    this.create_basic_jobbox(this.id, this.outer_div, "twin");
    let param = this.jobbox_id.toString() + ", " + this.id.toString();
    let inp_inner_html = "<button id='twindelbtn"+this.id.toString() + "' type='button' onclick='delete_twinbox("+ param + ");'>Löschen</button>"; // LANG!!
    let btn_box = this.create_jobbox_elem("div", "jobbox", "twindelbtndiv"+ this.id.toString(), inp_inner_html);
    this.outer_div.appendChild(btn_box);
    this.mother_div.appendChild(this.outer_div);
  }

}

// http://localhost/deftab/tab.php?PREday1=2022-06-03&PREday2=2022-06-04&PREday3=2022-06-06&PREday4=2022-06-07&PREday5=2022-06-08&job1=Bar&PREjob1=&job2=Bar&special2=special2&PREjob2=&job3=B%C3%BCro&PREjob3=&job4=Technik&PREjob4=&job5=B%C3%BChnenbetreuung&PREjob5=&job21=Crew+sensibel&special21=special21&PREjob21=&job22=Crew+unsensibel&PREjob22=&job23=Helper+sensibel&helper23=helper23&special23=special23&PREjob23=&job24=Helper+unsensibel&helper24=helper24&PREjob24=&job25=t1&twin1=twin11&twin_helper1=on&special1=on&twin4=twin12&job26=t2&twin2=twin21&twin5=twin22&twin_helper5=on&special5=on

// http://localhost/deftab/tab.php?PREday1=2022-06-03&PREday2=2022-06-04&PREday3=2022-06-06&PREday4=2022-06-07&PREday5=2022-06-08&job1=Bar&PREjob1=&job2=Bar&special2=special2&PREjob2=&job3=B%C3%BCro&PREjob3=&job4=Technik&PREjob4=&job5=B%C3%BChnenbetreuung&PREjob5=&job21=Crew+sensibel&special21=special21&PREjob21=&job22=Crew+unsensibel&PREjob22=&job23=Helper+sensibel&helper23=helper23&special23=special23&PREjob23=&job24=Helper+unsensibel&helper24=helper24&PREjob24=&job27=t1&twin3=t11&twin4=t12&twins_ids27=&job28=t2&twin5=t21&twin6=t22&twins_ids28=

// http://localhost/deftab/tab.php?PREday1=2022-06-03&PREday2=2022-06-04&PREday3=2022-06-06&PREday4=2022-06-07&PREday5=2022-06-08&job1=Bar&PREjob1=&job2=Bar&special2=special2&PREjob2=&job3=B%C3%BCro&PREjob3=&job4=Technik&PREjob4=&job5=B%C3%BChnenbetreuung&PREjob5
// =&job21=Crew+sensibel&special21=special21&PREjob21=&job22=Crew+unsensibel&PREjob22=&job23=Helper+sensibel&helper
//23=helper23&special23=special23&PREjob23=&job24=Helper+unsensibel&helper24=helper24&PREjob24=&job25=t1&PREjob25=&job26=t2&PREjo
//b26=&job27=t1&twin1=t11&twin2=t12&twins_ids27=%5B1%2C2%5D&job28=t2&twin3=t21&twin4=t22&twins_ids28=%5B3%2C4%5D&job30=t3&twins_ids30=
