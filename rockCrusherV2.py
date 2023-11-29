## Imports
import time
import math as m
import random
from graphics import *
from graphicAnimator import *
from graphicsExtended import *
from graphicObjectsGrouper import *

# Sets up the window values
winSize = 800
textSize = math.floor((12 / 450) * winSize)
if (textSize < 5):
	textSize = 5
elif (textSize > 36):
	textSize = 36

coordMax = 100
boundsStart = 5
boundsEnd = coordMax - boundsStart

# Sets up the color pallet
BorderColor = "#000000"
InsideColor = "#2D0A0D"
HighlightColor = "#FFCECB"
RockColorOne = "#C2253C"
RockColorTwo = "#71131F"
RockColorThree = "#2D0A0D"

# Sets up logo OBJ
# Creates a new logo
logo = []
# Base
logoBase = [30, 31]
# Crystal
crystalBits = [32, 33, 34]
# Top
logoTopLetters = [35, 36, 37, 38, 39, 40, 41, 42]
# Bottom
logoBottomLetters = [43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57]
# Add all parts together
logo.extend(logoBase + crystalBits + logoTopLetters + logoBottomLetters)


# Sets up rock OBJ
# Creates a new rock
polyRock = []
# Base and base shadow
rockBaseAndShadow = [0, 1, 2]
# Rocks
rockBits = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]
# Shadows
rockBitsShadows = [16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
# Add all parts together
polyRock.extend(rockBaseAndShadow + rockBits + rockBitsShadows)

# Sets up crystal OBJ
# Creates a new crystal
crystal = []
# Base
crystalBase = [58]
# Base and highlight
crstalHilight = [59, 60, 61, 62, 63, 64]
# Shadows
crystalShadows = [65, 66, 67]
# Rock
crystalRock = [68, 69]
# Add all parts together
crystal.extend(crystalBase + crstalHilight + crystalShadows + crystalRock)

# Sets up spikeball OBJ
# Creates a new spikeball
spikeball = []
# Base
spikeballBase = [71, 72, 73]
# Base and highlight
spikeballSpikes = [74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92]
# Shadows
spikeballHighlights = [93, 94, 95, 96, 97, 98, 99, 100, 101, 102, 103, 104, 105, 106, 107, 108, 109, 110, 111, 112, 113]
# Add all parts together
spikeball.extend(spikeballBase + spikeballSpikes + spikeballHighlights)

# Sets the amount the rock will change when hit
rockShrink = (2/3)
rockRotMin = 0
rockRotMax = 360

# Sets the change values for the colors
secndReq = 1
thrdReq = 2
frthReq = 3

# Creates a list of the crystals
crystals = []

# Sets if certain debug values are on
collideRockRotDebugOn = False

# Creates the window
def createWindow():
	# Sets the window values
	name = "Rock Crusher"

	# Draws the window
	win = drawWindowE(name, winSize, winSize, coordMax, coordMax, BorderColor)
	drawRectE(win, Point(5, 5), Point(coordMax - boundsStart, coordMax - boundsStart), InsideColor, InsideColor)

	return win

# Display instrucions
def instructions(win: GraphWin):
	# Sets the instructions for the game
	words = """The object of the game is to break the rocks.
Rocks change colors the more they are hit by the ball.
Each rock can be hit three times before breaking.
How many can you destroy?
Click to draw rocks but not in the bright red area.
Good luck!"""

	# Sets random colors for the logo crystal
	crystalHue = random.randint(0, 360)
	crystalColor1 = hslToHex(crystalHue, 100, 94)
	crystalColor2 = hslToHex(crystalHue, 29, 54)

	# Draws the game logo
	gameLogo = setupInitialObjectGroup(win, logo, 0.5, 0, Point(50, 73))

	# Colors the crystal
	for g in range(len(gameLogo.poly)):
			# Sets base and shadows
			if g + 30 == 32 or g + 30 == 34:
				gameLogo.setColor(g, crystalColor2)
			# Sets highlights
			elif g + 30 == 33:
				gameLogo.setColor(g, crystalColor1)

	# Draws the instructions
	instruct = drawTextE(win, Point(50, 40), words, textSize, HighlightColor)
	
	# Creates a button used to play the game
	playButton = Button(Point(50, 20), 25, 8, "Play", textSize, InsideColor, HighlightColor, BorderColor, 5)
	playButton.draw(win)
	
	# Waits for the button to be pressed
	while not playButton.checkButton(win.getMouse()):
		pass

	# Undraws all of the instructions screen
	gameLogo.undraw()
	instruct.undraw()
	playButton.undraw()

# Spawns in the ball
def spawnBall(win: GraphWin):
	# Instatiaes ball values
	radius = random.uniform(2.5, 4)
	fill = HighlightColor
	outline = HighlightColor

	# Picks a random location
	a = random.uniform(radius + boundsStart, boundsEnd - radius)
	b = random.uniform(radius + boundsStart, boundsEnd - radius)
	spawnPoint = Point(a, b)

	# Draws the ball
	ball = cirE(spawnPoint, radius, fill, outline)

	# Creates the group obj
	polyBall = setupInitialObjectGroup(win, spikeball, (radius * .13) / 4, random.uniform(0, 360), ball.getCenter())
	
	return ball, polyBall

# Adds an line on the end of a ball showing the balls directory
def ballGuideline(win: GraphWin, ball: Circle, length: float, rotAngle, color = HighlightColor, width = 1):
	# Finds the two points of the line
	center = ball.getCenter()
	radius = ball.getRadius()
	point1 = movePoint(center, rotAngle, radius)
	point2 = movePoint(center, rotAngle, radius + length)

	# Sets a radius for where you cant place the rocks
	barrierRad = distance(center, point2)

	# Draws the line
	guideline = drawLineE(win, point1, point2, color)
	guideline.setWidth(width)

	return guideline, barrierRad

# Create the rocks
def generateRocks(win: GraphWin, amnt: int, color, ball, polyBall, curDirection):
	# Sets the rock variables
	radius = 5
	fill = color
	rockList = []
	polyRockList = []

	# Adds a guideline to get idea of balls direction
	guideline, barrierRad = ballGuideline(win, ball, 10, curDirection, HighlightColor, 5)

	# Creates a visible barrier where a rock cant be placed
	wallBarrier = drawRectE(win, Point(0, 0), Point(coordMax, coordMax), RockColorTwo, RockColorTwo)
	insideTemp = drawRectE(win, Point(boundsStart + radius, boundsStart + radius), Point(coordMax - boundsStart - radius, coordMax - boundsStart - radius), InsideColor, InsideColor)
	barrier = drawCirE(win, ball.getCenter(), barrierRad + radius, RockColorTwo, RockColorTwo)
	polyBall.undraw()
	guideline.undraw()
	polyBall.draw(win)
	guideline.draw(win)

	# Draws the instruction text
	newAmnt = int(amnt)
	instruct = drawTextE(win, Point(50, 10), f"Place {newAmnt} more rock(s)", textSize, HighlightColor)

	# Draws the rocks
	i = 0
	while i < amnt:
		# Finds where the mouse is clicked
		clickPoint = win.getMouse()
		clickX = clickPoint.getX()
		clickY = clickPoint.getY()

		# Gets the distance between the rock and the ball
		rockDistFromBall = distance(clickPoint, ball.getCenter()) - radius

		# Makes sure the rock is inside the bounds of the play area
		if (boundsStart + radius < clickX < coordMax - boundsStart - radius and boundsStart + radius < clickY < coordMax - boundsStart - radius):
			# Makes sure the rock is far enough away from the ball
			if (rockDistFromBall > barrierRad):
				# Updates the instruct text when clicked
				i += 1
				newAmnt -= 1
				instruct.setText(f"Place {newAmnt} more rock(s)")

				# Creates a new rock collider
				newRock = cirE(clickPoint, radius, fill, fill)
				rockList.append(newRock)

				# Creates the group obj
				rock = setupInitialObjectGroup(win, polyRock, (radius * .13) / 4, random.uniform(0, 360), newRock.getCenter())
				polyRockList.append(rock)

				# Makes the instrucitons above any rocks
				instruct.undraw()
				instruct.draw(win)
		

	# Removes the instructions
	instruct.undraw()
	barrier.undraw()
	guideline.undraw()
	wallBarrier.undraw()
	insideTemp.undraw()

	# Returns the rocks
	return rockList, polyRockList

# Creates a crystal at a point
def generateCrystal(win: GraphWin, center: Point, polyBall: ObjGroup):
	# Randomizes the crystals scale rotation and colors
	crystalScale = random.uniform(0.09, 0.03)
	crystalRot = random.uniform(-20, 20)
	crystalHue = random.randint(0, 360)
	crystalColor1 = hslToHex(crystalHue, 100, 94)
	crystalColor2 = hslToHex(crystalHue, 29, 54)

	# Creates the crystal
	newCrystal = setupInitialObjectGroup(win, crystal, crystalScale, crystalRot, center)
	
	# Colors the crystal
	for g in range(len(newCrystal.poly)):
			# Sets base and shadows
			if crystalBase.__contains__(g + 58) or crystalShadows.__contains__(g + 58):
				newCrystal.setColor(g, crystalColor2)
			# Sets highlights
			elif crstalHilight.__contains__(g + 58):
				newCrystal.setColor(g, crystalColor1)

	# Adds the crystal to a list
	crystals.append(newCrystal)

	# Redraws the ball above the crystal
	polyBall.undraw()
	polyBall.draw(win)

# Helps to find the distance between two points
def distance(point1: Point, point2: Point):
	# Uses the euclidian distance formula to find the distance
	dist = m.sqrt((point1.x - point2.x) ** 2 + (point1.y - point2.y) ** 2)
	return dist

# Moves the ball around the screen
def moveBall(ball: Circle, curDirection, moveLength, polyBall: ObjGroup, win):
	# Finds the x and y distance to move the ball
	dX, dY, quadrant = moveDist(curDirection, moveLength)

	# Moves the ball at the given speed and angle
	ball.move(dX, dY)
	polyBall.moveToPoint(win, ball.getCenter())

	return quadrant

# Moves a point from start point a certain angle
def movePoint(point: Point, curDirection, moveLength):
	# Finds the x and y distance to move the ball
	dX, dY, quadrant = moveDist(curDirection, moveLength)

	# Creates the point where it was moved
	movePoint = Point(point.getX() + dX, point.getY() + dY)

	return movePoint

# Finds the x and y distance to move something from a degree
def moveDist(curDirection, moveLength):
	# Gets the quadrant of the movement
	quadrant = 1
	moveDir = float(curDirection[0])

	while (moveDir > 90 or moveDir < 0):

		# If moveDir is too much
		if (moveDir > 90):
			moveDir -= 90

			if(quadrant == 1):
				quadrant = 4

			else:
				quadrant -= 1
		# If moveDir is too little
		elif (moveDir < 0):
			moveDir += 90

			if(quadrant == 4):
				quadrant = 1

			else:
				quadrant += 1


	# Sets the proportions for the movement
	moveRadian = moveDir * (m.pi / 180)

	firstMov = moveLength * m.sin(moveRadian) # Opposite
	secondMov = moveLength * m.cos(moveRadian) # Adjacent

	"""Sets the delta(X) and delta(Y)"""
	# Flips the x and y if the quadrant is even
	if (quadrant % 2 == 0):
		dX = secondMov
		dY = firstMov

		# Second quadrant has x negative
		if (quadrant == 2):
			dX *= -1 

		# Fourth quadrant has y negative
		else:
			dY *= -1 
	
	# Keeps them the same if odd
	else:
		dX = firstMov
		dY = secondMov

		# Third quadrant has x and y negative
		if (quadrant == 3):
			dX *= -1 
			dY *= -1

		# First doesn't change

	return dX, dY, quadrant

# Checks the amount of time between calls
def checkTime(startTime, curTime, timeGoal, printTime = False):
	# Gets the amount of time from the start of when the ball moved to now
	timeDif = curTime- startTime

	if(printTime):
		print(timeDif)

	return not (timeGoal < timeDif)

# Gets a new rotation for the ball when a wall is hit
def collideWallRot(curDirection: list, quadDelta, xOrY):
	# Finds the angle within 90 degrees
	
	angle = float(curDirection[0])
	while (angle > 90):
		angle -= 90

	while (angle < 0):
		angle += 90

	# Checks the x or y of the ball
	if (xOrY == "y"):
		# Checks the quadrant of the movement
		if (quadDelta == 1 or quadDelta == 3):
			# Takes the distance from 90
			dist = 90 - angle
			addAngle = dist * 2

		elif (quadDelta == 2 or quadDelta == 4):
			addAngle = angle * -2

	elif (xOrY == "x"):
		# Checks the quadrant of the movement
		if (quadDelta == 2 or quadDelta == 4):
			# Takes the distance from 90
			dist = 90 - angle
			addAngle = (dist * 2) + 360

		elif (quadDelta == 1 or quadDelta == 3):
			addAngle = (angle * -2) + 360

	return addAngle

# Checks if the ball hits a wall
def checkWallCollision(ball: Circle, curDirection: list, quadDelta, polyBall, win):
	# Gets the center and radius of the ball
	center = ball.getCenter()
	radius = ball.getRadius()
	wallsHit = 0

	# Checks if the ball hit a horisontal wall
	if (hitHorisontal(ball)):
		# Adds to wall hit counter
		wallsHit += 1

		# Randomizes the ball color
		randoColor = randoRGB()
		ball.setFill(randoColor)
		ball.setOutline(randoColor)

		# Rotates the ball
		curDirection[0] += collideWallRot(curDirection, quadDelta, "y")

		# If the ball is on the bottom side of the screen move it up
		if (center.getY() < coordMax / 2):
			bottomPoint = center.getY() - radius
			reAdjustY = (bottomPoint * -1) + boundsStart

		# If the ball is on the top side of the screen move it down
		elif (center.getY() > coordMax / 2):
			topPoint = center.getY() + radius
			reAdjustY = boundsEnd - topPoint

		# Fixes the ball position back in bounds
		ball.move(0, reAdjustY)
		polyBall.moveToPoint(win, ball.getCenter())

	# Checks if the ball hit a vertical wall
	if (hitVertical(ball)):
		# Adds to wall hit counter
		wallsHit += 1

		# Randomizes the ball color
		randoColor = randoRGB()
		ball.setFill(randoColor)
		ball.setOutline(randoColor)

		# Rotates the ball
		curDirection[0] += collideWallRot(curDirection, quadDelta, "x")

		# If the ball is on the left side of the screen move it right
		if (center.getX() < coordMax / 2):
			leftPoint = center.getX() - radius
			reAdjustX = (leftPoint * -1) + boundsStart

		# If the ball is on the right side of the screen move it left
		elif (center.getX() > coordMax / 2):
			rightPoint = center.getX() + radius
			reAdjustX = boundsEnd - rightPoint
		
		# Fixes the ball position back in bounds
		ball.move(reAdjustX, 0)
		polyBall.moveToPoint(win, ball.getCenter())

	# Checks if both walls were hit
	if (wallsHit == 2):
		# Rotates the ball
		curDirection[0] += 180

# Checks for if the ball hits a vertical wall
def hitVertical(ball: Circle):
	# Finds the left point and right point of the ball
	center = ball.getCenter()
	radius = ball.getRadius()

	leftPoint = center.getX() - radius
	rightPoint = center.getX() + radius

	# Checks if ball is in the window bounds
	if (leftPoint < boundsStart):
		return True
	if (rightPoint > boundsEnd):
		return True
	
	# If it's in bounds
	return False
	
# Checks for if the ball hits a horisontal wall
def hitHorisontal(ball: Circle):
	# Finds the bottom point and top point of the ball
	center = ball.getCenter()
	radius = ball.getRadius()

	bottomPoint = center.getY() - radius
	topPoint = center.getY() + radius

	# Checks if ball is in the window bounds
	if (bottomPoint < boundsStart):
		return True
	if (topPoint > boundsEnd):
		return True
	
	# If it's in bounds
	return False

# Finds the new rotation for the ball when a rock is hit
def collideRockRot(win: GraphWin, curDirection: list, quadDelta, ball: Circle, rock: Circle, moveDegree, turnOnDebug = False):
	# Simplifies important variables
	rCenter = rock.getCenter()
	rRad = rock.getRadius()
	bCenter = ball.getCenter()
	
	# Finds the angle perpendicular to the collsion angle
	startMoveDegree = [moveDegree]
	oppAngle = [moveDegree - 90]
	moveDegree = [moveDegree]

	# Makes the angle within the bounds of 360 degrees
	if (oppAngle[0] > 360):
		oppAngle[0] -= 360
	elif (oppAngle[0] < 0):
		oppAngle[0] += 360

	# Gets the opposite angle's distance from 90 and flips the sign
	distFrom90 = (oppAngle[0] - 90) * -1 

	# Finds the angle of the balls movement once flattened
	ballDir = float(curDirection[0]) + distFrom90
	while (ballDir > 360):
		ballDir -= 360
	while (ballDir < 0):
		ballDir += 360

	# Finds if the way to get the direction is positive or negative
	#posDist = m.fabs(ballDir - ) # Distance to the right in degrees
	#negDist = m.fabs(ballDir - ) # Distance to the right in degrees

	# If the balls move degree is more than the degree where the ball was moved off the rock
	#if (ballDir > moveDegree[0]):
		#moveDegree[0] *= -1

	# Sets the flattened quadrant
	ballQuadNorm = 1

	while (ballDir > 90):
		ballDir -= 90
		if (ballQuadNorm == 4):
			ballQuadNorm = 1
		else:
			ballQuadNorm += 1

	while (ballDir < 0):
		ballDir += 90
		if (ballQuadNorm == 1):
			ballQuadNorm = 4
		else:
			ballQuadNorm -= 1


	# Checks the quadrant of the movement
	if (ballQuadNorm == 1 or ballQuadNorm == 3):
		# Takes the distance from 90
		dist = 90 - ballDir
		addAngle = dist * 2

	elif (ballQuadNorm == 2 or ballQuadNorm == 4):
		addAngle = ballDir * -2

	# Adds the displacemnt back to the angle
	addAngle -= distFrom90

	""" 
	*Tries* to get the correct angle 

	[Disclaimer]	I don't really know if these are 100% correct but it looks close enough
	
	"""
	# If the ball is above the rock
	if (bCenter.getY() > rCenter.getY()):
		addAngle += 180
	# If the ball hits the rock around the right middle of the ball or left middle
	if (moveDegree[0] > 45 and moveDegree[0] < 135) or (moveDegree[0] > 225 and moveDegree[0] < 315):
		addAngle -= 90
	# If the ball is above the rock and in the above left bounds or below the rock in the right bounds
	if ((moveDegree[0] > 225 and moveDegree[0] < 315) and (bCenter.getY() > rCenter.getY())) or ((moveDegree[0] > 45 and moveDegree[0] < 135) and (bCenter.getY() < rCenter.getY())):
		addAngle += 180

	# Draws the debugging options
	if (turnOnDebug):
		# Finds the point between the two centers
		midPoint = Point(rCenter.x, rCenter.y)
		midPoint = movePoint(midPoint, startMoveDegree, rRad)

		# Finds one end of the perpendicular slope to a positive amount
		topPoint = midPoint.clone()
		topPoint = movePoint(topPoint, oppAngle, 10)

		# Finds one end of the perpendicular slope to a negative amount
		bottomPoint = midPoint.clone()
		bottomPoint = movePoint(bottomPoint, oppAngle, -10)

		# Finds the direction the ball will go
		trajectoryStart = ball.getCenter()
		trajectory = [curDirection[0] + addAngle]
		trajectoryOpp = [curDirection[0]]
		trajectoryFlip = [curDirection[0] + addAngle + 180]
		trajectoryOppFlip = [curDirection[0] - addAngle + 180]
		trajectoryCur = [360 - curDirection[0]]
		trajectoryCurEnd = movePoint(midPoint.clone(), trajectoryCur, 5)
		trajectoryEnd = movePoint(midPoint.clone(), trajectory, 5)
		trajectoryOppEnd = movePoint(midPoint.clone(), trajectoryOpp, 5)
		trajectoryFlipEnd = movePoint(midPoint.clone(), trajectoryFlip, 5)
		trajectoryFlipOppEnd = movePoint(midPoint.clone(), trajectoryOppFlip, 5)

		# Draws the line from the end points
		drawShapes = []
		drawShapes.append(drawLineE(win, topPoint, bottomPoint, "white"))
		drawShapes.append(drawCirE(win, rCenter, rRad, "green"))
		drawShapes.append(drawCirE(win, midPoint, .5))
		drawShapes.append(drawLineE(win, midPoint, trajectoryEnd, "white"))
		drawShapes.append(drawLineE(win, trajectoryStart, trajectoryOppEnd, "red"))
		#drawShapes.append(drawLineE(win, midPoint, trajectoryFlipEnd, "black"))
		#drawShapes.append(drawLineE(win, midPoint, trajectoryFlipOppEnd, "blue"))
		drawShapes.append(drawLineE(win, midPoint, trajectoryCurEnd, "green"))
		print("\n", quadDelta, moveDegree, trajectory, addAngle)
		#time.sleep(.5)
		win.getMouse()
		for i in range(len(drawShapes)):
			drawShapes[i].undraw()

	return addAngle

# Changes the tradjectory of the ball when a rock is hit
def checkRockCollision(ball: Circle, curDirection: list, rocks: list, hitList: list, color1, color2, color3, polyRockList: list, win, polyBall):
	# Sets ball variables
	center = ball.getCenter()
	radius = ball.getRadius()
	
	# Checks if the ball collided with a rock
	if (didCollide(rocks, hitList, ball, polyRockList, win, polyBall)):
		# Finds the rocks(s) it collided with 
		# Runs through every rock checking to see if the rock was hit
		for i in range(len(rocks)):
			# Checks to see if the ball is hitting a rock
			curDist = distance(center, rocks[i].getCenter())
			if (curDist <= (radius + rocks[i].getRadius())):
				# Finds which quadrant the ball compared to the rock is in
				quadrant = None

				# Checks the x value if negative
				if (center.getX() - rocks[i].getCenter().getX() < 0):
					# Checks the y value if negative
					if (center.getY() - rocks[i].getCenter().getY() < 0):
						quadrant = 3
					# Checks the y value if positive
					elif (center.getY() - rocks[i].getCenter().getY() > 0):
						quadrant = 2
				# Checks the x value if positive 
				elif (center.getX() - rocks[i].getCenter().getX() > 0):
					# Checks the y value if negative
					if (center.getY() - rocks[i].getCenter().getY() < 0):
						quadrant = 4
					# Checks the y value if positive
					elif (center.getY() - rocks[i].getCenter().getY() > 0):
						quadrant = 1
				
				# Reconstructs point to find the adjacent length
				adjacentPoint = Point(rocks[i].getCenter().getX(), center.getY())
				adjacentDist = distance(adjacentPoint, rocks[i].getCenter())

				# Gets the angle from the adjacent side to the hypotnuse
				radianAmnt = m.acos(adjacentDist / curDist)
				degreeAmnt = radianAmnt * (180 / m.pi)

				# Swaps the angle around the correct way in the 2nd and 4th quadrant
				if (quadrant == 2):
					moveDegree = (90 - degreeAmnt) + 180

				elif (quadrant == 4):
					moveDegree = (90 - degreeAmnt) - 180

				else:
					moveDegree = float(degreeAmnt)


				# Adds the amount of quadrants to the moveDegree
				moveDegree += (90 * (quadrant - 1))
				moveDegreeList = [moveDegree]

				# Gets the distance to move the ball
				moveDist = (radius + rocks[i].getRadius()) - curDist

				# Moves the ball off the rock
				moveBall(ball, moveDegreeList, moveDist, polyBall, win)

				# Used for checking if collisions have correct angle
				"""print()
				print(moveDegree)
				print(moveDist)
				time.sleep(1)#"""		

				# Gets the new rotation for the ball when a rock is hit
				curDirection[0] += collideRockRot(win, curDirection, quadrant, ball, rocks[i], moveDegree, collideRockRotDebugOn)		
				
				# Changes the color of the rock if it can based off of hit value
				updateRock(rocks, hitList, i, polyRockList, win)

# Checks if a ball hit a rock
def didCollide(rocks: list, hitList: list, ball: Circle, polyRockList: list, win, polyBall):
	# Sets ball variables
	center = ball.getCenter()
	radius = ball.getRadius()
	hitCounter = 0

	# Runs through every rock checking to see if the rock was hit
	for i in range(len(rocks)):
		# Checks to see if the ball is hitting a rock
		if (distance(center, rocks[i].getCenter()) <= (radius + rocks[i].getRadius())):

			# Adds one to the rocks hit counter and regular
			hitList[i] += 1
			hitCounter += 1

	# Checks if a rock was hit
	if (hitCounter > 0):
		# If it has the max hits add to delete list
		delList = []
		if not hitList.__contains__([]):
			for i in range(len(hitList)):
				if (hitList[i] > thrdReq):
					delList.append(i)

		# If it's in delete list run backwards through list and delete
		if not delList.__contains__([]):
			for i in range(len(delList)):
				newIndex = (i + 1) * -1

				# Spaws a crystal where the rock was destoryed
				generateCrystal(win, rocks[delList[newIndex]].getCenter(), polyBall)

				hitList.pop(delList[newIndex])
				rocks.pop(delList[newIndex])
				polyRockList[delList[newIndex]].undraw()
				polyRockList.pop(delList[newIndex])

		return True
	
	else:
		return False

# Updates the rocks' color based on its hit value
def updateRock(rocks: list, hitList: list, index, polyRockList: list, win: GraphWin):
	

	# Sets the rock to the first color
	if (hitList[index] < secndReq):
		for g in range(len(polyRockList[index].poly)):
			# Sets base color
			if g == 0:
				polyRockList[index].setColor(g, "black")
			# Sets base shadow color
			elif g == 1 or g == 2:
				polyRockList[index].setColor(g, RockColorThree)
			# Sets bits color
			elif rockBits.__contains__(g):
				polyRockList[index].setColor(g, RockColorOne)
			# Sets bits shadows color
			elif rockBitsShadows.__contains__(g):
				polyRockList[index].setColor(g, RockColorTwo)
			

	# Sets the rock to the second color
	elif (hitList[index] < thrdReq):
		for g in range(len(polyRockList[index].poly)):
			# Sets base color
			if g == 0:
				polyRockList[index].setColor(g, "black")
			# Sets base shadow color
			elif g == 1 or g == 2:
				polyRockList[index].setColor(g, "black")
			# Sets bits color
			elif rockBits.__contains__(g):
				polyRockList[index].setColor(g, RockColorTwo)
			# Sets bits shadows color
			elif rockBitsShadows.__contains__(g):
				polyRockList[index].setColor(g, RockColorThree)
			

	# Sets the rock to the fourth color
	elif (hitList[index] < frthReq):
		for g in range(len(polyRockList[index].poly)):
			# Sets base color
			if g == 0:
				polyRockList[index].setColor(g, "black")
			# Sets base shadow color
			elif g == 1 or g == 2:
				polyRockList[index].setColor(g, "black")
			# Sets bits color
			elif rockBits.__contains__(g):
				polyRockList[index].setColor(g, "black")
			# Sets bits shadows color
			elif rockBitsShadows.__contains__(g):
				polyRockList[index].setColor(g, "black")

	# If the rock hasn't been hit the max times
	if (hitList[index] < frthReq):
		shrinkRock(rocks, index, polyRockList, rockShrink, win)

# Shrinks the rock after being hit
def shrinkRock(rocks: list, index, polyRockList: list, shrinkAmnt, win):
	# Gets the circle in the rocks list
	curCollider = rocks[index]

	# Gets the area of the current circle
	areaCircle = math.pi * (curCollider.getRadius() ** 2)

	# Gets the area of the new circle based on the shrink amount
	newArea = areaCircle * shrinkAmnt

	# Gets the new radius of the circle based on the new area
	newRadius = math.sqrt(newArea / math.pi)
	
	# Gets the new circle for the rocks list
	newCircle = Circle(rocks[index].getCenter(), newRadius)
	rocks[index] = newCircle

	# Shrinks the polyRock and picks a random new rotation
	newRot = random.uniform(1, 360)
	polyRockList[index].scaleRot(win, shrinkAmnt, newRot)

# Checks if all the rocks are destroyed and if so end the game
def checkWin(rocks: list, startTime, maxTime):
	# Checks if any rocks are left
	try :
		if rocks[0] == []:
			pass
		winner = False

	except:
		winner = True

	
	# Defines the time left after winning
	winTime = round(maxTime - (time.time()- startTime), 2)

	return winner, winTime

# Undraws the entire list of items
def clearWindow(itemsToClear: list):
	for item in itemsToClear:
		item.undraw()

# Runs the game
def playGame():
	# Creates the window
	win = createWindow()
	
	# Shows the instructions
	instructions(win)

	# Sets up the game loop
	playing = True
	while playing == True:
		# Spawns in the ball
		ball, polyBall = spawnBall(win)

		# Sets up the start for the ball
		curDirection = [random.uniform(0, 360)]
		#curDirection = [0]
		moveSpeed = 2

		# Lets the user place rocks
		placeAmnt = 5
		rocks, polyRockList = generateRocks(win, placeAmnt, RockColorOne, ball, polyBall, curDirection)


		# Creates a list to hold which rocks got hit in how many times
		hitList = [0] * placeAmnt
		

		# Sets up the time
		startTime = time.time()
		maxTime = 30
		instruct = textE(Point(50, 10), maxTime, textSize, HighlightColor)
		instruct.draw(win)

		# Moves the ball around the screen unilt the time is up or the player wins
		winner = False
		while (checkTime(startTime, time.time(), maxTime) and winner == False):
			# Moves the ball
			time.sleep(.01)
			quadDelta = moveBall(ball, curDirection, moveSpeed, polyBall, win)

			# Keeps the angle in range to prevent overflow
			while (curDirection[0] > 360):
				curDirection[0] -= 360

			# Displays the time left
			instruct.setText(f"{round(maxTime - (time.time()- startTime), 1)}")

			# Checks for collisions
			checkWallCollision(ball, curDirection, quadDelta, polyBall, win)
			checkRockCollision(ball, curDirection, rocks, hitList, RockColorOne, RockColorTwo, RockColorThree, polyRockList, win, polyBall)

			# Checks if the player won before the time ended
			winner, winTime = checkWin(rocks, startTime, maxTime)

		# Updates the instruction 
		instruct.undraw()
		if (winner == False):
			instruct.setText(f"You broke {placeAmnt - len(rocks)} rock(s)!")
		elif (winner == True):
			instruct.setText(f"You broke {placeAmnt - len(rocks)} rocks!\nYou won with {winTime} seconds left!!")
		instruct.draw(win)

		# Creates buttons
		replayButton = Button(Point(25, 50), 25, 8, "Replay", textSize, InsideColor, HighlightColor, BorderColor, 5)
		quitButton = Button(Point(75, 50), 25, 8, "Quit", textSize, InsideColor, HighlightColor, BorderColor, 5)
		replayButton.draw(win)
		quitButton.draw(win)

		# Checks for which button is pressed
		notPressed = True
		while (notPressed):
			# Finds where the user last clicked
			click = win.checkMouse()

			# If the replay button is pressed keep playing
			if replayButton.checkButton(click):
				notPressed = False
				playing = True

			# If quit button is pressed close the program
			if quitButton.checkButton(click):
				notPressed = False
				playing = False
			

		# Clears the window
		undrawList = [polyBall, instruct, replayButton, quitButton]
		undrawList.extend(polyRockList)
		undrawList.extend(crystals)
		clearWindow(undrawList)
		crystals.clear()



	# Closes the window
	win.close()

playGame()