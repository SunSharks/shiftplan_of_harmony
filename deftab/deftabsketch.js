
let num_days = 3;
let num_jobs = 8;
let headerheight = 20;
let rowheaderwidth = 60;
// col_width;
// row_height;
let col_width;
let row_height;
let ww;
let wh;

let grid;
let griditems = [];
let num_griditems = 0;

let curr_color = "blue";


function setup() {
  createCanvas(windowWidth, windowHeight);
  col_width = (windowWidth - rowheaderwidth) / num_days;
  row_height = (windowHeight - headerheight) / num_jobs;
  ww = windowWidth;
  wh = windowHeight;
  grid = new Grid();
}


let selected = -1;
let row = -1;
function draw() {
  // background(255);
  // print(col_width);
  // create_grid();

  if (mouseIsPressed){

    for (var i=0; i<griditems.length; i++){
      if (griditems[i].collides(mouseX, mouseY)){
        if(row == -1){
          row = Math.floor(i/grid.cols.length)
        }
        if (row == Math.floor(i/grid.cols.length)){
          griditems[i].set_color(curr_color);
          griditems[i].select();
        }
      }
    }
  }
}


function mouseReleased() {
    curr_color = grid.generate_random_color();
    row = -1;
}


class Grid {
  constructor(){
    this.rows = [];
    this.cols = [];
    this.assemble_grid();
  }

  make_data_row(y, num_cols=num_days){
    let x = rowheaderwidth;
    let l = [];
    for (let i=0; i<num_cols; i++){
      let r = new Griditem(num_griditems, x, y);
      num_griditems += 1;
      r.show();
      griditems.push(r);
      l.push(r);
      x += col_width;
    }
    this.rows.push(l);
  }

  assemble_grid(num_rows=num_jobs, num_cols=num_days){
    let y = headerheight;
    for (let i=0; i<num_rows; i++){
      this.make_data_row(y);
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
    let g = random(100,200); // g is a random number betwen 100 - 200
    let b = random(100); // b is a random number between 0 - 100
    let a = random(200,255); // a is a random number between 200 - 255
    return color(r, g, b, a)
  }

}

class Griditem {
  constructor(id, x, y, w=col_width, h=row_height) {
    this.id = id
    this.x = x; // upper left corner
    this.y = y; // upper left corner
    this.w = w;
    this.h = h;
    this.content = "";
    this.color = "red";

    this.pressed = false;
    this.mouse_over = false;
    this.can_hold = true;
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

  select(x, y) {
      this.show();
      print("selected." + this.id.toString());
      print(this.color)

  }

  // press(){
  //   if(this.mouse_over) {
  //     this.pressed = true;
  //   }
  // }


  show() {
    stroke(255);
    strokeWeight(4);
    // fill(255);
    // rect(this.x, this.y, this.w, this.h);
    fill(this.color);
    rect(this.x, this.y, this.w, this.h);
    print("draw " + this.id.toString())
  }


}
