#include "WaveletArray.h"
#include <MemoryFree.h>

const int RATE = 64; //Hertz
const int LEVELS = 7;
const int SCALE_FACTOR = 64; // raw input values can be scaled up by this factor for higher precision
const float LOW_CUTOFF = 0.4; // No frequencies below this
const float HIGH_CUTOFF = 8.0; // No frequencies above this

int data;
int lastRate;
boolean first;

// dwt variables, transformArray and temp used to be unsigned
WaveletArray rawInput;
int transformArray[WINDOWLENGTH] = {64, 74, 101, 140, 187, 224, 262, 315, 376, 428, 482, 538, 596, 646, 693, 757, 760, 760, 760, 760, 760, 760, 760, 760, 760, 767, 759, 758, 671, 525, 381, 283, 214, 167, 134, 114, 101, 95, 95, 94, 89, 87, 89, 90, 87, 84, 75, 63, 54, 48, 42, 39, 36, 33, 32, 31, 32, 32, 255, 40, 45, 57, 73, 93, 127, 172, 224, 281, 336, 393, 448, 501, 551, 592, 636, 680, 710, 724, 701, 628, 505, 367, 265, 194, 144, 109, 83, 65, 52, 43, 37, 32, 29, 26, 25, 23, 22, 22, 21, 21, 21, 21, 21, 21, 20, 20, 20, 20, 20, 20, 21, 21, 23, 24, 29, 255, 80, 122, 172, 228, 287, 349, 413, 468, 520, 573, 622, 677, 732, 760, 760, 760, 760, 677, 531, 382, 277, 255, 150, 113, 86, 67, 54, 45, 38, 33, 29, 27, 25, 25, 24, 24, 24, 24, 27, 26, 27, 28, 31, 36, 45, 64, 91, 125, 162, 205, 249, 286, 324, 370, 511, 475, 531, 580, 623, 667, 708, 749, 760, 760, 760, 759, 760, 760, 760, 722, 603, 439, 317, 231, 170, 127, 96, 74, 59, 48, 40, 34, 30, 28, 26, 24, 23, 22, 21, 21, 21, 21, 21, 20, 20, 20, 21, 23, 28, 39, 65, 106, 163, 234, 315, 399, 486, 572, 655, 736, 760, 767, 760, 760, 759, 759, 760, 760, 760, 760, 760, 760, 760, 759, 741, 602, 435, 314, 229, 169, 126, 96, 74, 255, 48, 40, 34, 30, 27, 25};
int temp[WINDOWLENGTH];
float freqs[LEVELS];
float freq_widths[LEVELS];
float powers[LEVELS];

void setup() {
  //set timer1 interrupt at 1Hz
  TCCR1A = 0;// set entire TCCR1A register to 0
  TCCR1B = 0;// same for TCCR1B
  TCNT1  = 0;//initialize counter value to 0
  // set compare match register for 1hz increments
  // denominator is timer frequency
  OCR1A = 15625/RATE-1;// = (16*10^6) / (RATE*1024) - 1 (must be <65536)
  // turn on CTC mode
  TCCR1B |= (1 << WGM12);
  // Set CS10 and CS12 bits for 1024 prescaler
  TCCR1B |= (1 << CS12) | (1 << CS10);  
  // enable timer compare interrupt
  TIMSK1 |= (1 << OCIE1A);
  
  Serial.begin(9600);
  Serial.print("fm: "); Serial.println(freeMemory());
  first = true;
  lastRate = 0;
  if(PRELOAD) {
    rawInput.loadArray(transformArray);
  }
}

// The data sampling is handled by the interrupt. Every time 
// enough samples have accumulated for one snapshot,
// copy to transformArray and call runTransform to find the heart rate
void loop() {
  if(PRELOAD && first) {
    Serial.println(runTransform());
  }
  
  if(first) {
    first = false;
  }
  
//    Serial.println(rawInput.getValue(rawInput.getLength() -1));
  if(rawInput.getLength() == WINDOWLENGTH) {
    noInterrupts();
    rawInput.getArray(transformArray);
    rawInput.newWindow();
    interrupts();
    int rate = runTransform();
    if(lastRate == 0 || abs(rate-lastRate) < 4) {
      lastRate = rate;
    } else if(rate > lastRate) {
      lastRate += 3;
    } else {
      lastRate -= 3;
    }
    Serial.println(lastRate);
  }
}

// Interrupt routine, runs at a frequency of RATE
ISR(TIMER1_COMPA_vect) {
  data = analogRead(A0);
  rawInput.appendValue(data);
}

// call several functions to determine the heart rate

// returns the calculated heart rate
int runTransform() {
  wavedec();
  decodeArray();
  return getRate();
//  Serial.println(getRate());
} 

// Perform a multilevel 1D discrete wavelet decomposition using the haar wavelet
// With some work this could be made to use a temp array of size WINDOWLENGTH / 2
void wavedec() {
  
  int length = WINDOWLENGTH >> 1;
  for(int i=0; i<LEVELS; i++) {
    for(int j=0; j<length; j++) {
      int sum = transformArray[j * 2] + transformArray[j * 2 + 1];
      int diff = transformArray[j * 2] - transformArray[j * 2 + 1];
      temp[j] = sum;
      temp[j + length] = diff;
//      transformArray[j] = sum;
//      temp[j] = diff;
    }
    
//    for(intj=length; j < length << 1; j++) {
//      transformArray[j] = temp[j-length];
//    }
    for(int j=0; j < length << 1; j++) {
      transformArray[j] = temp[j];
    }
    length >>= 1;
  }
  
}

// Extract meaningful information from the wavelet transform. Each level of the
// decomposition is assigned an average frequency and a power, which get placed
// in separate arrays
void decodeArray() {
  float nyquist = RATE / 2;
  for(int i=1; i<= LEVELS; i++) {
    float lower_limit = nyquist / power(2, LEVELS-i+1);
    float upper_limit = nyquist / power(2, LEVELS-i);
    freqs[i-1] = (lower_limit + upper_limit) / 2.0;
//    Serial.print("low: "); Serial.println(lower_limit);
//    Serial.print("upper: "); Serial.println(upper_limit);
//    Serial.print("freq: "); Serial.println(freqs[i-1]);
    if(i != 1) {
      freq_widths[i-1] = freqs[i-1] - freqs[i-2];
    }
    if(freqs[i-1] <= HIGH_CUTOFF && freqs[i-1] >= LOW_CUTOFF) {
      powers[i-1] = transformMean(i);
    } else {
      powers[i-1] = 0;
    }
    Serial.print("power: "); Serial.println(powers[i-1]);
  }
}

// Take the geometric center of the frequency vs. power plot 
// (as if it's a solid shape)

// returns the core frequency
int getRate() {
  float rate = 0;
  float numerator = 0;
  float denominator = 0;
  
  for(int i=1; i<LEVELS; i++) {
    numerator += float((power(freq_widths[i], 2) / 6.0) * (2.0 * powers[i] + powers[i-1]) * freq_widths[i]);
    delay(1); // Really really shouldn't need this but Arduino throws a weird error
    denominator += (freq_widths[i]/2.0) * (powers[i] + powers[i-1]) * freq_widths[i];
    Serial.print("N: "); Serial.println(numerator);
    Serial.print("D: "); Serial.println(denominator);
  }
  
  rate = numerator / denominator;
  return 60*rate;
}
  
// perform a basic exponent operation given the base and exponent
// return base^(exponent)
float power(float base, int exponent) {
  float result = 1;
  for(int i=0; i<exponent; i++) {
    result *= base;
  }
  return result;
}  

// find the average value of a section of the wave decomposition
// use the fact that each section is as long as all the sections before it 
// combined, and starts at position 2^(LEVELS-sectionIndex+1)

// sectionIndex: number of the section who's mean is to be calculated
// returns the average of the specified section
float transformMean(int sectionIndex) {
  int first = WINDOWLENGTH / power(2, LEVELS-sectionIndex+1); 
  int length = first;
  unsigned int sum = 0;
  for(int i=first; i<first+length; i++) {
    sum += abs(transformArray[i]);
  }
  float mean = sum / float(length);
//  Serial.print("tm: "); Serial.print(sectionIndex); Serial.print(", "); Serial.println(mean);
  return mean;
}

// calculate the raw mean of the transform array (should only be 
// called before wavedec, or results will be meaningless)

// returns the average value of the transform array
float rawMean() {
  long sum = 0;
  for(int i=0; i<WINDOWLENGTH; i++) {
    sum += transformArray[i];
  }
  float numSamples = WINDOWLENGTH;
  return sum/numSamples;
}
