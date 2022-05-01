
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

let griditems = [];
let num_griditems = 0;

function setup() {
  createCanvas(windowWidth, windowHeight);
  col_width = (windowWidth - rowheaderwidth) / num_days;
  row_height = (windowHeight - headerheight) / num_jobs;
  ww = windowWidth;
  wh = windowHeight;
  grid = new Grid();

}


// function mousePressed() {
//   // inputcolorbutton.collides();
//
//   if (mouseButton === RIGHT) {
//     // Get the same color as a right-clicked circle.
//         for(var i=0; i<circles.length; i++){
//           if (circles[i].collides()){
//             colormode = i;
//             c[0] = circles[i].curr_color[0];
//             c[1] = circles[i].curr_color[1];
//             c[2] = circles[i].curr_color[2];
//             for (var s=0; s<sliders.length; s++){
//               sliders[s].set_pos(c[s]);
//             }
//           }
//       }
//       return;
//     }
//     if(mouseX <= tri_area_dim){
//       mode = 1;
//     }
//     else{
//       mode = 0;
//     }
//   if (mode == 0){
//     colormode = -1
//     for(let i = 0; i < sliders.length; i++) {
//       sliders[i].press();
//     }
//   }
//   else if (mode == 1){
//     console.log("in mode == 1");
//     for (var i=0; i<circles.length; i++){
//       if (circles[i].collides()){
//         circles[i].update();
//       }
//     }
//   }
//   colormode = -1
// }

function mousePressed() {
  for (let i = 0; i < num_jobs * num_days; i++) {
    griditems[i].clicked(mouseX, mouseY);
  }
}

// function mousePressed() {
//   // inputcolorbutton.collides();
//
//   if (mouseButton === RIGHT) {
//     // Get the same color as a right-clicked circle.
//         for(var i=0; i<circles.length; i++){
//           if (circles[i].collides()){
//             colormode = i;
//             c[0] = circles[i].curr_color[0];
//             c[1] = circles[i].curr_color[1];
//             c[2] = circles[i].curr_color[2];
//             for (var s=0; s<sliders.length; s++){
//               sliders[s].set_pos(c[s]);
//             }
//           }
//       }
//       return;
//     }
//     if(mouseX <= tri_area_dim){
//       mode = 1;
//     }
//     else{
//       mode = 0;
//     }
//   if (mode == 0){
//     colormode = -1
//     for(let i = 0; i < sliders.length; i++) {
//       sliders[i].press();
//     }
//   }
//   else if (mode == 1){
//     console.log("in mode == 1");
//     for (var i=0; i<circles.length; i++){
//       if (circles[i].collides()){
//         circles[i].update();
//       }
//     }
//   }
//   colormode = -1
// }

function draw() {
  // background(255);
  // print(col_width);
  // create_grid();
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
  }

  collides(x, y) {
    let ret = x > this.x && x < this.x + this.w && y > this.y && y < this.y + this.h
    return ret
  }

  clicked(x, y) {
    if (this.collides(x, y)) {
      this.color = "green";
      this.show();
      print("clicked." + this.id.toString());
    }
  }

  show() {
    stroke(255);
    strokeWeight(4);
    fill(255);
    rect(this.x, this.y, this.w, this.h);
    fill(this.color);
    rect(this.x, this.y, this.w, this.h);
    print("draw " + this.id.toString())
  }
}
