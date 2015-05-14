// GSR sensor variables
int sensorPin = 0; // select the input pin for the GSR
int sensorValue; // variable to store the value coming from the sensor

// Time variables
unsigned long time;
double secForGSR;
int curMillisForGSR;
int preMillisForGSR;

const int R = 10000;
double voltage;
double resistance;
double conductivity;

void setup() {
// Prepare serial port
Serial.begin(9600);
secForGSR = .1; // How often do we get a GSR reading
curMillisForGSR = 0;
preMillisForGSR = -1;
}
void loop() {
time = millis();

curMillisForGSR = time / (secForGSR * 1000);
if(curMillisForGSR != preMillisForGSR) {
// Read GSR sensor and send over Serial port
sensorValue = analogRead(sensorPin);
voltage = map(sensorValue,0,1023,0,500);
voltage /= 100;
resistance = (5/voltage)*R-R;
conductivity = 1000000/resistance;
Serial.println(sensorValue);
preMillisForGSR = curMillisForGSR;
}
}

//- See more at: http://ftmedia.eu/diy-gsr-sensor/#sthash.7X3gjuv5.dpuf
