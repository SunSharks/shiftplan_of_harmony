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


function setup() {
  createCanvas(windowWidth, windowHeight);
  col_width = (windowWidth - rowheaderwidth) / num_days;
  row_height = (windowHeight - headerheight) / num_jobs;
  ww = windowWidth;
  wh = windowHeight;
}


function mousePressed() {
  // inputcolorbutton.collides();

  if (mouseButton === RIGHT) {
    // Get the same color as a right-clicked circle.
        for(var i=0; i<circles.length; i++){
          if (circles[i].collides()){
            colormode = i;
            c[0] = circles[i].curr_color[0];
            c[1] = circles[i].curr_color[1];
            c[2] = circles[i].curr_color[2];
            for (var s=0; s<sliders.length; s++){
              sliders[s].set_pos(c[s]);
            }
          }
      }
      return;
    }
    if(mouseX <= tri_area_dim){
      mode = 1;
    }
    else{
      mode = 0;
    }
  if (mode == 0){
    colormode = -1
    for(let i = 0; i < sliders.length; i++) {
      sliders[i].press();
    }
  }
  else if (mode == 1){
    console.log("in mode == 1");
    for (var i=0; i<circles.length; i++){
      if (circles[i].collides()){
        circles[i].update();
      }
    }
  }
  colormode = -1
}

function mousePressed() {
  for (let i = 0; i < bubbles.length; i++) {
    bubbles[i].clicked(mouseX, mouseY);
  }
}


function create_grid(){
  let x = 0;
  let y = headerheight;
  for(let i=0; i<num_jobs; i++){
    line(x, y, ww, y)
    y += row_height;
  }
  x = rowheaderwidth;
  y = 0;
  for(let i=0; i<num_days; i++){
    line(x, 0, x, wh)
    x += col_width;
  }

}

function draw() {
  background(255);
  // print(col_width);
  create_grid();
}


class Griditem {
  constructor(x, y, w=col_width, h=row_height) {
    this.x = x; // upper left corner
    this.y = y; // upper left corner
    this.w = w;
    this.h = h;
    this.content = "";
  }

  isin(x, y) {
    let ret = x > this.x && x < this.x + this.w && y > this.y && y < this.y + this.h
    return ret
  }

  clicked(x, y) {
    if (isin(x, y)) {
      this.color = 255;
    }
  }

  move() {
    this.x = this.x + random(-2, 2);
    this.y = this.y + random(-2, 2);
  }

  show() {
    stroke(255);
    strokeWeight(4);
    fill(this.brightness, 125);
    ellipse(this.x, this.y, this.r * 2);
  }
}
