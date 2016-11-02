# Simple pong game - don't let the ball hit the bottom!
# KidsCanCode - Intro to Programming
import Tkinter
import random
import time
import math
import environment
import qlearningAgents
import threading
import sys


weight = [random.random(), random.random(), random.random(), random.random()]
#weight = [0.1, 0.0, 0.0, 0.0]
lambd = 0.05

# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 300)
        
        self.yspeed = -random.randint(30, 50)
        self.xspeed = random.randint(1, 2)
        self.hit_bottom = False
        self.score = 0.0

    def draw(self):
    	posy = self.yspeed*0.1  + 0.5*9.8*0.01
    	self.yspeed  += 0.5*9.8*0.1
        self.canvas.move(self.id, self.xspeed, posy)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.yspeed *= -1 

        if pos[3] >= 500:
            self.yspeed *= -1
            self.score -= 100
            self.paddle.score -= 100
            self.canvas.move(self.id, 200-pos[0], 400-pos[1])
            self.yspeed = -random.randint(30, 50)
            self.xspeed = random.randint(1, 2)
            #self.hit_bottom = True
        
        if pos[0] <= 0:
            self.xspeed *= -1
            self.score -= 200
            self.paddle.score -= 10
        
        if pos[2] >=500:
            self.xspeed *= -1
            self.score -= 200
            self.paddle.score -= 10

        if self.hit_paddle(pos) == True:
            self.yspeed *= -1 
#            self.xspeed = random.randrange(-3,3)
            self.score += 100
            self.paddle.score += 100
        
        paddle_pos = self.canvas.coords(self.paddle.paddle)
        self.paddle.diff = (paddle_pos[0] - pos[0])/10.0
        #print 'Ball diff',self.paddle.diff

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.paddle)
        if (pos[0]+pos[2])/2 >= paddle_pos[0] and (pos[0]+pos[2])/2 <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1]:# and pos[3] <= paddle_pos[3]:
                #self.xspeed = (abs(self.xspeed))*(( (pos[0]+pos[2])/2.0 - (paddle_pos[0]+paddle_pos[2])/2.0)/(paddle_pos[2]-paddle_pos[0])/2.0)
                self.xspeed = abs(self.xspeed)* (1- 2*int( (paddle_pos[0]+paddle_pos[2])/2.0  >(pos[0]+pos[2])/2.0 ))
                return True
        return False


        
class CrawlingRobotEnvironment(environment.Environment):

    def __init__(self, paddlerobot):

        self.paddlerobot = paddlerobot

        self.state = None

        self.nvelstate = 5
        self.prevscore = 0.0

        # create a list of arm buckets and hand buckets to
        # discretize the state space
        minspeed = -4.0
        armIncrement = 2.0
        self.velBuckets = [minspeed+(armIncrement*i) \
           for i in range(self.nvelstate)]
        
        # Reset
        self.reset()

    def getCurrentState(self):
        """
          Return the current state
          of the crawling robot
        """
        return self.state

    def getPossibleActions(self, state):
        """
          Returns possible actions
          for the states in the
          current state
        """

        actions = list()

        currVelocity, currDiff = state[0], state[1]

        print 'Curr Diff', currDiff, currVelocity
        if currVelocity > 0: 
        	if currDiff < -10:
        		actions.append('moverightfast')
        	elif currDiff < -1:
        		actions.append('moverightslow')
        	elif currDiff < 1:
        		actions.append('stop')
        	elif currDiff < 10:
        		actions.append('moveleftslow')
        	else:
        		actions.append('moveleftfast')

        if currVelocity < 0: 
        	if currDiff < -10:
        		actions.append('moverightfast')
        	elif currDiff < -1:
        		actions.append('moverightslow')
        	elif currDiff < 1:
        		actions.append('stop')
        	elif currDiff < 10:
        		actions.append('moveleftslow')
        	else:
        		actions.append('moveleftfast')

        if currVelocity == 0:
        	if currDiff < -10:
        		actions.append('moverightfast')
        	elif currDiff < -1:
        		actions.append('moverightslow')
        	elif currDiff < 1:
        		actions.append('stop')
        	elif currDiff < 10:
        		actions.append('moveleftslow')
        	else:
        		actions.append('moveleftfast')

   		print actions
        return actions

    def doAction(self, action):
        """
          Perform the action and update
          the current state of the Environment
          and return the reward for the
          current state, the next state
          and the taken action.

          Returns:
            nextState, reward
        """
        nextState, reward =  None, None

        velBucket, diffBucket = int(self.state[0]), self.state[1]
        
        if action == 'moveleftfast':
        	if(velBucket == 0):
        		velBucket = 1
        	newVel = self.velBuckets[velBucket-1]
        	self.paddlerobot.moveleft(newVel)
        	nextState = (velBucket-1), self.paddlerobot.diff -4.0

        if action == 'moverightfast':
        	if velBucket == len(self.velBuckets)-1:
        		velBucket -= 1
        	newVel = self.velBuckets[velBucket+1]
        	self.paddlerobot.moveright(newVel)
        	nextState = (velBucket+1), self.paddlerobot.diff + 4.0

        if action == 'moveleftslow':
        	if(velBucket == 0):
        		velBucket = 1
        	newVel = self.velBuckets[velBucket-1]
        	self.paddlerobot.moveleft(newVel)
        	nextState = (velBucket-1), self.paddlerobot.diff -2.0

        if action == 'moverightslow':
        	if velBucket == len(self.velBuckets)-1:
        		velBucket -= 1
        	newVel = self.velBuckets[velBucket+1]
        	self.paddlerobot.moveright(newVel)
        	nextState = (velBucket+1), self.paddlerobot.diff + 2.0
        
        if action == 'stop':
            self.paddlerobot.stop1()
            nextState = 0, self.paddlerobot.diff
        
        
        self.score = self.paddlerobot.getScore()
        reward = self.score - self.prevscore #- self.paddlerobot.diff/2.0
        #print reward
        self.prevscore = self.paddlerobot.score

        self.state = nextState
        return nextState, reward


    def reset(self):
        """
         Resets the Environment to the initial state
        """
        ## Initialize the state to be the middle
        ## value for each parameter e.g. if there are 13 and 19
        ## buckets for the arm and hand parameters, then the intial
        ## state should be (6,9)
        ##
        ## Also call self.crawlingRobot.setAngles()
        ## to the initial arm and hand angle

        velState = 0.0
        diffState = 10.0
        
        self.state = velState, diffState

        #self.crawlingRobot.setAngles(self.velBuckets[armState],self.handBuckets[handState])
        #self.crawlingRobot.positions = [20,self.crawlingRobot.getRobotPosition()[0]]


class Paddle:
    def setVel(self, velocity):
        """
            set the robot's arm and hand angles
            to the passed in values
        """
        self.xspeed = velocity
        

    def getVel(self):
        """
            returns the pair of (armAngle, handAngle)
        """
        return self.xspeed

    def getPos(self):
        """
            returns the (x,y) coordinates
            of the lower-left point of the
            robot
        """
        pos = self.canvas.coords(self.paddle)
        return (pos[0]+pos[2])/2.0, (pos[1]+pos[3])/2.0

    def getScore(self):
    	return self.score

    def stop1(self):
    	self.xspeed = 0.0


    def moveleft(self, velocity):
        """
            move the robot arm to 'newArmAngle'
        """
        
        self.xspeed = velocity
        

        # Position and Velocity Sign Post
        self.positions.append(0.0)
#        self.angleSums.append(abs(math.degrees(oldArmAngle)-math.degrees(newArmAngle)))
        if len(self.positions) > 100:
            self.positions.pop(0)
 #           self.angleSums.pop(0)

    def moveright(self, velocity):
        """
            move the robot hand to 'newArmAngle'
        """
        self.xspeed = velocity
        

        # Position and Velocity Sign Post
        self.positions.append(0.0)
#        self.angleSums.append(abs(math.degrees(oldArmAngle)-math.degrees(newArmAngle)))
        if len(self.positions) > 100:
            self.positions.pop(0)
 #           self.angleSums.pop(0)



    def getSpeeds(self):
        """
            get the lower- and upper- bound
            for the arm angles returns (min,max) pair
        """
        return self.minspeed, self.maxspeed

    def draw(self, stepCount, stepDelay):
    	velocity = self.xspeed
    	#print 'Velocity', velocity
    	pos = self.getPos()
    	#if( pos[0] <= 0 and velocity < 0 ):
    	#	return
    	#if( pos[0] >= 500 and velocity > 0 ):
    	#	return
    	print 'Velocity', velocity
    	self.canvas.move(self.paddle, velocity, 0)

    	steps = stepCount - self.lastStep
    	if steps == 0:
    		return


    def __init__(self, canvas, color):

    	self.canvas = canvas
        self.paddle = canvas.create_rectangle(0,0, 100, 5, fill=color)
        self.canvas.move(self.paddle, 250, 495)
        
        self.xspeed = 0
        
        #self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        #self.canvas.bind_all('<KeyPress-Right>', self.move_right)
        ## Canvas ##
        
        
        self.lastStep = 0
#        self.lastVel = 0

        ## Arm and Hand Degrees ##
        self.velocity = 0.0
        self.positions = [0]
        self.score = 0.0
        self.diff = 0.0
        #self.maxHandAngle = 0
        #self.minHandAngle = -(5.0/6.0) * PI
		

def multiply(a, b):
	prod = 0.0
	for i in range(len(a)):
		prod += a[i]*b[i]
	return prod

def update(weight, lambd, y, x, score):
	print 'Weight', weight
	print 'Lambda', lambd
	print 'Y', y
	print 'X', x
	print 'Score', score
	print 'Product',multiply(weight, x)
	sumi = (multiply(weight, x) - y)/float(len(weight))

	for i in range(len(weight)):
		weight[i] = weight[i] - lambd*sumi*x[i]/float(score+1)

	return weight

def ai(ball, paddle):
	global weight
	pos = ball.canvas.coords(ball.id)
	[bx, by, px, py] = [ball.xspeed, ball.yspeed, (pos[1]+pos[3])/400.0, (pos[0]+pos[2])/500.0]
	paddle.xspeed = multiply([bx, by, px, py], weight)
	#print paddle.xspeed
	


class Application:

    def sigmoid(self, x):
        return 1.0 / (1.0 + 2.0 ** (-x))

    def incrementSpeed(self, inc):
        self.tickTime *= inc
#        self.epsilon = min(1.0, self.epsilon)
#        self.epsilon = max(0.0,self.epsilon)
#        self.learner.setSpeed(self.epsilon)
        self.speed_label['text'] = 'Step Delay: %.5f' % (self.tickTime)

    def incrementEpsilon(self, inc):
        self.ep += inc
        self.epsilon = self.sigmoid(self.ep)
        self.learner.setEpsilon(self.epsilon)
        self.epsilon_label['text'] = 'Epsilon: %.3f' % (self.epsilon)

    def incrementGamma(self, inc):
        self.ga += inc
        self.gamma = self.sigmoid(self.ga)
        self.learner.setDiscount(self.gamma)
        self.gamma_label['text'] = 'Discount: %.3f' % (self.gamma)

    def incrementAlpha(self, inc):
        self.al += inc
        self.alpha = self.sigmoid(self.al)
        self.learner.setLearningRate(self.alpha)
        self.alpha_label['text'] = 'Learning Rate: %.3f' % (self.alpha)

    def __initGUI(self, win):
        ## Window ##
        self.win = win

        ## Initialize Frame ##
        win.grid()
        self.dec = -.5
        self.inc = .5
        self.tickTime = 0.1

        ## Epsilon Button + Label ##
        self.setupSpeedButtonAndLabel(win)

        self.setupEpsilonButtonAndLabel(win)

        ## Gamma Button + Label ##
        self.setUpGammaButtonAndLabel(win)

        ## Alpha Button + Label ##
        self.setupAlphaButtonAndLabel(win)

        ## Exit Button ##
        #self.exit_button = Tkinter.Button(win,text='Quit', command=self.exit)
        #self.exit_button.grid(row=0, column=9)

        ## Simulation Buttons ##
#        self.setupSimulationButtons(win)

         ## Canvas ##
        self.canvas = Tkinter.Canvas(root, height=500, width=500)
        self.canvas.grid(row=2,columnspan=10)

    def setupAlphaButtonAndLabel(self, win):
        self.alpha_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementAlpha(self.dec)))
        self.alpha_minus.grid(row=1, column=3, padx=10)

        self.alpha = self.sigmoid(self.al)
        self.alpha_label = Tkinter.Label(win, text='Learning Rate: %.3f' % (self.alpha))
        self.alpha_label.grid(row=1, column=4)

        self.alpha_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementAlpha(self.inc)))
        self.alpha_plus.grid(row=1, column=5, padx=10)

    def setUpGammaButtonAndLabel(self, win):
        self.gamma_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementGamma(self.dec)))
        self.gamma_minus.grid(row=1, column=0, padx=10)

        self.gamma = self.sigmoid(self.ga)
        self.gamma_label = Tkinter.Label(win, text='Discount: %.3f' % (self.gamma))
        self.gamma_label.grid(row=1, column=1)

        self.gamma_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementGamma(self.inc)))
        self.gamma_plus.grid(row=1, column=2, padx=10)

    def setupEpsilonButtonAndLabel(self, win):
        self.epsilon_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementEpsilon(self.dec)))
        self.epsilon_minus.grid(row=0, column=3)

        self.epsilon = self.sigmoid(self.ep)
        self.epsilon_label = Tkinter.Label(win, text='Epsilon: %.3f' % (self.epsilon))
        self.epsilon_label.grid(row=0, column=4)

        self.epsilon_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementEpsilon(self.inc)))
        self.epsilon_plus.grid(row=0, column=5)

    def setupSpeedButtonAndLabel(self, win):
        self.speed_minus = Tkinter.Button(win,
        text="-",command=(lambda: self.incrementSpeed(.5)))
        self.speed_minus.grid(row=0, column=0)

        self.speed_label = Tkinter.Label(win, text='Step Delay: %.5f' % (self.tickTime))
        self.speed_label.grid(row=0, column=1)

        self.speed_plus = Tkinter.Button(win,
        text="+",command=(lambda: self.incrementSpeed(2)))
        self.speed_plus.grid(row=0, column=2)







    def skip5kSteps(self):
        self.stepsToSkip = 5000

    def __init__(self, win):

        self.ep = 0
        self.ga = 2
        self.al = 2
        self.stepCount = 0
        ## Init Gui

        self.__initGUI(win)

        
        self.robot = Paddle(self.canvas, 'blue')
        self.robotEnvironment = CrawlingRobotEnvironment(self.robot)
        self.ball = Ball(self.canvas, 'red', 25, self.robot)
        

        # Init Agent
        simulationFn = lambda agent: \
          simulation.SimulationEnvironment(self.robotEnvironment,agent)
        actionFn = lambda state: \
          self.robotEnvironment.getPossibleActions(state)
        self.learner = qlearningAgents.QLearningAgent(actionFn=actionFn)

        self.learner.setEpsilon(self.epsilon)
        self.learner.setLearningRate(self.alpha)
        self.learner.setDiscount(self.gamma)

        # Start GUI
        self.running = True
        self.stopped = False
        self.stepsToSkip = 0
        self.thread = threading.Thread(target=self.run)
        self.thread.start()


    def exit(self):
        self.running = False
        for i in range(5):
            if not self.stopped:
                time.sleep(0.1)
        try:
            self.win.destroy()
        except:
            pass
        sys.exit(0)

    def step(self):

        self.stepCount += 1

        state = self.robotEnvironment.getCurrentState()
        actions = self.robotEnvironment.getPossibleActions(state)
        if len(actions) == 0.0:
            self.robotEnvironment.reset()
            state = self.robotEnvironment.getCurrentState()
            actions = self.robotEnvironment.getPossibleActions(state)
            print 'Reset!'
        action = self.learner.getAction(state)
        if action == None:
            raise 'None action returned: Code Not Complete'
        nextState, reward = self.robotEnvironment.doAction(action)
        
        self.learner.observeTransition(state, action, nextState, reward)


    def run(self):
        self.stepCount = 0
        self.learner.startEpisode()
        while True:
            minSleep = .01
            tm = max(minSleep, self.tickTime)
            time.sleep(tm)
            self.stepsToSkip = int(tm / self.tickTime) - 1

            if not self.running:
                self.stopped = True
                return
            for i in range(self.stepsToSkip):
                self.step()
            self.stepsToSkip = 0
            self.step()
#          self.robot.draw()
        self.learner.stopEpisode()

    def start(self):
        self.win.mainloop()





def run():
    global root
    root = Tkinter.Tk()
    root.title( 'Crawler GUI' )
    root.resizable( 0, 0 )

#  root.mainloop()


    app = Application(root)
    def update_gui():
        app.robot.draw(app.stepCount, app.tickTime)
        app.ball.draw()
        root.after(10, update_gui)
    update_gui()

    root.protocol( 'WM_DELETE_WINDOW', app.exit)
    try:
        app.start()
    except:
        app.exit()


if __name__ == '__main__':
    run()

# # Create window and canvas to draw on
# tk = Tk()
# tk.title("GD Pong")

# canvas = Canvas(tk, width=500, height=400, bd=0, bg='papaya whip')
# canvas.pack()
# label = canvas.create_text(5, 5, anchor=NW, text="Score: 0")
# tk.update()
# i = 0
# while(i < 1000):
# 	canvas.delete("all")

	
	

# 	paddle = Paddle(canvas, 'blue')
# 	ball = Ball(canvas, 'red', 25, paddle)
# 	canvas.itemconfig(label, text="Score: "+str(ball.score))
# 	# Animation loop
# 	while ball.hit_bottom == False:
# 	    ball.draw()
# 	    paddle.draw()
# 	    #paddle.draw(app.stepCount, app.tickTime)

# 	    #ai(ball, paddle)
# 	    canvas.itemconfig(label, text="Score: "+str(ball.score))
# 	    tk.update_idletasks()
# 	    tk.update()
# 	    time.sleep(0.01)

# 	pos = ball.canvas.coords(ball.id)
# 	weight = update(weight, lambd, ball.xspeed, [ball.xspeed, ball.yspeed, (pos[1]+pos[3])/400.0, (pos[0]+pos[2])/500.0], ball.score )
# 	#weight[1] = 0.0
# 	#weight[2] = 0.0
# 	#weight[3] = 0.0
# 	print 'Completed Iteration:',i
# 	ball.score = 0
# 	i += 1

# # Game Over
# go_label = canvas.create_text(250,200,text="GAME OVER",font=("Helvetica",30))
# tk.update()



