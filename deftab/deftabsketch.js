let jobnames = ["Ordnung", "Springer", "Bar", "Amphitheaterbetreuung", "Alternativebetreuung", "Büro", "Finanzamt", "Wasser", "Technik"]
let num_jobs = jobnames.length;

let daynames = ["Freitag", "Samstag", "Sonntag"];
let num_days = daynames.length;

let num_cols = num_days * 24;
let headerheight = 30;
let rowheaderwidth = 100;
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

let selected = -1;
let row = -1;


function setup() {
  createCanvas(windowWidth, windowHeight);
  col_width = (windowWidth - rowheaderwidth) / (num_cols);
  row_height = (windowHeight - headerheight) / num_jobs;
  headertexty = headerheight / 2;
  let corrector = (col_width / 2) - txtsize / 2 -1;
  headertextx = rowheaderwidth + corrector;
  rowheadertexty = headerheight + row_height / 2;
  ww = windowWidth;
  wh = windowHeight;
  grid = new Grid();
}



function draw() {
  // background(255);

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
    this.make_colheaders();
    this.make_rowheaders();
  }

  make_data_row(y){
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

  assemble_grid(num_rows=num_jobs){
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
  constructor(id, x, y, w=col_width, h=row_height) {
    this.id = id
    this.x = x; // upper left corner
    this.y = y; // upper left corner
    this.w = w;
    this.h = h;
    this.content = "";
    if (this.id % 2 == 0){
      this.color = color(187, 186, 143);
    }
    else{
      this.color = color(170, 175, 91);
    }
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
