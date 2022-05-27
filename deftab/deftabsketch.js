let request_mode = "get";
let get_params  = new Map();
let edit_mode = true;
let deletion_mode = false;
let del_btns = [];
//  JOBS
let jt_id_to_griditems = new Map();
let jobnames = []; // "Ordnung", "Springer", "Bar", "Amphitheaterbetreuung", "Alternativebetreuung", "Büro", "Finanzamt", "Wasser", "Technik"
let jobtypes = new Map(); // {id: <jobtype instance>}
let num_jobs;
let predef_jobs = [];
let json_jobs = [];
let job_instances = [];
let job_instances_id = new Map();
let max_jobid = -1;
let indb_jts = [];
let indb_jobs = [];
let editable_area = 0;
let del_idxs = [];

// DAYS
let days = new Map();
let days_arr = [];
let indb_days = [];
const daynames = [ "Sonntag", "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag"]; // "Freitag", "Samstag", "Sonntag"
let num_days;

let num_cols;
const headerheight = 30;
const rowheaderwidth = 100;
let gridendy;
const txtsize = 12;
let headertextx;
let headertexty;
let rowheadertextx = 0;
let rowheadertexty;

// ============
let default_col_width;
let row_height;
let ww;
let wh;

let grid;
let daygrid;
let dayview = false;
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
let cntbox;
let edited = false;

function set_post_request_mode(){
  request_mode = "post";
}

function set_get_request_mode(){
  request_mode = "get";
}

function unset_edit_mode(){
  console.log("unset edit_mode");
  edit_mode = false;
}

function set_deletion_mode(){
  deletion_mode = true;
}

function unset_deletion_mode(){
  deletion_mode = false;
}

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

function get_params_readonly(ds, jts, js){
  for (let i=0; i<ds.length; i++){
    let id = ds[i]["id"];
    let new_day = new Day(ds[i]["date"], id, indb=true);
    days.set(id, new_day);
    days_arr.push(new_day);
    num_days = days_arr.length;
  }
  for (let i=0; i<jts.length; i++){
    let id = jts[i]["id"];
    let new_jt = new Jobtype(id);
    new_jt.set_name(jts[i]["name"]);
    new_jt.set_indb();
    if (jts[i]["special"] === true){
      new_jt.set_special();
    }
    jobtypes.set(id, new_jt);
    jobnames.push(jts[i]["name"]);
    num_jobs = jobnames.length;
  }
  predef_jobs = js;
}




function assign_params(map){
  let id;
  map.forEach (function(value, key){
    if (key.startsWith("day")){
      id = parseInt(key.slice(3));
      let new_day = new Day(value, id, indb=false);
      days.set(id, new_day);
      days_arr.push(new_day);
      num_days = days_arr.length;
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
      jobnames.push(value);
      num_jobs = jobnames.length;
    }
    else if (key.startsWith("PRE")){
      id = parseInt(key.slice(6));
      if (key.startsWith("PREjob")){
        if (jobtypes.has(id)){
          jobtypes.get(id).set_indb();
          jobtypes.get(id).set_name(value);
        }
        else{
          let new_jt = new Jobtype(id);
          new_jt.set_indb();
          jobtypes.set(id, new_jt);
        }
      }
      else if (key.startsWith("PREday")){
        if (days.has(id)){
          days.get(id).set_indb();
        }
        else{
          let new_day = new Day(value, id, indb=true);
          days.set(id, new_day);
          days_arr.push(new_day);
          num_days = days_arr.length;
        }
      }

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
}

function insert_predefined_jobs(job_json){
  predef_jobs = job_json;
}

function insert_day_indb(day_json){
  indb_days.push(day_json);
}

function insert_jobtype_indb(jt_json){
  indb_jts.push(jt_json);
}

function insert_job_indb(job_json){
  indb_jobs.push(job_json);
}

function setup() {
  if (request_mode === "get"){
    console.log("get");
    get_params = get_params();
    assign_params(get_params);
    console.log("__get");
  }
  num_cols = num_days * 24;
  default_col_width = (windowWidth-5 - rowheaderwidth-5) / (num_cols);
  row_height = (windowHeight-20 - headerheight) / num_jobs;
  let canv;
  if (row_height > 100){
    row_height = 100;
    canv = createCanvas(windowWidth-5, row_height*num_jobs+100);
  }
  else{
    canv = createCanvas(windowWidth-5, windowHeight-20);
  }
  canv.parent("p5tab");

  if (request_mode === "post"){
    background(242, 199, 87, 200);
  }
  gridendy = row_height * num_jobs + headerheight;
  headertexty = headerheight / 2;
  let corrector = (default_col_width / 2) - txtsize / 2 -1;
  headertextx = rowheaderwidth + corrector;
  rowheadertexty = headerheight + row_height / 2;
  ww = windowWidth-5;
  wh = windowHeight-5;
  // COLOR DEFINITION!
  default_colors = [[color(246, 232, 184), color(255, 255, 204)], [color(229, 216, 171), color(241, 241, 185)]];
  default_special_colors = [[color(211, 227, 196), color(237, 249, 225)],[color(199, 227, 171), color(223, 248, 195)]];
  grid = new Grid();
  btn = new Button(0, 0, rowheaderwidth, headerheight, "deselect", false, ["select", "deselect"]);
  btn.draw();
  // savebtn = new Button(rowheaderwidth, gridendy, ww, 50, "save", false, ["save", "save"]);
  // savebtn.draw();
  // console.log(jt_id_to_griditems);
  // console.log(predef_jobs);
  // if (request_mode != "get"){
    grid.insert_predefs();
  // }

  // grid.update_predefs();
  if (edit_mode === true){
    cntbox = new Countbox(0, gridendy-10, rowheaderwidth, 50);
  }
  let daybtn_div = document.getElementById("daybtns");
  let w = rowheaderwidth.toString() + "px";
  daybtn_div.style.setProperty('left', w);
  // let dayselection = document.getElementById("dayselection");
  // dayselection.style.setProperty('left', w);

  let wholeviewbtn = document.getElementById("wholeviewbtn");
  wholeviewbtn.style.setProperty('left', w);
  w = (windowWidth-5-rowheaderwidth).toString() + "px";
  wholeviewbtn.style.setProperty('width', w);

  let daywidth = default_col_width * 24;
  for (let i=0; i<num_days; i++){
    let w = daywidth.toString() + "px";
    let daybtn = document.getElementById("daybtn"+i.toString());
    daybtn.style.setProperty('width', w);
  }
}


function save_data(){
  let groups = [];
  let group = [];
  let curr_group = -1;
  for (let i=0; i<grid.rows.length; i++){
    for (let j=0; j<grid.rows[i].length; j++){
      if (grid.rows[i][j].selected){
        if (grid.rows[i][j].group === curr_group || curr_group === -1){
          group.push(grid.rows[i][j]);
          curr_group = grid.rows[i][j].group;
        }
        else{
          groups.push(group);
          group = [grid.rows[i][j]];
          curr_group = grid.rows[i][j].group;
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
    if (group.length > 0){
      groups.push(group);
    }
    group = [];
    curr_group = -1;
  }
  // console.log("GROUPS");
  let ret = [];
  for (let i = 0; i<groups.length; i++){
    // console.log(JSON.stringify(groups[i]));
    let j = new Job(groups[i][0].jobid, groups[i][0].name, groups[i][0].time, groups[i].length, groups[i][0].jobtype_id, groups[i][0].special, groups[i][0].pre);
    json_jobs.push(JSON.stringify(j));
    // console.log(JSON.stringify(j));
  }
  // write_to_file("jobs.json", ret);
  // console.log(job_instances);
  // for (let i=0; i<json_jobs.length; i++){
  //   console.log(json_jobs[i]);
  // }
  console.log("created json jobs.");

  return json_jobs
  }

function write_to_file(filename, obj){
  writer = createWriter(filename);
  writer.write(JSON.stringify(obj));
  writer.close();
}

function get_colliding_row(mouse_y){
  if (dayview){
    for (let i=daygrid.rows.length-1; i>=0; i--){
        // console.log(mouse_y.toString() + " => daygrid => " + daygrid.rows[i][0].y);
      if (mouse_y > daygrid.rows[i][0].y && mouse_y < daygrid.rows[i][0].y+daygrid.rows[i][0].h){
        return i;
      }
    }
  }
  else{
    for (let i=grid.rows.length-1; i>=0; i--){
      let upper = grid.rows[i][0].y + grid.rows[i][0].h;
      // console.log(mouse_y.toString() + " => grid => " + grid.rows[i][0].y + " => => " + grid.rows[i][0].h + grid.rows[i][0].h);
      if ((mouse_y > parseInt(grid.rows[i][0].y)) && (mouse_y < parseInt(grid.rows[i][0].y)+parseInt(grid.rows[i][0].h))){
        return i;
      }
    }
  }
  return false;
}


function draw() {
  let lastidx = griditems.length - 1;
  if (edit_mode){
    if (mouseIsPressed){
      // savebtn.collides();
      if (mouseButton === LEFT){
        if (mouseY > editable_area){
          let colliding_row = get_colliding_row(mouseY);
          if (colliding_row === false){
            console.log("no colliding row");
            return;
          }
          let use_grid;
          if (dayview){
            use_grid = daygrid;
          }
          else{
            use_grid = grid;
          }
          for (var i=0; i<use_grid.rows[colliding_row].length; i++){
            if (use_grid.rows[colliding_row][i].collides(mouseX, mouseY) && !jobtypes.get(use_grid.rows[colliding_row][i].jobtype_id).indb){
              console.log("colides" + use_grid.rows[colliding_row][i].name);
              if(row == -1){
                row = Math.floor(i/grid.cols.length);
              }
              if (row == Math.floor(i/grid.cols.length)){
                if (!btn.state){
                  if (use_grid.rows[colliding_row][i].selected && use_grid.rows[colliding_row][i].group == curr_group){
                    continue;
                  }
                  if (edit_mode === true){
                    cntbox.count();
                  }
                  use_grid.rows[colliding_row][i].set_color(curr_color);
                  use_grid.rows[colliding_row][i].set_group(curr_group);
                  use_grid.rows[colliding_row][i].select();
                  edited = true;
                }
                else {
                  use_grid.rows[colliding_row][i].deselect();
                  edited = true;
                }
              }
            }
          }
        }
      }
    }
  }
}

function mousePressed(){
  if (deletion_mode){
    for (let i=0; i<del_btns.length; i++){
      del_btns[i].collides();
    }
  }
  else{
    btn.collides();
  }
}


function mouseReleased() {
    curr_color = grid.generate_random_color();
    curr_group += 1;
    row = -1;
    if (edit_mode === true){
      cntbox.reset_counter();
    }

}

function clean_it_up(){
  clear();
  if (request_mode === "post"){
    background(242, 199, 87, 200);
  }
}


class Jobtype {
  constructor(id){
    this.id = id;
    this.name;
    this.special = false;
    this.indb = false;
    this.delete = false;
  }

  set_special(){
    this.special = true;
  }

  set_name(name){
    this.name = name;
  }

  set_indb(){
    this.indb = true;
  }

  set_delete(){
    this.delete = true;
  }

  unset_delete(){
    this.delete = false;
  }

}

function resume_default_view(){
  clean_it_up();
  btn.draw();
  dayview = false;
  grid.make_colheaders();
  grid.make_rowheaders();
  for (let i=0; i<griditems.length; i++){
    griditems[i].set_default_coords();
    griditems[i].show();
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
    // console.log("Grid constructed.");
  }

  insert_predefs(){
    let colors = ['green', 'red', 'blue', 'yellow', 'magenta', 'black', 'cyan'];
    let c = 0;
    let _maxid = -1;
    console.log(jt_id_to_griditems);
    console.log(predef_jobs);
    for (var i=0; i< predef_jobs.length; i++){
      // curr_color = this.generate_random_color();
      curr_color = colors[c%colors.length];
      c++;
      if (jt_id_to_griditems.size == 0){
        return;
      }
      while (!jt_id_to_griditems.has(predef_jobs[i]["jt_primary"])){
        predef_jobs[i]["jt_primary"]++;
      }
      for (let t=predef_jobs[i]["abs_start"]; t<predef_jobs[i]["abs_end"]; t++){
        jt_id_to_griditems.get(predef_jobs[i]["jt_primary"])[t].set_color(curr_color, true);
        jt_id_to_griditems.get(predef_jobs[i]["jt_primary"])[t].select();
        jt_id_to_griditems.get(predef_jobs[i]["jt_primary"])[t].set_pre();
        jt_id_to_griditems.get(predef_jobs[i]["jt_primary"])[t].set_jobid(predef_jobs[i]["id"]);
      }
    }
  }

  update_predefs(){
    for (let i = 0; i < indb_jts.length; i++){
      if (jobtypes.size > 0){
        jobtypes.get(indb_jts[i]["id"]).set_indb();
      }
    }
    for (let i = 0; i < indb_days.length; i++){
      if (days.size > 0){
        days.get(parseInt(indb_days[i]["id"])).set_indb();
      }
    }
    for (let i = 0; i < indb_jobs.length; i++){
      if (job_instances_id.size > 0){
        jt_id_to_griditems.get(parseInt(indb_jobs[i]["id"])).set_pre();
      }
    }
  }

  deselect(){
    this.select = !this.select;
  }


  make_data_row(name, y, jobtype_id, row, special=false){
    let x = rowheaderwidth;
    let l = [];
    // editable_rows_start = 0;
    let day = 0;
    for (let i=0; i<num_cols; i++){
      if ((i % 24 === 0) && i != 0){
        day++;
      }
      let r = new Griditem(name, griditems.length, x, y, i, jobtype_id, row, day, special=special);

      r.show();
      griditems.push(r);
      l.push(r);
      x += default_col_width;
    }
    if (jobtypes.get(jobtype_id).indb){
      editable_area = y + row_height;
      // editable_rows_start = 0;
    }
    this.rows.push(l);
    jt_id_to_griditems.set(jobtype_id, l);

  }

  assemble_grid(num_rows=num_jobs){
    let y = headerheight;
    let cnt = 0;
    console.log(jobtypes);
    for (var [key, value] of jobtypes.entries()){
      this.make_data_row(jobtypes.get(key).name, y, jobtypes.get(key).id, cnt++, jobtypes.get(key).special);
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
    let r;
    let g;
    let b;
    while ((r === g) && (r === b)){
      r = Math.floor(Math.random() * 156) + 100; // r is a random number between 100 - 255
      g = Math.floor(Math.random() * 156) + 100; // g is a random number betwen 100 - 255
      b = Math.floor(Math.random() * 101) + 100; // b is a random number between 100 - 200
      // let a = Math.random(200,255); // a is a random number between 200 - 255
    }
    return color(r, g, b);
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
        x += default_col_width;
      }
    }
  }

  make_rowheaders(){
    let y = rowheadertexty;
    if (deletion_mode){
      for (var [key, value] of jobtypes.entries()){
        let new_btn = new Button(0, y, rowheaderwidth, headerheight, "delete"+key.toString(), false, ["delete\n"+jobtypes.get(key).name, "keep\n"+jobtypes.get(key).name]);
        new_btn.draw();
        del_btns.push(new_btn);
        y += row_height;
      }
    }
    else{
      for (let i=0; i<num_jobs; i++){
        this.insert_text(jobnames[i], 0, y);
        y += row_height;
      }
    }
  }
}

function create_dayview(day){
  dayview = true;
  daygrid = new Daygrid(grid, day);
}

class Daygrid {
  constructor(whole_grid, day){
    // whole_grid: Grid object, day: day index.
    clean_it_up();
    btn.draw();
    this.col_width = (ww - rowheaderwidth) / 24;
    this.whole_grid = whole_grid;
    this.startcol = day * 24;
    this.endcol = this.startcol + 24;
    this.rows = [];
    this.cols = [];
    this.make_colheaders();
    this.make_rowheaders();

    this.calc_rows_and_cols();
    this.update_coords();
  }

  calc_rows_and_cols(){
    for (let i=0; i<this.whole_grid.rows.length; i++){
      this.rows.push(this.whole_grid.rows[i].slice(this.startcol, this.endcol));
    }
    let col = [];
    for (let i=0; i<24; i++){
      for (let j=0; j<num_jobs; j++){
        col.push(this.rows[j][i])
      }
      this.cols.push(col)
      col = [];
    }
  }

  update_coords(){
    clean_it_up();
    btn.draw();
    this.make_colheaders();
    this.make_rowheaders();
    let y = headerheight;
    for (let i=0; i<this.whole_grid.rows.length; i++){
      for (let j=0; j<this.whole_grid.rows[i]; j++){
        this.whole_grid.rows[i][j].unset_coords();
      }
    }
    for (let i=0; i<this.rows.length; i++){
      let x = rowheaderwidth;
      for (let j=0; j<24; j++){
        this.rows[i][j].set_new_coords(x, y, this.col_width, row_height);
        this.rows[i][j].show();
        x += this.col_width;
      }
      y += row_height;
    }
  }

  generate_random_color(){
    let r = random(255); // r is a random number between 0 - 255
    let g = random(255); // g is a random number betwen 100 - 200
    let b = random(200); // b is a random number between 0 - 100
    // let a = random(200,255); // a is a random number between 200 - 255
    return color(r, g, b);
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
    let x = headertextx + this.col_width/2;
    let y = headertexty;
    for (let i=0; i<1; i++){
      for (let j=0; j<24; j++){
        this.insert_text(j.toString(), x, y);
        x += this.col_width;
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
  constructor(name, id, x, y, time, jobtype_id, row, day, special=false, w=default_col_width, h=row_height) {
    this.name = name; // name of job
    this.special = special;
    this.id = id;
    this.row = row;
    this.jobtype_id = jobtype_id;
    this.time = time;
    this.day; // TODO
    this.x = x; // upper left corner
    this.y = y; // upper left corner
    this.w = w;
    this.h = h;
    this.default_x = x;
    this.default_y = y;
    this.default_w = w;
    this.default_h = h;
    this.content = "";
    this.group = -1;
    this.selected = false;
    this.editable = true;
    this.pre = false;
    this.jobid = -1;
    this.day = day;
    this.color = default_colors[this.day%2][this.id%2];
    this.defaultcolor = default_colors[this.day%2][this.id%2];
    if (this.special){
      this.color = default_special_colors[this.day%2][this.id%2];
      this.defaultcolor = default_special_colors[this.day%2][this.id%2];
    }
  }

  collides(x, y) {
    let ret = x > this.x && x < this.x + this.w && y > this.y && y < this.y + this.h;
    return ret;
  }

  set_new_coords(x, y, w, h){
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
  }

  set_default_coords(){
    this.x = this.default_x;
    this.y = this.default_y;
    this.w = this.default_w;
    this.h = this.default_h;
  }

  unset_coords(){
    this.x = false;
    this.y = false;
    this.w = false;
    this.h = false;
  }

  set_jobid(jid){
    this.jobid = jid;
  }

  set_pre(){
    this.pre = true;
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
      this.selected = true;
  }

  deselect(){
    this.color = this.defaultcolor;
    this.selected = false;
    this.show();
  }

  show() {
    stroke(255);
    strokeWeight(4);
    fill(this.color);
    rect(this.x, this.y, this.w, this.h);
  }
}


class Day{
  constructor(date, id, indb=false, name=null){
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
  let dns = [];
  for (const key in d){
    // console.log(`${key}: ${d[key]}`);
    let tmp = new Day(d[key], parseInt(key), indb=false);
    dns.push(tmp.name);
  }
}


class Job {
  constructor(id, name, start, dur, jobtype_id, special=false, indb=false){
    this.id = parseInt(id);
    this.name = name;
    this.start = start;
    this.end = start + dur;
    this.during = dur;
    this.start_day_id = days_arr[Math.floor(this.start/24)].id;
    if (this.end >= num_cols){
      this.end_day_id = days_arr[Math.floor(this.end/24)-1].id;
    }
    else{
      this.end_day_id = days_arr[Math.floor(this.end/24)].id;
    }

    this.dt_start = this.start % 24;
    this.dt_end = this.end % 24;
    this.special = special;
    this.jobtype_id = jobtype_id;
    this.indb = indb;
    job_instances.push(this);
    job_instances_id.set(this.id, this);
  }

  set_indb(){
    this.indb = true;
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
      fill(default_colors[0][0]);
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
      this.draw();
    }
    return;
  }
  else if (this.func.startsWith("delete")){
      if (this.state == 0){
        // console.log("set_del");
        jobtypes.get(parseInt(this.func.slice(6))).set_delete();
      }
      else{
        // console.log("unset_del");
        jobtypes.get(parseInt(this.func.slice(6))).unset_delete();
      }

  }
  this.state = !this.state;
  this.text = this.texts[+this.state];
  this.draw();
}

function generate_random_color(){
  let r;
  let g;
  let b;
  while ((r === g) && (r === b)){
    r = Math.floor(Math.random() * 156) + 100; // r is a random number between 100 - 255
    g = Math.floor(Math.random() * 156) + 100; // g is a random number betwen 100 - 255
    b = Math.floor(Math.random() * 156) + 100; // b is a random number between 100 - 255
    // let a = Math.random(200,255); // a is a random number between 200 - 255
  }

  return [r, g, b];
}

class Countbox{
  constructor(x, y, w, h){
    this.counter = 0;
    this.x = x;
    this.y = y;
    this.w = w;
    this.h = h;
    this.show_counter = false;
    this.show();
  }

  reset_counter(){
    this.counter = 0;
    this.show_counter = false;
  }

  count(){
    this.counter++;
    this.show_counter = true;
    this.show();
  }

  show(){
    fill(255, 255, 255);
    rect(this.x, this.y, this.w, this.h);
    if (this.show_counter){
      textSize(35);
      fill(0,0,0);
      textStyle(NORMAL);
      text(this.counter.toString(), this.x, this.y+this.h/2);
    }
  }
}
