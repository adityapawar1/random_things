import processing.serial.*;

public int global_ground = 460; // the ground
public int scroll_speed = 4; // scrolling speed (pixels per frame)
public boolean hitbox = false;

public class Dino { // class for dino (character)
  public int animation_index = -1;
  public boolean duck = false;
  public int prevmil = 0;
  public int x = 0;
  public int y = 0;
  public int h = 0;
  public int w = 0;
  public int ground = 0;
  public boolean jump_mode = false;
  public int jump_speed = 6;
  public int basew = 0;
  public int baseh = 0;
  int count = 0;

  public Dino(int x, int y, int h, int w) { // init
    this.x = x;
    this.y = y;
    this.h = h;
    this.baseh = h;
    this.w = w;
    this.basew = w;
    this.ground = y;
  }

  public void show() { // draws dino
    if (millis() - this.prevmil > 100) {
      if (!(this.animation_index+1 >= 3)) {
        this.animation_index += 1;
      } else {
        this.animation_index = 0;
      }
      this.prevmil = millis();
    }
    push();
    noFill();
    stroke(0);
    if (!this.duck) {
      // println(this.animation_index);
      if (hitbox) {
        rect(this.x - 1, this.y - 1, this.w + 1, this.h + 1);
      }
      dinosaur_animation[this.animation_index].resize(this.w, this.h);
      image(dinosaur_animation[this.animation_index], this.x, this.y);
    } else {
      if (hitbox) {
        rect(this.x - 1, this.y - 1, this.w + 1, this.h + 1);
      }
      dinosaur_crouch.resize(this.w, this.h);
      image(dinosaur_crouch, this.x, this.y);
    }
    pop();
  }

  public void reset() { // so dino does not get stuck in duck mode
    this.h = this.baseh;
    this.w = this.basew;
    this.y = global_ground - this.h;
    this.duck = false;
  }

  public void duck() { // for ducking
    if (this.y <= this.ground - 60) { // if in air, go to the ground
      this.y += jump_speed + 1;
    } else { // duck 'animation'
      this.h = 30;
      this.w = 60;
      this.y = global_ground - this.h;
      this.duck = true;
    }
  }

  public boolean jump(int h) { // for jumping
    this.duck = false;
    if (this.y >= this.ground && this.jump_mode) {
    } else if (this.y > this.ground - h && !this.jump_mode) {
      // going up
      this.y -= this.jump_speed;
      return true;
    } else if (this.y < this.ground - h || this.jump_mode) {
      // going down
      this.jump_mode = true;
      this.y += this.jump_speed;
      return true;
    }
    this.jump_mode = false;
    count = 0;
    return false;
  }
}

public class Obstacle {
  public int x = 0;
  public int y = 0;
  public boolean[] height_; // saves whether obstacle is "big" or "small" 
  public boolean bird;
  public boolean use = false; // if this object is being used
  public int w = 0;

  Obstacle(int x, boolean[] height_) { // actual init
    this.x = x;
    this.y = global_ground;
    this.height_ = height_;
    this.use = true;
    // this.bird = bird;
  }
  Obstacle(boolean temp) { // for intilizing objects
  }

  public void show() {
    if (this.use) {
      int count = 0;
      if (!this.bird) {

        for (boolean obstacle_height : this.height_) {
          count++;
          if (obstacle_height) { // big cactus
            push();
            fill(0, 255, 0);
            noStroke();
            if (hitbox) {
              rect(this.x + count - 1, this.y - 45 - 1, 20 + 1, 45 + 1);
            }
            cactus_sprite.resize(20, 45);
            image(cactus_sprite, this.x + count, this.y - 45);
            pop();
            count += 20;
          } else { // small cactus
            push();
            fill(0, 255, 0);
            noStroke();
            if (hitbox) {
              rect(this.x + count - 1, this.y - 25 - 1, 10 + 1, 25 + 1);
            }
            cactus_sprite.resize(10, 25);
            image(cactus_sprite, this.x + count, this.y - 25);
            pop();
            count += 10;
          }
        }
        this.w = count;
      } else {
        // bird code goes here
      }
      if (this.x >= -60) {
        this.x -= scroll_speed; // if obstacle is not on screen, change use to false
      } else {
        this.use = false;
      }
    }
  }
}

int score = 0;

// obstacles
Obstacle obstacle1 = new Obstacle(false);
Obstacle obstacle2 = new Obstacle(false);
Obstacle obstacle3 = new Obstacle(false);
Obstacle obstacle4 = new Obstacle(false);

Dino dino = new Dino(60, 400, 60, 45);

// for jumping and ducking
boolean wkey;
boolean skey;

// if dino is currently jumping
boolean jump = false;

// obstacle random constants
int obstacle_chance = 3;
int obstacle_rate = 1000;
int speed_up = 60; // add to speed every x score

// used to see when to place new obstacle
int prevMillis = 0;

int startMillis = 0;

PImage[] dinosaur_animation = new PImage[4];
PImage cactus_sprite;
PImage dinosaur_crouch;

void setup() { // make screen
  size(800, 600);
  dinosaur_crouch = loadImage("dino_crouch1.jpg");
  dinosaur_animation[0] = loadImage("dino1.jpg");
  dinosaur_animation[1] = loadImage("dino2.jpg");
  dinosaur_animation[2] = loadImage("dino3.jpg");
  dinosaur_animation[3] = loadImage("dino4.jpg");
  
  cactus_sprite = loadImage("cactus.jpg");
}

void draw() {

  if (!checkDeath()) {
    resetScreen(); // resets screen and draws the ground

    checkJump(); // checks is w or s is pressed

    createObstacle();

    showScore();

    show();
  } else {
    textSize(48);
    fill(100);
    text("Game Over!", width / 2 - 150, height / 2 - 200);
  }
}

boolean checkDeath() {
  if (!(obstacle1.x >= dino.x + dino.w && dino.x <= obstacle1.w + obstacle1.x) && obstacle1.x >= 30) {
    if (!(dino.y + dino.h <= global_ground - 25)) {
      //println("Game Over!");
      return true;
    }
  } else if (!(obstacle2.x >= dino.x + dino.w && dino.x <= obstacle2.w + obstacle2.x) && obstacle2.x >= 30) {
    if (!(dino.y + dino.h <= global_ground - 25)) {
      //println("Game Over!");
      return true;
    }
  } else if (!(obstacle3.x >= dino.x + dino.w && dino.x <= obstacle3.w + obstacle3.x) && obstacle3.x >= 30) {
    if (!(dino.y + dino.h <= global_ground - 25)) {
      //println("Game Over!");
      return true;
    }
  } else if (!(obstacle4.x >= dino.x + dino.w && dino.x <= obstacle4.w + obstacle4.x) && obstacle4.x >= 30) {
    if (!(dino.y + dino.h <= global_ground - 25)) {
      //println("Game Over!");
      return true;
    }
  }
  return false;
}

void showScore() {
  textSize(32);
  fill(0);
  score = int(millis() - startMillis)/100;
  text("Score: " + str(score), 600 / 2 - 75, 30);
  scroll_speed = (score / speed_up) + 4;
  if (1000 - (score / 20) > 250) {
    obstacle_rate = 1000 - (score / 20);
    cactus_sprite = loadImage("cactus.jpg");
  }
  if (score >= 300) {
    obstacle_chance = 2;
  }
  // println(obstacle_rate);
}

void show() {
  try {
    obstacle1.show();
    obstacle2.show();
    obstacle3.show();
    obstacle4.show();
  } 
  catch(Exception e) {
    println(e);
  }
  dino.show();
}

void createObstacle() {
  if (millis() - prevMillis >= obstacle_rate) { // if its time to create obstacle
    if (int(random(0, obstacle_chance)) == 0) {
      println("creating abstacle");
      try {
        int array_size = int(random(1, 5));
        boolean[] heights = new boolean[array_size];
        for (int i = 0; i < array_size; i++) {
          heights[i] = random(0, 1) < 0.5; // make height array for object
        }
        // println(heights);
        if (!obstacle1.use) { // if this obstcle is not being used, make one
          obstacle1 = new Obstacle(width, heights);
        } else if (!obstacle2.use) {
          obstacle2 = new Obstacle(width, heights);
        } else if (!obstacle3.use) {
          obstacle3 = new Obstacle(width, heights);
        } else if (!obstacle4.use) {
          obstacle4 = new Obstacle(width, heights);
        }
      }
      catch (Exception e) {
        println(e);
      }
    }
    prevMillis = millis();
  }
}

void checkJump() {
  if (wkey && !jump) {
    jump = true;
    dino.reset();
  }
  if (jump) {

    jump = dino.jump(110);
  } 
  if (skey) {
    dino.duck();
    jump = false;
  } else if (!jump) {
    dino.reset();
    // dinosaur_animation[dino.animation_index] = loadImage("dino" + Integer.toString(dino.animation_index - 1) + ".jpg");
  }
}

void resetScreen() {
  background(255);
  push();
  stroke(0);
  line(0, global_ground, width, global_ground);
  pop();
}


void keyPressed() {
  if (key == 'w' || key == 'W') {
    wkey = true;
  }
  if (key == 's' || key == 'S') {
    skey = true;
  }
}

void keyReleased() {
  if (key == 'w' || key == 'W') {
    wkey = false;
  }
  if (key == 's' || key == 'S') {
    skey = false;
  }
  if ((key == 'r' || key == 'K') && checkDeath()) {
    gameReset();
  }
}

void gameReset() {
  obstacle1 = new Obstacle(false);
  obstacle2 = new Obstacle(false);
  obstacle3 = new Obstacle(false);
  obstacle4 = new Obstacle(false);
  score = 0;
  jump = false;
  startMillis = millis();
  dinosaur_animation[0] = loadImage("dino1.jpg");
  dinosaur_animation[1] = loadImage("dino2.jpg");
  dinosaur_animation[2] = loadImage("dino3.jpg");
  dinosaur_animation[3] = loadImage("dino4.jpg");
}
