// Communicating with Arduino
// Creating a txt file

import processing.serial.*;

Serial serialPort;
int counter;
String[] data;

void setup() {
//println(Serial.list()); // To see the ports
serialPort = new Serial(this, Serial.list()[1], 9600);
counter = 0;
data = new String[1300];
}

void draw() {
int temp = serialPort.read();

// If there is some input print it
if(temp != -1) {
println(counter + " " + temp);
data[counter] = counter + "," + temp;
counter++;
}

// if we reached 20min save text and exit
if(counter == 1300) {
saveStrings("thesis_data.txt", data);
exit();
}
}

//- See more at: http://ftmedia.eu/diy-gsr-sensor/#sthash.bRwkD8Nz.dpuf
