# Simple pong game - don't let the ball hit the bottom!
# KidsCanCode - Intro to Programming
from Tkinter import *
import random
import time

#weight = [random.random(), random.random(), random.random(), random.random()]
weight = [0.1, 0.0, 0.0, 0.0]
lambd = 0.05

# Define ball properties and functions
class Ball:
    def __init__(self, canvas, color, size, paddle):
        self.canvas = canvas
        self.paddle = paddle
        self.id = canvas.create_oval(10, 10, size, size, fill=color)
        self.canvas.move(self.id, 245, 100)
        
        self.yspeed = -random.randint(7, 9)
        self.xspeed = random.randint(7, -self.yspeed)
        self.hit_bottom = False
        self.score = 0

    def draw(self):
        self.canvas.move(self.id, self.xspeed, self.yspeed)
        pos = self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.yspeed *= -1 
        if pos[3] >= 400:
            self.hit_bottom = True
        if pos[0] <= 0:
            self.xspeed *= -1
        if pos[2] >= 500:
            self.xspeed *= -1
        if self.hit_paddle(pos) == True:
            self.yspeed *= -1 
#            self.xspeed = random.randrange(-3,3)
            self.score += 1

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if (pos[0]+pos[2])/2 >= paddle_pos[0] and (pos[0]+pos[2])/2 <= paddle_pos[2]:
            if pos[3] >= paddle_pos[1]:# and pos[3] <= paddle_pos[3]:
                return True
        return False

# Define paddle properties and functions
class Paddle:
    def __init__(self, canvas, color):
        self.canvas = canvas
        self.id = canvas.create_rectangle(0,0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 390)
        self.xspeed = 0
        #self.canvas.bind_all('<KeyPress-Left>', self.move_left)
        #self.canvas.bind_all('<KeyPress-Right>', self.move_right)

    def draw(self):
        self.canvas.move(self.id, self.xspeed, 0)
        pos = self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.xspeed = 0
        if pos[2] >= 500:
            self.xspeed = 0
		

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
	

# Create window and canvas to draw on
tk = Tk()
tk.title("GD Pong")

canvas = Canvas(tk, width=500, height=400, bd=0, bg='papaya whip')
canvas.pack()
label = canvas.create_text(5, 5, anchor=NW, text="Score: 0")
tk.update()
i = 0
while(i < 1000):
	canvas.delete("all")

	
	

	paddle = Paddle(canvas, 'blue')
	ball = Ball(canvas, 'red', 25, paddle)
	canvas.itemconfig(label, text="Score: "+str(ball.score))
	# Animation loop
	while ball.hit_bottom == False:
	    ball.draw()
	    paddle.draw()
	    ai(ball, paddle)
	    canvas.itemconfig(label, text="Score: "+str(ball.score))
	    tk.update_idletasks()
	    tk.update()
	    time.sleep(0.01)

	pos = ball.canvas.coords(ball.id)
	weight = update(weight, lambd, ball.xspeed, [ball.xspeed, ball.yspeed, (pos[1]+pos[3])/400.0, (pos[0]+pos[2])/500.0], ball.score )
	#weight[1] = 0.0
	#weight[2] = 0.0
	#weight[3] = 0.0
	print 'Completed Iteration:',i
	ball.score = 0
	i += 1

# Game Over
go_label = canvas.create_text(250,200,text="GAME OVER",font=("Helvetica",30))
tk.update()

