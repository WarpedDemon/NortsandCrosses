import math, pygame
from tkinter import *
from tkinter import messagebox

pygame.init() #Initialize Pygame Module
smallText = pygame.font.Font('freesansbold.ttf',32)

class GameButton:
	def __init__(self, dimensions, color, highlight_color, textValue, clickAble, hoverAble, x, y):
		self.x = dimensions[0]
		self.y = dimensions[1]
		self.gridx = x
		self.gridy = y
		self.width = dimensions[2]
		self.height = dimensions[3]
		self.color = color
		self.highlight_color = highlight_color
		self.dimensions = dimensions
		self.clickAble = clickAble
		self.hoverAble = hoverAble
		self.nought = False
		self.cross = False
		self.scoreValue = 0
		self.CreateText(textValue)

	def IsHovered(self, mouse):
		if(self.x < mouse[0] and mouse[0] <  self.x + self.width):
			if(self.y + self.height > mouse[1] and mouse[1] > self.y):
				return True
		return False

	def CreateText(self, textValue):
		self.text = smallText.render(textValue, True, (0, 0, 0))
		self.textRect = self.text.get_rect()
		self.textValue = textValue
		self.textRect.center = (self.x + self.width / 2, self.y + self.height / 2)

	def ClickEvent(self, GC):
		if self.CanClick() == True:
			if self.NotOwned():
				self.SetOwner(GC.GetCurrentPlayer())
				GC.DetectWinner(self.gridx, self.gridy, GC.GetCurrentPlayer())

	def CanClick(self):
		return self.clickAble

	def CanHover(self):
		return self.hoverAble

	def NotOwned(self):
		if not self.nought and not self.cross: return True
		return False

	def SetOwner(self, owner):
		if(owner == "X"): self.nought = True
		if(owner == "O"): self.cross = True
		if(owner == ""):
			self.cross = False
			self.nought = False
		self.CreateText(owner)
		return

	def Render(self, g, window, mouse):
		if(self.IsHovered(mouse) and self.CanHover()):
			g.draw.rect(window, self.highlight_color, self.dimensions)
		else:
			g.draw.rect(window, self.color, self.dimensions)
		window.blit(self.text, self.textRect)
		return

class Box:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.width = 50
		self.height = 50
		self.nought = False
		self.cross = False

class GameController:
	'''Custom Main class to control python game'''

	def __init__(self, context):
		'''Initialize Game Controller Class Object'''
		#Variables
		self.GAMEOBJECTS = []

		self.windowDimensions = (625, 320)
		self.windowTitle = "Tic Tac Toe - Version 1.0"

		self.programRunning = False
		self.gameRunSpeed = math.floor(1000/60) #Sets game to 60 frames per second

		#Test Box Dimensions + Locations
		self.BoxList = []

		self.CurrentPlayer = "X"

		#Holds the main pygame object to be used in game.
		self.ctx = context
		self.window = self.ctx.display.set_mode(self.windowDimensions)
		self.QUIT_EVENT = self.ctx.QUIT

		#Sets window title
		self.ctx.display.set_caption(self.windowTitle)
		return

	def Initialize(self):
		'''Commence Game Loop'''
		self.programRunning = True
		self.CreateBoxes()
		self.player1 = GameButton((330, 70, 280, 40), (0, 255, 0), (255, 0, 0), "Player1, Score: 0", False, False, 0, 0)
		self.player2 = GameButton((330, 115, 280, 40), (255, 0, 0), (0, 255, 0), "Player2, Score: 0", False, False, 0, 0)
		self.GAMEOBJECTS.append(self.player1)
		self.GAMEOBJECTS.append(self.player2)
		self.GameLoop()

	def CreateBoxes(self):
		for y in range(0, 3):
			for x in range(0, 3):
				# Create Box
				newBox = GameButton((x * 110, y * 110, 100, 100), (170, 170, 170), (255,255,255), "", True, True, x, y)
				this = newBox
				self.GAMEOBJECTS.append(newBox)
				self.BoxList.append(newBox)
		return

	def GameLoop(self):
		'''Runs each frame to control game.'''

		self.RotationTick = 0 #Ignore this, controls the orbit animation.

		while self.programRunning:
			self.ctx.time.delay(self.gameRunSpeed) #Delays game to 30 frames per second.
			self.RotationTick += 0.1

			mousePos = self.ctx.mouse.get_pos()
			self.RegisterEvents(mousePos) #Get inputs and window events.

			self.Update()
			self.Render(mousePos)

	#Updates positions and other behind scenes stuff.
	def Update(self):
		pass

	def Render(self, mousePos):
		self.window.fill((0,0,0)) #Resets window to black.

		for box in self.BoxList:
			box.Render(self.ctx, self.window, mousePos)

		#print(self.ctx.mouse.get_pos())
		self.player1.Render(self.ctx, self.window, mousePos)
		self.player2.Render(self.ctx, self.window, mousePos)

		self.ctx.display.update() #Update the render to reflect changes.
		return

	#Gets all Pygame related events.
	def GetEvents(self):
		return self.ctx.event.get()

	def GetCurrentPlayer(self):
		return self.CurrentPlayer

	def RegisterMouseClick(self, mousePos):
		for obj in self.GAMEOBJECTS:
			if obj.IsHovered(mousePos):
				obj.ClickEvent(self)

	def SwitchPlayers(self):
		if self.CurrentPlayer == "X":
			self.CurrentPlayer = "O"
			self.player2.color = (0, 255, 0)
			self.player1.color = (255, 0, 0)
		else:
			self.CurrentPlayer = "X"
			self.player2.color = (255, 0, 0)
			self.player1.color = (0, 255, 0)
		return

	def DetectWinner(self, x, y, mark):
		#print(str(x), str(y), mark)
		checkList = []
		count = 0
		addition = []
		for box in self.BoxList:
			addition.append(box.textValue)
			count += 1
			if count > 2:
				count = 0
				checkList.append(addition)
				addition = []

		#print(str(checkList))
		win = False
		#print("X: " + str(x) + " Y: " + str(y))
		if checkList[0][x] == (mark) and checkList[1][x] == (mark) and checkList[2][x] == (mark): win = True
		if checkList[y][0] == (mark) and checkList[y][1] == (mark) and checkList[y][2] == (mark): win = True

		if checkList[0][0] == (mark) and checkList[1][1] == (mark) and checkList[2][2] == (mark): win = True
		if checkList[2][0] == (mark) and checkList[1][1] == (mark) and checkList[0][2] == (mark): win = True

		if(win):
			if mark == "X":
				self.player1.scoreValue += 1
				self.player1.CreateText("Player1, Score: " + str(self.player1.scoreValue))
			if mark == "O":
				self.player2.scoreValue += 1
				self.player2.CreateText("Player2, Score: " + str(self.player2.scoreValue))

			Tk().wm_withdraw()  # to hide the main window
			MsgBox = messagebox.askyesnocancel("Winner!", 'Winner Found: ' + mark + ' is the winner! Would you like to play again and save your score?', icon='question')
			if MsgBox:
				#print("Yes!!!")
				self.RestartGame()
			elif MsgBox == None:
				self.programRunning = False
			else:
				self.player1.scoreValue = 0
				self.player1.CreateText("Player1, Score: 0")
				self.player2.scoreValue = 0
				self.player2.CreateText("Player2, Score: 0")
				self.RestartGame()
		else:
			empty = False
			for y in checkList:
				for value in y:
					if value == "" or value == None:
						empty = True

			if empty == True:
				self.SwitchPlayers()
			else:
				Tk().wm_withdraw()  # to hide the main window
				MsgBox = messagebox.askyesnocancel("Draw!",
												   'Draw Found: No winner would you like to play again and save your score?', icon='question')
				if MsgBox:
					# print("Yes!!!")
					self.RestartGame()
				elif MsgBox == None:
					self.programRunning = False
				else:
					self.player1.scoreValue = 0
					self.player1.CreateText("Player1, Score: 0")
					self.player2.scoreValue = 0
					self.player2.CreateText("Player2, Score: 0")
					self.RestartGame()

	def RestartGame(self):
		for box in self.BoxList:
			box.SetOwner("")
		if(self.CurrentPlayer == "O"): self.SwitchPlayers()

	def RegisterEvents(self, mousePos):
		for event in self.GetEvents():
			if event.type == self.QUIT_EVENT:
				self.programRunning = False
			if event.type == self.ctx.MOUSEBUTTONUP:
				self.RegisterMouseClick(mousePos)
		return
		
#Instantiate instance of our custom game controller
GC = GameController(pygame)
GC.Initialize() #Start Game