from Tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk

size = 4

class ui:
    def __init__(self, master, pos_p, pos_w, pos_g, pos_pit ):
        global size
        
        self.root   =   master
        self.frame  =   Frame(master)
        self.frame.pack(fill='both', expand=True)
        self.canvas = Canvas(self.frame, width=100*size, height=100*size)
        self.canvas.pack(fill='both', expand=True)
        self.frameb=Frame(self.frame)
        self.frameb.pack(fill="both", expand=True)
        self.Start1=Button(self.frameb, text='Start', height=4, command=self.start1,bg='green', fg='purple')
        self.Start1.pack(fill="both", expand=True, side=RIGHT)
        

        self._board()
        self.size = size
        
        self.player_pos = [pos_p[0], pos_p[1]]
        self.wall_pos   = [pos_w[0], pos_w[1]]
        self.goal_pos   = [pos_g[0], pos_g[1]]
        self.pit_pos    = [pos_pit[0], pos_pit[1]]
        
        self.player = self.canvas.create_oval( 25, 25, 75, 75, width=4, outline="green", fill='green')
        self.wall   = self.canvas.create_rectangle(0, 0, 100, 100, 
    outline="#f11", fill="#1f1", width=2)
        self.pit   = self.canvas.create_rectangle(0, 0, 100, 100, fill="black", width=2)
        self.goal = self.canvas.create_oval( 25, 25, 75, 75, width=4, outline="red", fill='red')

        print self.player_pos

        self.canvas.move(self.player, 100*self.player_pos[1], 100*self.player_pos[0])
        self.canvas.move(self.wall, 100*self.wall_pos[1], 100*self.wall_pos[0])
        self.canvas.move(self.goal, 100*self.goal_pos[1], 100*self.goal_pos[0])
        self.canvas.move(self.pit, 100*self.pit_pos[1], 100*self.pit_pos[0])
        
    def start1(self):
        self.canvas.delete(ALL)
        print 'Start1'
        self.Start1.configure(bg = "yellow", text='Restart')

        
        #self.canvas.bind("<ButtonPress-1>", self.play2)  
        
        self._board()
        self.j=False

        print self.player_pos
        print self.wall_pos
        print self.goal_pos
        print self.pit_pos
        
        self.canvas.move(self.player, 100*self.player_pos[0], 100*self.player_pos[1])
        self.canvas.move(self.wall, 100*self.wall_pos[0], 100*self.wall_pos[1])
        self.canvas.move(self.goal, 100*self.goal_pos[0], 100*self.goal_pos[1])
        self.canvas.move(self.pit, 100*self.pit_pos[0], 100*self.pit_pos[1])
     
     
    def _board(self):
        for i in range(size):
            for j in range(size):
                self.canvas.create_rectangle(100*i,100*j,100*i+100,100*j+100, outline="black")   
        
    def move_up(self):
        self.canvas.move(self.player, 0, -100)
    
    def move_down(self):
        self.canvas.move(self.player, 0, 100)
        
    def move_left(self):
        self.canvas.move(self.player, -100, 0)
    
    def move_right(self):
        self.canvas.move(self.player, 100, 0)
        
    def update(self):
        pass
