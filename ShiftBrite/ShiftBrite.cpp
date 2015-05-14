#include "ShiftBrite.h" //include the declaration for this class

#ifndef ShiftBrite_cpp
#define ShiftBrite_cpp

//Pinout for Shiftbrite
#define clockpin 13 // CI
#define enablepin 10 // EI
#define latchpin 9 // LI
#define datapin 11 // DI


boolean operator==(const Color &a, const Color &b)
{
  boolean ret = true;
  ret = ret && (a.r == b.r);
  ret = ret && (a.g == b.g);
  ret = ret && (a.b == b.b);
  ret = ret && (a.name == b.name);
  return ret; 
}
boolean operator!=(const Color &a, const Color &b)
{
  boolean ret = false;
  ret = ret || (a.r != b.r);
  ret = ret || (a.g != b.g);
  ret = ret || (a.b != b.b);
  ret = ret || (a.name != b.name);
  return ret; 
}

ShiftBrite::ShiftBrite() {
 
   pinMode(datapin, OUTPUT);
   pinMode(latchpin, OUTPUT);
   pinMode(enablepin, OUTPUT);
   pinMode(clockpin, OUTPUT);
   //SPCR = (1<<SPE)|(1<<MSTR)|(0<<SPR1)|(0<<SPR0);
   digitalWrite(latchpin, LOW);
   digitalWrite(enablepin, LOW);
   setDefaults();
   initArrays();
   defineColors();
   randomSeed(analogRead(0));
}

ShiftBrite::ShiftBrite(int num) {
 
   pinMode(datapin, OUTPUT);
   pinMode(latchpin, OUTPUT);
   pinMode(enablepin, OUTPUT);
   pinMode(clockpin, OUTPUT);
   //SPCR = (1<<SPE)|(1<<MSTR)|(0<<SPR1)|(0<<SPR0);
   digitalWrite(latchpin, LOW);
   digitalWrite(enablepin, LOW);
   _NumLEDs = num;
   initArrays();
   defineColors();
   randomSeed(analogRead(0));
}

ShiftBrite::~ShiftBrite(){
  //Nothing to destruct
}

void ShiftBrite::setDefaults(){
  _NumLEDs = 4; 
}

void ShiftBrite::initArrays(){
  int x = 0;
  for(int i = 0; i < 4; i++){
    for(int j = 0; j< 3; j++){
    if (i >= _NumLEDs){
        x = -1;
    }
    LEDChannels[i][j] = x;
    }
   }
   for (int i = 0; i < numColors; i++){
     colors_in_use[i] = 0;
   }
}

void ShiftBrite::defineColors(){
//Predefined colors
//the number of predefined colors, numColors, is set in ShiftBrite.h
//If adding new colors, change numColors and add new cases to ShiftBrite::_getColor()
  red.r = 1200;
  red.g = 0;
  red.b = 0;
  red.name = "red";
  colors[0] = red;
  blue.r = 0;
  blue.g = 0;
  blue.b = 1200;
  blue.name = "blue";
  colors[1] = blue;
  green.r = 0;
  green.g = 1200;
  green.b = 0;
  green.name = "green";
  colors[2] = green;
  purple.r = 600;
  purple.g = 0;
  purple.b = 600;
  purple.name = "purple";
  colors[3] = purple;
  yellow.r = 600;
  yellow.g = 600;
  yellow.b = 0;
  yellow.name = "yellow";
  colors[4] = yellow;
  teal.r = 0;
  teal.g = 700;
  teal.b = 700;
  teal.name = "teal";
  colors[5] = teal;
  // Users should add their own colors below this line

  
  // All user colors should be defined above this line
  // Set empty color
  empty.r = 0;
  empty.g = 0;
  empty.b = 0;
  empty.name = "empty";
}

// communication
void ShiftBrite::SB_SendPacket() {
 
    if (SB_CommandMode == B01) {
     // power from 0 - 127
     SB_RedCommand = 80; 
     SB_GreenCommand = 70;
     SB_BlueCommand = 70;
    }
   
    /*SPDR = SB_CommandMode << 6 | SB_BlueCommand>>4;
    while(!(SPSR & (1<<SPIF))) /*Serial.println(1)/;
    SPDR = SB_BlueCommand<<4 | SB_RedCommand>>6;
    while(!(SPSR & (1<<SPIF))) /*Serial.println(2)/;
    SPDR = SB_RedCommand << 2 | SB_GreenCommand>>8;
    while(!(SPSR & (1<<SPIF))) /*Serial.println(3)/;
    SPDR = SB_GreenCommand;
    while(!(SPSR & (1<<SPIF))) /*Serial.println(4)/;*/
    unsigned long SB_CommandPacket = SB_CommandMode & B11;
    SB_CommandPacket = (SB_CommandPacket << 10) | (SB_BlueCommand & 1023);
    SB_CommandPacket = (SB_CommandPacket << 10) | (SB_RedCommand & 1023);
    SB_CommandPacket = (SB_CommandPacket << 10) | (SB_GreenCommand & 1023);
    
    shiftOut(datapin, clockpin, MSBFIRST, SB_CommandPacket >> 24);
    shiftOut(datapin, clockpin, MSBFIRST, SB_CommandPacket >> 16);
    shiftOut(datapin, clockpin, MSBFIRST, SB_CommandPacket >> 8);
    shiftOut(datapin, clockpin, MSBFIRST, SB_CommandPacket);
}

void ShiftBrite::turnOff(int num){
  setColor(num, empty);
}
 
void ShiftBrite::WriteLEDArray() {
   //Serial.println("writing led array");
    SB_CommandMode = B00; // Write to PWM control registers
    // Sets the color
    for (int h = 0;h < _NumLEDs; h++) {
	  SB_RedCommand = LEDChannels[h][0];
	  SB_GreenCommand = LEDChannels[h][1];
	  SB_BlueCommand = LEDChannels[h][2];
	  SB_SendPacket();
    }
 
    delayMicroseconds(15);
    digitalWrite(latchpin,HIGH); // latch data into registers
    delayMicroseconds(15);
    digitalWrite(latchpin,LOW);
 
    SB_CommandMode = B01; // Write to current control registers
    // Sets the power (brightness)
    for (int z = 0; z < _NumLEDs; z++) SB_SendPacket();
    delayMicroseconds(15);
    digitalWrite(latchpin,HIGH); // latch data into registers
    delayMicroseconds(15);
    digitalWrite(latchpin,LOW); 
}

void ShiftBrite::setRgbVal(int num, char channel, int val){
  val = constrain(val, 0, 1023);
  if (num >=0 && num < _NumLEDs){
    switch(channel){
      case 'r':
        LEDChannels[num][0] = val;
        break;
      case 'g':
        LEDChannels[num][1] = val;
        break;
      case 'b':
        LEDChannels[num][2] = val;
        break;
      default:
        break;
    }
  }
}

void ShiftBrite::setColor(int num, Color color){
  int rgb[3];
  rgb[0] = color.r;
  rgb[1] = color.g;
  rgb[2] = color.b;
  if (num >= 0 && num <= _NumLEDs){
    for(int i = 0; i < 3; i++){
      rgb[i] = constrain(rgb[i],0,1023);
      LEDChannels[num][i] = rgb[i];
    }
    WriteLEDArray();
  }
}

void ShiftBrite::setColor(int num, String color){
  
  Color rgb;
  rgb = _getColor(color);
  setColor(num, rgb);
}

void ShiftBrite::setColor_rand(int num){
  Color rgb;
  rgb = randomColor();
  setColor(num, rgb);
}

Color ShiftBrite::randomColor()
{
  int rand = random(numColors); //random number between 0 and numColors
  return _getColor(rand);
}

void ShiftBrite::set(int* rgb, int* desired)
{
  for(int i = 0; i < 3; i++)
  {
    rgb[i] = desired[i];
  }
}

Color ShiftBrite::_getColor(int index)
{
  Color rgb;
  switch(index)
  {
     case 0:
       rgb = red;
       break;
     case 1:
       rgb = blue;
       break;
     case 2:
       rgb = green;
       break;
     case 3:
       rgb = purple;
       break;
     case 4:
       rgb = yellow;
       break;
     case 5:
       rgb = teal;
       break;
     default:
       rgb = empty;
       break; 
 }
 return rgb;
}

Color ShiftBrite::_getColor(String color)
{
  boolean found = false;
  int i = 0;
  for(i = 0; i < numColors; i++){
    if(color == colors[i].name)
    {
     found = true;
     break;
    }
  }
 if (found)
   return _getColor(i);
 else
  return _getColor(-1);
}

Color ShiftBrite::getColor(){
  return randomColor();
}

void ShiftBrite::getColors(int colors[][3])
{
  int num = 0;
  Color thisColor;
  for(int i = 1; i < numColors+1; i++){
    if(!colors_in_use[i]){
      num++;
      thisColor = _getColor(i);
      colors[i][0] = thisColor.r;
      colors[i][1] = thisColor.g;
      colors[i][2] = thisColor.b;
    }
    else{
      for(int j = 0; j < 3; j++){
        colors[i][j] = -1;
      }
    }
  }
  colors[0][0] = num;
}

int ShiftBrite::_colorIndex(Color rgb)
{
 Color temp;
 for(int i = 0; i < numColors; i++){
  temp = _getColor(i);
  if(rgb == temp)
    return i;
 }
 return -1;
}

/*String ShiftBrite::colorName(int* rgb)
{
  int index = _colorIndex(rgb);
  if(index >= 0)
    return names[index];
  
  return "Not a prefined color";
}*/
/* 
void loop() {
 
   LEDChannels[0][0] = 1023;
   LEDChannels[0][1] = 0;
   LEDChannels[0][2] = 0;
 
   LEDChannels[1][0] = 0;
   LEDChannels[1][1] = 0;
   LEDChannels[1][2] = 1023;
 
   WriteLEDArray();
   delay(200);
 
   LEDChannels[0][0] = 0;
   LEDChannels[0][1] = 0;
   LEDChannels[0][2] = 1023;
 
   LEDChannels[1][0] = 1023;
   LEDChannels[1][1] = 0;
   LEDChannels[1][2] = 0;
 
   WriteLEDArray();
   delay(200);
 
 
}*/

#endif
