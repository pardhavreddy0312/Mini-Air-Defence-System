import processing.serial.*;

Serial myPort;

PFont f;

int Angle = 0;
int Distance = 0;

float pixsDistance;

String portName = "COM11";

boolean blink = false;
int blinkTimer = 0;

void setup(){

  size(1250,700);

  smooth();

  f = createFont("Arial Bold",30);

  textFont(f);

  println(Serial.list());

  myPort = new Serial(this, portName, 115200);

  myPort.bufferUntil('\n');
}

void draw(){

  background(0);

  greenMesh();

  radarArea();

  greenLine();

  targetDot();

  infoText();
}

void serialEvent(Serial port){

  String line = port.readStringUntil('\n');

  if(line == null)
    return;

  line = trim(line);

  println(line);

  if(!line.startsWith("scan"))
    return;

  int aIndex = line.indexOf("a=");
  int dIndex = line.indexOf("d=");

  if(aIndex == -1 || dIndex == -1)
    return;

  String angleStr = line.substring(aIndex+2,dIndex).trim();

  String distStr = line.substring(dIndex+2).trim();

  Angle = int(angleStr);

  Distance = int(distStr);
}

void greenMesh(){

  stroke(98,245,31,40);

  strokeWeight(1);

  for(int i=0;i<height;i+=10)
    line(0,i,width,i);

  for(int i=0;i<width;i+=10)
    line(i,0,i,height);
}

void radarArea(){

  pushMatrix();

  translate(width/2,height*0.98);

  noFill();

  strokeWeight(2);

  stroke(98,245,31);

  arc(0,0,1150,1150,PI,TWO_PI);
  arc(0,0,850,850,PI,TWO_PI);
  arc(0,0,550,550,PI,TWO_PI);
  arc(0,0,250,250,PI,TWO_PI);

  for(int i=0;i<=180;i+=30){

    line(
      0,
      0,
      -600*cos(radians(i)),
      -600*sin(radians(i))
    );
  }

  popMatrix();
}

void greenLine(){

  pushMatrix();

  translate(width/2,height*0.98);

  strokeWeight(6);

  stroke(30,250,60);

  float x = -600*cos(radians(Angle));

  float y = -600*sin(radians(Angle));

  line(0,0,x,y);

  popMatrix();
}

void targetDot(){

  if(Distance <= 0 || Distance > 80)
    return;

  pushMatrix();

  translate(width/2,height*0.98);

  pixsDistance = map(Distance,0,80,0,600);

  float x = -pixsDistance*cos(radians(Angle));

  float y = -pixsDistance*sin(radians(Angle));

  if(millis() - blinkTimer > 300){

    blink = !blink;

    blinkTimer = millis();
  }

  if(blink){

    stroke(255,0,0);

    strokeWeight(12);

    point(x,y);
  }

  popMatrix();
}

void infoText(){

  fill(255);

  textSize(30);

  text("Auto Turret Radar",20,40);

  text("Angle : "+Angle+"°",20,80);

  text("Distance : "+Distance+" cm",20,120);

  text("Press F to FIRE",20,160);
}

void keyPressed(){

  if(key=='f' || key=='F'){

    println("Fire at angle: "+Angle);

    String cmd = "A"+Angle+"\n";

    myPort.write(cmd);
  }
}
