This is an Arduino Library for use with the ShiftBrite, an rgb led shift register.

To begin use, place this folder in the libraries folder under your arduino program files.
	For Mac OS X
		- Navigate to Applications > Arduino > libraries
	For Windows
		- Navitage to C://Program Files/Arduino/libraries

Example use:

	// define your Shiftbrite variable
	ShiftBrite shiftbrite(2);		// this means there are 2 shiftbrites
	shiftbrite.setColor(0, "red");		// set the first shiftbrite to the predefined red color
	shiftbrite.setColor(1, "blue");		// set the second shiftbrite to the predefined blue color
	Color my_color;				// declare your own color
	Color.r = red_pixel_val;
	Color.g = green_pixel_val;
	Color.b = blue_pixel_val;
	shiftbrite.setColor(0, my_color);	// set the first shiftbrite to your own color
	shiftbrite.turnOff(1);			// turn off the second shiftbrite


If you want to have your own colors predefined, first open ShiftBrite.h

Navigate down to the private variables and look for the where a number of "Color" 
variables are defined. Define your own Color variables with appropriate names.
For example, if you wanted to add a color called lime_green, you would add the line
	
	Color lime_green;


Next find the line that says
	#define numColors
and increment the value there to reflect the number of colors you have added.

Now open up ShiftBrite.cpp and find the function void ShiftBrite::defineColors(). Add your own color in the space provided
If we were adding the lime_green color defined above we would add the lines
	
	lime_green.r = 50;		// set the red pixel value
	lime_green.g = 205;		// set the green pixel value
	lime_green.b = 50;		// set the blue pixel value
	lime_green.name = "lime_green";	// set the name of the color
	colors[i] = lime_green;		// i should be the number (0 indexed) of the color being defined. 
					//  there are 6 colors already defined, so your first color should
					//  be placed at colors[6]

That's it! Now if you want a shiftBrite to set your new color, simply call the setColor function as we did in the
example usage, also shown below.

	shiftbrite.setColor(0, "lime_green");
