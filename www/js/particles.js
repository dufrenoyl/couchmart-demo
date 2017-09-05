var c = document.getElementById("activity");
var ctx = c.getContext("2d");



window.requestAnimFrame =
    window.requestAnimationFrame ||
    window.webkitRequestAnimationFrame ||
    window.mozRequestAnimationFrame ||
    window.oRequestAnimationFrame ||
    window.msRequestAnimationFrame ||
    function(callback) {
        window.setTimeout(callback, 1000 / 30);
};

NUM_CIRCLES=50;
MIN_DECAY_RATE = 0.005;
MAX_DECAY_RATE = 0.010;
MIN_SPEED=0.1
MAX_SPEED = 4
MIN_SIZE = 5
MAX_SIZE = 20

particles = []

palette = [{"red": 255, "green": 0, "blue": 0},
           {"red": 0, "green": 255, "blue": 0},
           {"red": 0, "green": 0, "blue": 255},
           {"red": 255, "green": 0, "blue": 255}]


var Particle = function(index){
  this.x = c.width/2;
  this.y = c.height/2;
  this.red = this.green = this.blue = 0;

  col_index = (index % palette.length);
  this.red = palette[col_index].red;
  this.green = palette[col_index].green;
  this.blue = palette[col_index].blue;


  var xdir = 0.5-Math.random();
  if (xdir < 0){
      this.xspeed = -MIN_SPEED - (Math.random() * (MAX_SPEED - MIN_SPEED));
  }
  else
  {
     this.xspeed = MIN_SPEED + (Math.random() * (MAX_SPEED - MIN_SPEED)); 
  }
  var ydir = 0.5-Math.random();
  if (ydir < 0){
      this.yspeed = -MIN_SPEED - (Math.random() * (MAX_SPEED - MIN_SPEED));
  }
  else
  {
     this.yspeed = MIN_SPEED + (Math.random() * (MAX_SPEED - MIN_SPEED)); 
  }
  this.yspeed = (0.5-Math.random()) * MAX_SPEED;
  this.size = MIN_SIZE + (Math.random() * (MAX_SIZE - MIN_SIZE));

  this.alpha = 1;
  this.decay = MIN_DECAY_RATE + (Math.random() * (MAX_DECAY_RATE - MIN_DECAY_RATE));
  this.index = index;

  this.draw = function(){
    ctx.fillStyle = 'rgba(' + this.red + ',' + this.green + ',' + this.blue + ',' + this.alpha+')';
    ctx.beginPath();
    ctx.arc(this.x, this.y, this.size, 0, Math.PI * 2);
    ctx.fill(); 
  }

  this.update = function(){
    this.alpha -= this.decay;

    if (this.x >= c.width || this.x <= 0 ||
        this.y >= c.height || this.y <= 0 ||
        this.alpha <= 0){
      particles[this.index] = new Particle(this.index);
    }
    this.x += this.xspeed;
    this.y += this.yspeed;
  }

};

  
function drawCircles(){  
  ctx.clearRect(0, 0, 600,400);
  for (i=0; i< NUM_CIRCLES;i++)
  {    
   particles[i].update();
   particles[i].draw();
  }
}

function loop() {
    drawCircles();
    requestAnimFrame(loop);
}

for (i=0; i< NUM_CIRCLES;i++)
{    
 particles[i] = new Particle(i);
}
loop();