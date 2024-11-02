#define ModePin 6
#define ClickPin 2
#define YPin A3
#define XPin A4

int lastX = 0;
int lastY = 0;

void setup() {
  pinMode(XPin, INPUT);
  pinMode(YPin, INPUT);
  pinMode(ClickPin, INPUT_PULLUP);
  pinMode(ModePin, INPUT);

  Serial.begin(115200);
  Serial.setTimeout(1);
}

void loop() {
  int x = analogRead(XPin) - 517;
  int y = analogRead(YPin) - 507;

  x = x < 10 && x > -10 ? 0 : x; 
  y = y < 10 && y > -10 ? 0 : y; 
  
  int diffX = x - lastX;
  int diffY = y - lastY;
  if (diffX < 5 && diffX > -5) {
    x = lastX;
  } else {
    lastX = x;
  }
  if (diffY < 5 && diffY > -5) {
    y = lastY;
  } else {
    lastY= y;
  }
  int click = digitalRead(ClickPin) == HIGH ? 0 : 1;
  int mode = digitalRead(ModePin) == HIGH ? 1 : 0;
  Serial.print(x);
  Serial.print(":");
  Serial.print(y);
  Serial.print(":");
  Serial.print(click);
  Serial.print(":");
  Serial.println(mode);
  
}
