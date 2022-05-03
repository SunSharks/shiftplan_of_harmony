let days = [];
let num_jobs = 0;
// let jobs = [];

class Daybox{
  constructor(){
    // First create a DIV element.
    this.id = days.length;
    this.box = document.createElement('div');
    this.box.setAttribute("id", "daybox");
    days.push(this);
  }

  create_daybox(){
    // Then add the content (a new input box) of the element.
    this.box.innerHTML = "<input type='text' id='day" + this.id + "'>";
      // Finally put it where it is supposed to appear.
    document.getElementById("add_day").appendChild(this.box);
    days.push(this.box);
  }

   delete_daybox(){
    id = days[days.length-1].id;
    days.pop();
    const element = document.getElementById(id);
    element.remove();
  }
}

class Jobbox{
  constructor(){

  }
  create_jobbox(){
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



function delete_jobbox(id){
  const element = document.getElementById(id);
  element.remove();
  num_jobs--;
}

function remove(elem){
elem.parentNode.removeChild(elem);
}
}
