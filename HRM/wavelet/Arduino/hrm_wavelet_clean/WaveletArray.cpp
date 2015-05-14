// Implement a circular array with functionality specifically designed for the
// wavelet transform-based heart rate monitor

#include "WaveletArray.h"

WaveletArray::WaveletArray() {
  index = 0;
  first = 0;
  length = 0;
}

void WaveletArray::appendValue(int value) {
  if(index > 0) {
    lastValue = circArray[index-1];
  }
  if(index > 0 && (abs(lastValue - value) > NOISE_FILTER)) {
    if(value > lastValue) {
      circArray[index] = circArray[index-1] + (NOISE_FILTER - 5);
    } else {
      circArray[index] = circArray[index-1] - (NOISE_FILTER - 5);
    }
  } else {
    circArray[index] = value;
  }
  index %= WINDOWLENGTH;
  circArray[index] = value;
  index++;
  length++;
}

int WaveletArray::getValue(int index) {
  return circArray[(first+index)%WINDOWLENGTH];
}

void WaveletArray::getArray(int data[], int scale) {
  for(int i=0; i<WINDOWLENGTH; i++) {
    data[i] = circArray[(first+i)%WINDOWLENGTH]*scale;
  }
}

int WaveletArray::getLength() {
  return length;
}

void WaveletArray::newWindow() {
  first += WINDOWDIFF;
  first %= WINDOWLENGTH;
  length -= WINDOWDIFF;
}

void WaveletArray::reset() {
  first = 0;
  index = 0;
}
