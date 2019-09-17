class Bullet {
  public float x;
  public float y;
  public boolean use = false;
  public float xdir;
  public float ydir;

  Bullet(float x, float y, float xdir, float ydir) {
    this.x = x;
    this.y = y;
    this.xdir = xdir;
    this.ydir = ydir;
  }
  void show() {
    fill(0);
    if (this.xdir + this.ydir != 0) {
      circle(this.x, this.y, 10);
      this.x += this.xdir;
      this.y += this.ydir;
    } else {
      this.use = true;
    }

  }
}
