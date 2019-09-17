class Tank {
  public int x;
  public int y;
  public String c;
  public int h;
  public int w;
  public String dir;
  public float rotate;
  public int rotation_zone = 0;
  public int speed = 2;
  public Bullet b1 = new Bullet(0, 0, 0, 0);

  public PImage sprite;

  Tank(int x, int y, String c) {
    this.x = x;
    this.y = y;
    this.c = c;
    this.w = 40;
    this.h = 60;
    this.dir = "u";
    this.rotate = 0;
    if (c == "red") {
      this.sprite = red;
    } else {
      this.sprite = blue;
    }
  }

  void shoot(boolean s) {
    PVector v = new PVector(0, 0);
    PVector off = new PVector(0, 0);
    if (s) {
      if (this.dir == "u") {
        v = new PVector(0, -4);
        off = new PVector(this.w/2, 0);
      } else if (this.dir == "d") {
        v = new PVector(0, 4);
        off = new PVector(this.w/2, this.h);
      } else if (this.dir == "l") {
        v = new PVector(-4, 0);
        off = new PVector(0, this.h/2);
      } else if (this.dir == "r") {
        v = new PVector(4, 0);
        off = new PVector(this.w, this.h/2);
      }
      b1 = new Bullet(this.x + off.x, this.y + off.y, v.x, v.y);
    }
  }

  void move(boolean up, boolean down, boolean left, boolean right) {
    if (up) {
      this.y-=this.speed;
      this.dir = "u";
      if (this.rotate > 180 + rotation_zone) {
        this.rotate-=10;
      } else if (this.rotate < 180 + rotation_zone) {
        this.rotate+=10;
      }
    } else if (down) {
      this.y+=this.speed;
      this.dir = "d";
      if (this.rotate > 0 + rotation_zone) {
        this.rotate-=10;
      } else if (this.rotate < 0 + rotation_zone) {
        this.rotate+=10;
      }
    } else if (left) {
      this.x-=this.speed;
      this.dir = "l";
      if (this.rotate > 90 + rotation_zone) {
        this.rotate-=10;
      } else if (this.rotate < 90 + rotation_zone) {
        this.rotate+=10;
      }
    } else if (right) {
      this.x+=this.speed;
      this.dir = "r";
      if (this.rotate > 270 + rotation_zone) {
        this.rotate-=10;
      } else if (this.rotate < 270 + rotation_zone) {
        this.rotate+=10;
      }
    }
  }

  void show() {
    pushMatrix();
    translate(this.x + (this.w / 2), this.y + (this.h / 2));
    rotate(radians(this.rotate));
    image(this.sprite, -this.w/2, -this.h/2, this.w, this.h);
    popMatrix();
    b1.show();
  }
}
