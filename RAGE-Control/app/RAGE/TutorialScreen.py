import pygame, Sprite, numpy, random, os

black = (0,0,0)
red = (255,0,0)
white = (255,255,255)
_mainDir = os.environ['RESOURCEPATH']#os.path.split(os.path.abspath(__file__))[0]

class TutorialScreen:

	def __init__(self, screen):
		all = pygame.sprite.RenderUpdates()
		self._screen = screen
		self._Instructions = ['Move left and right by using the arrow keys',
							  "Avoid meteors as they fall. If you get hit, you'll lose control!",
							  'Use the up arrow or space bar to shoot the meteors and gain points',
							  'Keep your friends safe from the meteors',
							  'You lose points whenever one of your friends explodes',
							  'Bigger meteors have to be shot by two players at the same time']
		self._defaultFont = os.path.join(_mainDir, 'fonts', 'freesansbold.ttf')#os.path.join(_mainDir, 'fonts', 'freesansbold.ttf')
		self._InstructionFont = pygame.font.Font(self._defaultFont, 30)
		self._ButtonFont = pygame.font.Font(self._defaultFont, 36)
		# self._InstructionPos = [(150,100),(50,100),(0,100),(175,100),(100,100),(0,100)]
		self._InstructionRect = pygame.Rect(100,100,700,300)
		self._ButtonPos = (400,175)
		self._UnselectedColor = black
		self._SelectedColor = red
		self._InstructionText = self._InstructionFont.render(self._Instructions[0],True,self._UnselectedColor)
		self._ButtonText = self._ButtonFont.render('Next -->',True,self._UnselectedColor)
		self.hoverButton = False
		self.step = 0
		self.numSteps = 6
		
	def draw(self):
		#print self._screen.get_size()
		if (self.step < self.numSteps):
			self._InstructionText = render_textrect(self._Instructions[self.step],self._InstructionFont,self._InstructionRect,self._UnselectedColor,white,1)
			# self._InstructionText = self._InstructionFont.render(self._Instructions[self.step],True,self._UnselectedColor)
			r = self._InstructionText.get_rect()
			self._InstructionPos = (450-(r.width/2),100)
			self._screen.blit(self._InstructionText, self._InstructionPos)
		self._screen.blit(self._ButtonText, self._ButtonPos)
	
	def ButtonHover(self):
		self._ButtonText = self._ButtonFont.render('Next -->',True,self._SelectedColor)
		if (self.step == self.numSteps-1):
			self._ButtonPos = (325,175)
			self._ButtonText = self._ButtonFont.render('Return to Menu -->',True,self._SelectedColor)
		self.hoverButton = True
	
	def ButtonLeave(self):
		self._ButtonText = self._ButtonFont.render('Next -->',True,self._UnselectedColor)
		if (self.step == self.numSteps-1):
			self._ButtonPos = (325,175)
			self._ButtonText = self._ButtonFont.render('Return to Menu -->',True,self._UnselectedColor)
		self.hoverButton = False
		
	def getInstructionText(self):
		if self._InstructionIndex < len(self._Instructions):
			self._InstructionIndex += 1
		return self._Instructions[self._InstructionIndex - 1]

	# source: http://www.pygame.org/pcr/text_rect/index.php
def render_textrect(string, font, rect, text_color, background_color, justification=0):
    """Returns a surface containing the passed text string, reformatted
    to fit within the given rect, word-wrapping as necessary. The text
    will be anti-aliased.

    Takes the following arguments:

    string - the text you wish to render. \n begins a new line.
    font - a Font object
    rect - a rectstyle giving the size of the surface requested.
    text_color - a three-byte tuple of the rgb value of the
                 text color. ex (0, 0, 0) = BLACK
    background_color - a three-byte tuple of the rgb value of the surface.
    justification - 0 (default) left-justified
                    1 horizontally centered
                    2 right-justified

    Returns the following values:

    Success - a surface object with the text rendered onto it.
    Failure - raises a TextRectException if the text won't fit onto the surface.
    """

    # import pygame
    
    final_lines = []

    requested_lines = string.splitlines()

    # Create a series of lines that will fit on the provided
    # rectangle.

    for requested_line in requested_lines:
        if font.size(requested_line)[0] > rect.width:
            words = requested_line.split(' ')
            # if any of our words are too long to fit, return.
            for word in words:
                if font.size(word)[0] >= rect.width:
                    raise TextRectException, "The word " + word + " is too long to fit in the rect passed."
            # Start a new line
            accumulated_line = ""
            for word in words:
                test_line = accumulated_line + word + " "
                # Build the line while the words fit.    
                if font.size(test_line)[0] < rect.width:
                    accumulated_line = test_line
                else:
                    final_lines.append(accumulated_line)
                    accumulated_line = word + " "
            final_lines.append(accumulated_line)
        else:
            final_lines.append(requested_line)

    # Let's try to write the text out on the surface.

    surface = pygame.Surface(rect.size)
    surface.fill(background_color)

    accumulated_height = 0
    for line in final_lines:
        if accumulated_height + font.size(line)[1] >= rect.height:
            raise TextRectException, "Once word-wrapped, the text string was too tall to fit in the rect."
        if line != "":
            tempsurface = font.render(line, 1, text_color)
            if justification == 0:
                surface.blit(tempsurface, (0, accumulated_height))
            elif justification == 1:
                surface.blit(tempsurface, ((rect.width - tempsurface.get_width()) / 2, accumulated_height))
            elif justification == 2:
                surface.blit(tempsurface, (rect.width - tempsurface.get_width(), accumulated_height))
            else:
                raise TextRectException, "Invalid justification argument: " + str(justification)
        accumulated_height += font.size(line)[1]

    return surface

#----------------------------------------------------------------------------------------
