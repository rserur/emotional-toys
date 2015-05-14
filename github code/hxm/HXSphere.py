from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import sys
import numpy as np
from HXMReceiver import *

ESCAPE = '\033'

window = 0
depthFactor = 0
HRVmax = 120000
HRVmin = 10000
HRmax = 110
HRmin = 60

def InitGL(Width, Height):				# We call this right after our OpenGL window is created.
	global quadratic
	
	quadratic = gluNewQuadric()
	gluQuadricNormals(quadratic, GLU_SMOOTH)		# Create Smooth Normals (NEW)
	
	glClearColor(0.0, 0.0, 0.0, 0.0)	# This Will Clear The Background Color To Black
	glClearDepth(1.0)					# Enables Clearing Of The Depth Buffer
	glDepthFunc(GL_LESS)				# The Type Of Depth Test To Do
	glEnable(GL_DEPTH_TEST)				# Enables Depth Testing
	glShadeModel(GL_SMOOTH)				# Enables Smooth Color Shading
	
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()					# Reset The Projection Matrix
										# Calculate The Aspect Ratio Of The Window
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)

	glMatrixMode(GL_MODELVIEW)
	
	glLightfv(GL_LIGHT0, GL_AMBIENT, (1.0, 0.0, 0.0, 0.5))	# Setup The Ambient Light 
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 0.0, 0.0, 0.5))	# Setup The Diffuse Light 
	#glLightfv(GL_LIGHT0, GL_SPECULAR, (1.0, 0.0, 0.0, 1.0))	# Setup The Diffuse Light 
	glLightfv(GL_LIGHT0, GL_POSITION, (1.0, 1.0, 1.0, 0.0))	# Position The Light 
	glEnable(GL_LIGHT0)										# Enable Light One
	
	glLightfv(GL_LIGHT1, GL_AMBIENT, (0.0, 0.0, 1.0, 0.5))	# Setup The Ambient Light 
	glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.0, 0.0, 1.0, 0.5))	# Setup The Diffuse Light 
	#glLightfv(GL_LIGHT1, GL_SPECULAR, (0.0, 0.0, 1.0, 1.0))	# Setup The Diffuse Light 
	glLightfv(GL_LIGHT1, GL_POSITION, (1.0, 1.0, 1.0, 0.0))	# Position The Light 
	glEnable(GL_LIGHT1)										# Enable Light One  
	
def moveLight():
	global depthFactor
	glLoadIdentity()
	depthFactor += 0.001
	glMatrixMode(GL_MODELVIEW)
	glLightfv(GL_LIGHT0, GL_POSITION, (5*np.sin(depthFactor*np.pi), 0.0, 5*np.cos(depthFactor*np.pi), 0))	# Position The Light
	glLightfv(GL_LIGHT1, GL_POSITION, (0.0, 5*np.sin(depthFactor*np.pi), 5*np.cos(depthFactor*np.pi), 0))	# Position The Light
	#glLightfv(GL_LIGHT0, GL_POSITION, (0.0, 0.0, 2.0, 0.0))	# Position The Light
	glLoadIdentity()
	
def respondToHRChanges():
	global h
	localHR = h.HR
	localHRV = h.HRV
	if (localHR > HRmax):
		localHR = HRmax
	if (localHR < HRmin):
		localHR = HRmin
	if (localHRV > HRVmax):
		localHRV = HRVmax
	if (localHRV < HRVmin):
		localHRV = HRVmin
	fRed = float(localHR-HRmin) / float(HRmax-HRmin)
	fBlue = 1.0 - (float(localHRV-HRVmin)/float(HRVmax-HRVmin))
	glLightfv(GL_LIGHT0, GL_AMBIENT, (fRed, 0.0, 0.0, 0.5))	# Setup The Ambient Light 
	glLightfv(GL_LIGHT0, GL_DIFFUSE, (fRed, 0.0, 0.0, 0.5))	# Setup The Diffuse Light 
	glLightfv(GL_LIGHT1, GL_AMBIENT, (0.0, 0.0, fBlue, 0.5))	# Setup The Ambient Light 
	glLightfv(GL_LIGHT1, GL_DIFFUSE, (0.0, 0.0, fBlue, 0.5))	# Setup The Diffuse Light 
	

def ReSizeGLScene(Width, Height):
	if Height == 0:						# Prevent A Divide By Zero If The Window Is Too Small 
		Height = 1

	glViewport(0, 0, Width, Height)		# Reset The Current Viewport And Perspective Transformation
	glMatrixMode(GL_PROJECTION)
	glLoadIdentity()
	gluPerspective(45.0, float(Width)/float(Height), 0.1, 100.0)
	glMatrixMode(GL_MODELVIEW)
	
def DrawGLScene():

	global quadratic
	global depthFactor
	
	moveLight()
	respondToHRChanges()
	glEnable(GL_LIGHTING)
	# Clear The Screen And The Depth Buffer
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
	glLoadIdentity()					# Reset The View
	glTranslatef(0.0,0.0,-15.0)
	gluSphere(quadratic,2.0,128,128)
	# glBindTexture(GL_TEXTURE_2D, int(textures[texture_num]))
	# glDisable(GL_LIGHTING) 
	
	# gluSphere(quadradic,1.3,32,32);

	#  since this is double buffered, swap the buffers to display what just got drawn. 
	glutSwapBuffers()
	
def keyPressed(*args):
	global window
	# If escape is pressed, kill everything.
	if args[0] == ESCAPE:
		sys.exit()
		
def main():
	global window
	global h
	h = HXMReceiver()
	h.run()
	# pass arguments to init
	glutInit(sys.argv)

	# Select type of Display mode:   
	#  Double buffer 
	#  RGBA color
	# Alpha components supported 
	# Depth buffer
	glutInitDisplayMode(GLUT_RGBA | GLUT_DOUBLE | GLUT_DEPTH)
	
	# get a 640 x 480 window 
	glutInitWindowSize(800, 600)
	
	# the window starts at the upper left corner of the screen 
	glutInitWindowPosition(0, 0)
	
	# Okay, like the C version we retain the window id to use when closing, but for those of you new
	# to Python (like myself), remember this assignment would make the variable local and not global
	# if it weren't for the global declaration at the start of main.
	window = glutCreateWindow("RAGE Control")

   	# Register the drawing function with glut, BUT in Python land, at least using PyOpenGL, we need to
	# set the function pointer and invoke a function to actually register the callback, otherwise it
	# would be very much like the C version of the code.	
	glutDisplayFunc(DrawGLScene)
	
	# Uncomment this line to get full screen.
	#glutFullScreen()

	# When we are doing nothing, redraw the scene.
	glutIdleFunc(DrawGLScene)
	
	# Register the function called when our window is resized.
	glutReshapeFunc(ReSizeGLScene)
	
	# Register the function called when the keyboard is pressed.  
	glutKeyboardFunc(keyPressed)

	# Initialize our window. 
	InitGL(640, 480)

	# Start Event Processing Engine	
	glutMainLoop()
	
print "Hit ESC key to quit."
main()