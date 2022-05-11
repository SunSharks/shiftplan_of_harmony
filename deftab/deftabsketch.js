let get_params;
//  JOBS
let jobnames = []; // "Ordnung", "Springer", "Bar", "Amphitheaterbetreuung", "Alternativebetreuung", "Büro", "Finanzamt", "Wasser", "Technik"
let jobtypes = new Map(); // {id: <jobtype instance>}
let num_jobs;
let json_jobs = [];
let job_instances = [];


// DAYS
let daynames = []; // "Freitag", "Samstag", "Sonntag"
let num_days;

let num_cols;
let headerheight = 30;
let rowheaderwidth = 100;
let gridendy;
let txtsize = 12;
let headertextx;
let headertexty;
let rowheadertextx = 0;
let rowheadertexty;

// ============
let col_width;
let row_height;
let ww;
let wh;

let grid;
let griditems = [];
let num_griditems = 0;
let curr_color = 'blue';
let curr_group = 0;
let default_colors;
let default_special_colors;

// let selected = -1;
let row = -1;
let curr_selected_cols = [];
let btn;
let savebtn;
let edited = false;



get_params = () => {
    // Address of the current window
    address = window.location.search

    // Returns a URLSearchParams object instance
    param_lst = new URLSearchParams(address)

    // Created a map which holds key value pairs
    let map = new Map()

    // Storing every key value pair in the map
    param_lst.forEach((value, key) => {
        map.set(key, value)
    })

    // Returning the map of GET parameters
    return map
}


function assign_params(map){
  let id;
  map.forEach (function(value, key){
    if (key.startsWith("day")){
      daynames.push(value);
      num_days = daynames.length;
    }
    else if (key.startsWith("job")){
      id = parseInt(key.slice(3));
      if (jobtypes.has(id)){
        jobtypes.get(id).set_name(value);
      }
      else{
        let new_jt = new Jobtype(id);
        new_jt.set_name(value);
        jobtypes.set(id, new_jt);
      }
      // console.log(jobs.get(id));
      jobnames.push(value);
      num_jobs = jobnames.length;
    }
    else if (key.startsWith("special")){
      id = parseInt(key.slice(7));
      if (jobtypes.has(id)){
        jobtypes.get(id).set_special();
      }
      else{
        let new_jt = new Jobtype(id);
        new_jt.set_special();
        jobtypes.set(id, new_jt);
      }
    }
  })
  console.log(jobtypes);
}


function setup() {
  // console.log("setup_tab");
  get_params = get_params();
  assign_params(get_params);
  createCanvas(windowWidth, windowHeight+20);
  num_cols = num_days * 24;
  col_width = (windowWidth - rowheaderwidth) / (num_cols);
  row_height = (windowHeight - headerheight) / num_jobs;
  if (row_height > 75){
    row_height = 75;
  }
  gridendy = row_height * num_jobs + headerheight;
  headertexty = headerheight / 2;
  let corrector = (col_width / 2) - txtsize / 2 -1;
  headertextx = rowheaderwidth + corrector;
  rowheadertexty = headerheight + row_height / 2;
  ww = windowWidth;
  wh = windowHeight;
  default_colors = [color(220, 220, 220), color(230, 230, 230)];
  default_special_colors = [color(220, 235, 220), color(230, 250, 230)];
  grid = new Grid();
  btn = new Button(0, 0, rowheaderwidth, headerheight, "deselect", false, ["select", "deselect"]);
  btn.draw();
  savebtn = new Button(rowheaderwidth, gridendy, ww, 50, "save", false, ["save", "save"]);
  savebtn.draw();
}


function save_data(){
  let groups = [];
  let group = [];
  let curr_group = -1;
  for (let i=0; i<griditems.length; i++){
    if (griditems[i].selected){
      if (griditems[i].group == curr_group || curr_group == -1){
        group.push(griditems[i]);
        curr_group = griditems[i].group;
      }
      else{
        groups.push(group);
        group = [griditems[i]];
        curr_group = griditems[i].group;
      }
    }
    else{
      if (group.length > 0){
        groups.push(group);
        group = [];
        curr_group = -1;
      }
    }
  }
  let ret = [];
  for (let i = 0; i<groups.length; i++){
    let j = new Job(groups[i][0].name, groups[i][0].time, groups[i].length, groups[i][0].jobtype_id, groups[i][0].special);
    json_jobs.push(JSON.stringify(j));
  }
  // write_to_file("jobs.json", ret);
  console.log(job_instances);
  console.log(json_jobs);
  return json_jobs
  }

function write_to_file(filename, obj){
  writer = createWriter(filename);
  writer.write(JSON.stringify(obj));
  writer.close();
}

function draw() {
  if (mouseIsPressed){
    btn.collides();
    savebtn.collides();
    if (mouseButton === LEFT){
      for (var i=0; i<griditems.length; i++){
        if (griditems[i].collides(mouseX, mouseY)){
          if(row == -1){
            row = Math.floor(i/grid.cols.length)
          }
          if (row == Math.floor(i/grid.cols.length)){
            if (!btn.state){
              griditems[i].set_color(curr_color);
              griditems[i].set_group(curr_group);
              griditems[i].select();
              edited = true;
            }
            else {
              griditems[i].deselect();
              edited = true;
            }
          }
        }
      }
    }
  }
}


function mouseReleased() {
    curr_color = grid.generate_random_color();
    curr_group += 1;
    row = -1;
}


class Jobtype {
  constructor(id){
    this.id = id;
    this.name;
    this.special = false;
  }

  set_special(){
    this.special = true;
  }

  set_name(name){
    this.name = name;
  }
}


class Grid {
  constructor(){
    this.rows = [];
    this.cols = [];
    this.assemble_grid();
    this.make_colheaders();
    this.make_rowheaders();
    this.selected = [];
    this.select = true;
  }

  deselect(){
    this.select = !this.select;
  }

  make_data_row(name, y, jobtype_id, special=false){
    let x = rowheaderwidth;
    let l = [];
    for (let i=0; i<num_cols; i++){
      let r = new Griditem(name, griditems.length, x, y, i, jobtype_id, special=special);
      r.show();
      griditems.push(r);
      l.push(r);
      x += col_width;
    }
    this.rows.push(l);
  }

  assemble_grid(num_rows=num_jobs){
    let y = headerheight;
    for (var [key, value] of jobtypes.entries()){
      this.make_data_row(jobtypes.get(key).name, y, jobtypes.get(key).jobtype_id, jobtypes.get(key).special);
      y += row_height;
    }
    let col = [];
    for (let i=0; i<num_cols; i++){
      for (let j=0; j<num_rows; j++){
        col.push(this.rows[j][i])
      }
      this.cols.push(col)
      col = [];
    }
  }

  generate_random_color(){
    let r = random(255); // r is a random number between 0 - 255
    let g = random(255); // g is a random number betwen 100 - 200
    let b = random(200); // b is a random number between 0 - 100
    let a = random(200,255); // a is a random number between 200 - 255
    return color(r, g, b, a);
  }

  insert_text(t, x, y){
    fill(0);
    // stroke(1);
    textFont('Helvetica');
    textSize(12);
    text(t, x, y);
    pop();
  }

  make_colheaders(){
    let x = headertextx;
    let y = headertexty;
    for (let i=0; i<num_cols; i++){
      for (let j=0; j<24; j++){
        this.insert_text(j.toString(), x, y);
        x += col_width;
      }
    }
  }

  make_rowheaders(){
    let y = rowheadertexty;
    for (let i=0; i<num_jobs; i++){
      this.insert_text(jobnames[i], 0, y);
      y += row_height;
    }
  }
}


class Griditem {
  constructor(name, id, x, y, time, jobtype_id, special=false, w=col_width, h=row_height) {
    this.name = name; // name of job
    this.special = special;
    this.id = id;
    this.jobtype_id = jobtype_id;
    this.time = time;
    this.day; // TODO
    this.x = x; // upper left corner
    this.y = y; // upper left corner
    this.w = w;
    this.h = h;
    this.content = "";
    this.color = default_colors[this.id%2];
    this.defaultcolor = default_colors[this.id%2];
    if (this.special){
      this.color = default_special_colors[this.id%2];
      this.defaultcolor = default_special_colors[this.id%2];
    }

    this.group = -1;
    this.selected = false;
  }

  collides(x, y) {
    let ret = x > this.x && x < this.x + this.w && y > this.y && y < this.y + this.h
    if (ret){
      this.set_color("green");
    }
    return ret
  }

  set_color(c, show=false){
    this.color = c;
    if (show){
      this.show();
    }
  }

  set_group(g){
    this.group = g;
  }

  select() {
      this.show();
      // print("selected." + this.id.toString());
      this.selected = true;
  }

  deselect(){
    this.color = this.defaultcolor;
    this.selected = false;
    this.show();
    // print("deselected." + this.id.toString());
  }

  show() {
    stroke(255);
    strokeWeight(4);
    // fill(255);
    // rect(this.x, this.y, this.w, this.h);
    fill(this.color);
    rect(this.x, this.y, this.w, this.h);
   // console.log("draw " + this.id.toString());
  }
}


class Job {
  constructor(name, start, dur, jobtype_id, special=false){
    this.name = name;
    this.start = start;
    this.end = start + dur;
    this.during = dur;
    this.start_day = daynames[Math.floor(this.start/24)];
    this.end_day = daynames[Math.floor(this.end/24)];
    this.dt_start = this.start % 24;
    this.dt_end = this.end % 24;
    this.special = special;
    this.jobtype_id = jobtype_id;
    job_instances.push(this);
  }
}


Button = function(x, y, w, h, func, state, texts) {
  this.func = func;   // "deselect", "save", "clear"
  this.state = state; //0, 1
  this.text = texts[+state];
  this.texts = texts;
  this.x = x;
  this.y = y;
  this.h = h;
  this.w = w;
  this.color = [0, 155, 140];
  this.textsize = 12;
}

Button.prototype.draw = function() {
  // stroke(0);
  if (this.func == "deselect"){
    if(this.state){
      fill(default_colors[0]);
    }
    else{
      fill(this.color[0], this.color[1], (this.color[2]+20*this.state)%255);
    }
  }
  else{
    fill(this.color[0], this.color[1], (this.color[2]+20*this.state)%255);
  }

  rect(this.x, this.y, this.w, this.h);
  textSize(this.textsize);
  fill(0)
  textStyle(NORMAL);
  text(this.text, this.x+10, this.y+this.h/2);
}

Button.prototype.collides = function() {
  var col = (mouseX >= this.x && mouseX <= this.x+this.w && mouseY >= this.y && mouseY <= this.y+this.h);
  if (col){
    this.change_mode();
  }
}
Button.prototype.change_mode = function() {
  if (this.func == "save"){
    if (this.state == 0 && edited == true){
      save_data();
      edited = false;
    }
  }
  else{
    this.state = !this.state;
  }
  this.text = this.texts[+this.state];
  this.draw();

}
