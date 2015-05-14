#ifndef ShiftBrite_h
#define ShiftBrite_h

#include "Arduino.h" //It is very important to remember this!

//------------------------------------//
// MAX NUMBER OF SHIFT REGISTERS IS 4 //
//------------------------------------//

struct Color
{
  String name;
  int r;
  int g;
  int b; 
};

// Used to set the number of predefined colors
#define numColors 6

class ShiftBrite {
public:
        ShiftBrite(); //Default Constructor. Defaults to 4 shiftbrites
        ShiftBrite(int num); //Overloaded Constructor. num is number of shiftbrites
        ~ShiftBrite(); //Destructor. Currently does nothing
        void WriteLEDArray();
        void setRgbVal(int num, char channel, int val); //Set value for an rgb channel for a single shiftbrite
        void setColor(int num, Color); //Takes in RGB array and sets the output for a single shiftbrite
        void setColor(int num, String color); //sets the color to the name provided. names defined in initArrays, stored in names[]
        void setColor_rand(int num); //sets the output for a single shiftbrite to a free color
        Color getColor(); //returns an RGB array for a free color
        void getColors(int colors[][3]); //fills colors with RGB arrays for all free colors. 
        //colors[0][0] is the number of colors available. Array elements of -1 indicate some colors are taken
        //String colorName(int* rgb); //returns the name of the color specified in rgb
        void turnOff(int);    //set the shiftbrite to off
        
private:
        void SB_SendPacket();
        Color randomColor();
        void setDefaults(); // Sets default number of shiftbrites
        void initArrays(); // Initializes LEDChannels[][]
        Color _getColor(int index); // fills rgb with values for a color from index (0 <= index < numColors)
        Color _getColor(String color); // fills rgb with values for color
        void defineColors(); // Defines RGB arrays for predefined colors
        int _NumLEDs; // number of shiftbrites wired in series
        int LEDChannels[4][3]; // LEDChannels[i][j] sets the color 
        //// output for monitor i with RGB values at j=0,1,2
        
        int SB_CommandMode; //toggle
        int SB_RedCommand;
        int SB_GreenCommand;
        int SB_BlueCommand;
        boolean colors_in_use[numColors]; // true if color is being used
        int _colorIndex(Color rgb); // return index for provided color if equal to predefined
        boolean _equal(int* rgb, int* rgb2); // true if colors are the same
        void set(int* rgb, int* desired); // sets rgb to the desired
        
        Color empty;
		Color colors[numColors];	// used to find colors by name
        // Allocate space for predefined colors
        Color red;
        Color blue;
        Color green;
        Color purple;
        Color yellow;
        Color teal;
		// Add your own colors here
		
};

#endif
