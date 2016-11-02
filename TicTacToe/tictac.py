from Tkinter import Frame, Canvas, Label, Button, LEFT,RIGHT, ALL, Tk
from random import randint

class main:
    def __init__(self,master):
            self.frame = Frame(master)
            self.frame.pack(fill="both", expand=True)
            self.canvas = Canvas(self.frame, width=300, height=300, bg='white')
            self.canvas.pack(fill="both", expand=True)
            self.frameb=Frame(self.frame)
            self.frameb.pack(fill="both", expand=True)
            self.Start1=Button(self.frameb, text='Start', height=3, command=self.start1,bg='green', fg='purple')
            
            self.Start1.pack(fill="both", expand=True, side=RIGHT)
            
            self._board()

    def start1(self):
        self.canvas.delete(ALL)
        self.Start1.configure(bg = "yellow", text='Restart')
        self.canvas.bind("<ButtonPress-1>", self.play)  
        self._board()
        self.state='---------'
        self.player = 'X'
        self.j=False
        self.endstate = 8

    def checkWin(self, board):
        for i in range(0, 3):
            if board[i*3] != '-' and len(set(board[i*3:i*3+3])) ==  1:
                #self.canvas. create_line( 50*(2*i+1), 0, 50*(2*i+1), 300, width=10, fill="red")
                self.endstate = i
                return True
        
        for i in range(0, 3):
           if board[i] != '-' and (board[i] == board[i+3]) and (board[i] ==  board[i+6]):
               #self.canvas. create_line( 0, 50*(2*i+1), 300, 50*(2*i+1), width=10, fill="red")
               self.endstate = i+3
               return True,
        
        if board[4] != '-' and board[0] == board[4] and board[4] == board[8]:
            #self.canvas. create_line( 0, 0, 300, 300, width=10, fill="red")
            self.endstate = 6
            return  True
        
        if board[4] != '-' and board[2] == board[4] and board[4] == board[6]:
            #self.canvas. create_line( 300, 0,0 ,300, width=10, fill="red")
            self.endstate = 7
            return  True
        
        return False


    def nextMove(self, board,player):
        if len(set(board)) == 1:
            return 0,4

        if player == 'O':
            nextplayer = 'X'
        else:
            nextplayer = 'O'

        
        if self.checkWin(board) :
            if player == 'X': 
                return -1,-1
            else: 
                return 1,-1
        
        res_list=[] # list for appending the result
        
        c= board.count('-')
        
        if  c is 0:
            return 0,-1
        
        _list=[] # list for storing the indexes where '-' appears
        
        for i in range(0, len(board)):
            if board[i] == '-':
                _list.append(i)
        
        #tempboardlist=list(board)
        
        for i in _list:
            s = list(board)
            s[i] = player
            board = "".join(s)

            ret,move = self.nextMove(board,nextplayer)
            res_list.append(ret)
            
            s = list(board)
            s[i] = '-'
            board = "".join(s)
            
            
        
        if player == 'X':
            max_val = max(res_list)
            return max_val,_list[res_list.index(max_val)]
        else :
            min_val = min(res_list)
            return min_val,_list[res_list.index(min_val)]



    def play(self, event):
        for k in range(0,300,100):
            for j in range(0,300,100):
                if event.x in range(k,k+100) and event.y in range(j,j+100):
                    if self.canvas.find_enclosed(k,j,k+100,j+100)==():
                        
                        X=(2*k+100)/2
                        Y=(2*j+100)/2
                        X1=int(k/100)
                        Y1=int(j/100)
                        print X, Y, X1, Y1
                        self.canvas. create_line( X+20, Y+20, X-20, Y-20, width=4, fill="black")
                        self.canvas. create_line( X-20, Y+20, X+20, Y-20, width=4, fill="black")
                        

                        s = list(self.state)
                        s[3*Y1+X1] = 'X'
                        self.state = "".join(s)
                        print self.state
                        if self.checkWin(self.state):
                            print 'Player Won!!!'
                            self.end()
                            return



                        w, nm = self.nextMove(self.state, 'O')
                        
                        #print w, nm
                        if nm == -1:
                            print 'Game Draw!!!'
                            self.endstate = 8
                            self.end()
                            return

                        s = list(self.state)
                        s[nm] = 'O'
                        self.state = "".join(s)
                        X1 = nm%3
                        Y1 = nm/3
                        X = 50*(2*X1+1)
                        Y = 50*(2*Y1+1)
                        self.canvas.create_oval( X+25, Y+25, X-25, Y-25, width=4, outline="black")
                        print self.state
                        if self.checkWin(self.state):
                            print 'Computer Won!!!'
                            self.end()
                            return
                            


    def end(self):
        self.Start1.configure(bg = "green", text='Start')
        self.canvas.unbind("<ButtonPress-1>")
        self.j=True

        if( self.endstate < 3):
            i = self.endstate
            
            self.canvas. create_line( 0, 50*(2*i+1), 300, 50*(2*i+1), width=10, fill="red")
        elif( self.endstate < 6):
            i = self.endstate-3
            self.canvas. create_line( 50*(2*i+1), 0, 50*(2*i+1), 300, width=10, fill="red")
        elif self.endstate == 6:
            self.canvas. create_line( 0, 0, 300, 300, width=10, fill="red")
        elif self.endstate == 7:
            self.canvas. create_line( 300, 0,0 ,300, width=10, fill="red")
        else:
            pass

    def _board(self):
        self.canvas.create_rectangle(0,0,300,300, outline="black")
        self.canvas.create_rectangle(100,300,200,0, outline="black")
        self.canvas.create_rectangle(0,100,300,200, outline="black")
        


root=Tk()
app=main(root)
root.title("Tic-Tac-Toe")
root.mainloop()
