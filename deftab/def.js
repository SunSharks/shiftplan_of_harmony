let days = [];
let num_jobs = 0;
// let jobs = [];

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
  let btn_box = document.createElement('div');
  btn_box.setAttribute("id", "jobdelbtn"+id.toString());
    // Then add the content (a new input box) of the element.
  btn_box.innerHTML = "<button type='button' onclick='delete_jobbox();'>"
  new_box.innerHTML = "<input type='text' id='job" + id.toString() + "'>";
  num_jobs++;

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
  const element = document.getElementById(id);
  element.remove();
  num_jobs--;
}

function remove(elem){
elem.parentNode.removeChild(elem);
}
