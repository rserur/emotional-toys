int counter;
int incoming;
void setup() {
  Serial.begin(9600);
  counter = 0;
}

void loop() {
//  Serial.println(counter);
  incoming = Serial.read();
  Serial.println(incoming);
  counter++;
  delay(1000);
}
