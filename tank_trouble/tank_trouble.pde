public boolean hitbox = false;

PImage red;
PImage blue;

Tank p1;
Tank p2;
Bullet b = new Bullet(0, 0, 1, 1);


boolean akey = false;
boolean dkey = false;
boolean skey = false;
boolean wkey = false;
boolean qkey = false;

boolean hkey = false;
boolean jkey = false;
boolean kkey = false;
boolean ukey = false;
boolean ikey = false;

void setup() {
  size(800, 700);
  red = loadImage("red.jpg");
  blue = loadImage("blue.jpg");
  p1 = new Tank(200, 200, "red");
  p2 = new Tank(400, 400, "blue");
}


void draw() {
  background(255);
  p1.move(wkey, skey, akey, dkey);
  p1.shoot(qkey);
  p2.move(ukey, jkey, hkey, kkey);
  p2.shoot(ikey);
  p1.show();
  p2.show();
}

void keyPressed() {
  if (key == 'A' || key == 'a') {
    akey = true;
  } else if (key == 'D' || key == 'd') {
    dkey = true;
  } else if (key == 's' || key == 'S') {
    skey = true;
  } else if (key == 'w' || key == 'W') {
    wkey = true;
  } if (key == 'q' || key == 'q') {
    qkey = true;
  }
  if (key == 'h' || key == 'H') {
    hkey = true;
  } else if (key == 'k' || key == 'K') {
    kkey = true;
  } else if (key == 'j' || key == 'J') {
    jkey = true;
  } else if (key == 'u' || key == 'U') {
    ukey = true;
  } if (key == 'i' || key == 'I') {
    ikey = true;
  }
}

void keyReleased() {
    if (key == 'A' || key == 'a') {
    akey = false;
  } else if (key == 'D' || key == 'd') {
    dkey = false;
  } else if (key == 's' || key == 'S') {
    skey = false;
  } else if (key == 'w' || key == 'W') {
    wkey = false;
  } if (key == 'q' || key == 'q') {
    qkey = false;
  }
  if (key == 'h' || key == 'H') {
    hkey = false;
  } else if (key == 'k' || key == 'K') {
    kkey = false;
  } else if (key == 'j' || key == 'J') {
    jkey = false;
  } else if (key == 'u' || key == 'U') {
    ukey = false;
  } if (key == 'i' || key == 'I') {
    ikey = false;
  }
}
