// Define a circular array with functionality specifically designed for the
// wavelet transform-based heart rate monitor

#ifndef WaveletArray_h
#define WaveletArray_h

#include "Arduino.h"
    
const int WINDOWLENGTH = 256;
const int WINDOWDIFF = 64;
const int NOISE_FILTER = 100;

class WaveletArray {
  public:
    WaveletArray();
    
    void appendValue(int value);
    void getArray(int data[], int scale=1);
    int getValue(int index);
    int getLength();
    void newWindow();
    void reset();
    
  private:
    int circArray[WINDOWLENGTH];
    int index;
    int first;
    int length;
    int lastValue;
};

#endif
