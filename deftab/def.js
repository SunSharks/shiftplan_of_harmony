let days = [];
let num_jobs = 0;
let jobs = [];

function create_daybox(){
    // First create a DIV element.
  var new_box = document.createElement('div');
  new_box.setAttribute("id", "daybox");
    // Then add the content (a new input box) of the element.
  new_box.innerHTML = "<input type='text' id='day" + days.length + "'>";

    // Finally put it where it is supposed to appear.
  document.getElementById("add_day").appendChild(new_box);
  days.push(new_box);
}

function create_jobbox(){
  let new_box = document.createElement('div');
  let id = num_jobs;
  new_box.setAttribute("id", "jobbox"+id.toString());
  let btn_box = document.createElement('button');
  btn_box.setAttribute("id", "jobdelbtn"+id.toString());
  btn_box.innerHTML = "<button type='button' content='del' onclick='delete_jobbox(" + id.toString() + ");'>";
  // print("<button type='button' content='-' onclick='delete_jobbox(" + id.toString() + ");'>");
  new_box.innerHTML = "<input type='text' id='job"   + id.toString() + "'>";
  // alert(id.toString());
  num_jobs++;
  jobs.push(new_box);
//   let btn_box = document.createElement('button');
//   btn_box.setAttribute("id", "jobdelbtn"+id.toString());
//   btn_box.setAttribute('content', '+');
//     // Then add the content (a new input box) of the element.
//   btn_box.innerHTML = "<button type='button' onclick='delete_jobbox(" + id + ");'>"
//   new_box.innerHTML = "<input type='text' id='job" + id.toString() + "'>";
//   num_jobs++;
//
//   var b =
//
// b.setAttribute('id', 'btn');
// b.textContent = 'test value';
//
// var wrapper = document.getElementById("divWrapper");
// wrapper.appendChild(b);

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
}

function remove(elem){
elem.parentNode.removeChild(elem);
}

function write_json(){

}
