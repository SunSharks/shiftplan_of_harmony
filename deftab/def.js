let days = [];
let num_jobs = 0;
let abs_num_jobs = 0;
let jobs = {};
// var dict = {
//   FirstName: "Chris",
//   "one": 1,
//   1: "some value"
// };

function setup(){

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
  var new_box = document.createElement('div');
  new_box.setAttribute("id", "daybox"+days.length.toString());
  new_box.setAttribute("class", "daybox");
    // Then add the content (a new input box) of the element.
  new_box.innerHTML = "<input type='text' id='day" + days.length + "'>";

    // Finally put it where it is supposed to appear.
  document.getElementById("add_day").appendChild(new_box);
  days.push(new_box);
}

function create_jobbox(){
  let new_box = document.createElement('div');
  let id = abs_num_jobs;
  new_box.setAttribute("id", "jobbox"+id.toString());
  let btn_box = document.createElement('button');
  btn_box.setAttribute("id", "jobdelbtn"+id.toString());
  btn_box.innerHTML = "<button type='button' content='del' onclick='delete_jobbox(" + id.toString() + ");'>-</button>";
  // print("<button type='button' content='-' onclick='delete_jobbox(" + id.toString() + ");'>");
  new_box.innerHTML = "<input type='text' id='job"   + id.toString() + "'>";
  // alert(id.toString());
  jobs[id.toString()] = new_box;
  num_jobs++;
  abs_num_jobs++;
    // Finally put it where it is supposed to appear.
  document.getElementById("add_job").appendChild(new_box);
  document.getElementById("add_job").appendChild(btn_box);
}

function delete_daybox(){
  id = days[days.length-1].id;
  days.pop();
  const element = document.getElementById(id);
  element.remove();
}

function delete_jobbox(id){
  const element = document.getElementById("jobbox"+id.toString());
  element.remove();
  const el = document.getElementById("jobdelbtn"+id.toString());
  el.remove();
  num_jobs--;
  delete jobs[id];
}

function remove(elem){
elem.parentNode.removeChild(elem);
}

function write_to_file(){
  const writer = createWriter("jobs_days.json");
  let d = [];
  for (let i=0; i<days.length; i++){
    console.log(document.getElementById("day"+i.toString()).value);
    console.log(jobs);
    d.push(document.getElementById("day"+i.toString()).value);
  }
  let j = [];
  for (const [key, value] of Object.entries(jobs)) {
    // console.log(`${key}: ${value}`);
    // console.log(document.getElementById("job"+key.toString()).value);
    j.push(document.getElementById("job"+key.toString()).value);
  }
  writer.write(JSON.stringify(d));
  writer.write(JSON.stringify(j));
  writer.close();
}


function draw(){

}
