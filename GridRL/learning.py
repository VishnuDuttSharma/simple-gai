from reinf import *
from gridui import *
import random
from IPython.core.display import clear_output
from jinja2.optimizer import Optimizer
from keras.backend.common import epsilon
import sys
import time

sys.setrecursionlimit(10000)


def testAlgo(init=0, ui_flag=True):
    i = 0
    player_loc = None
    wall_loc = None
    pit_loc = None
    goal_loc = None
    myapp = None
    myroot = None
    
    if init == 0:
        state = initGrid()
    elif init == 1:
        state = initGridPlayer()
    elif init == 2:
        state = initGridRand()
        
        
    raw_input('Input something')
    if( ui_flag):
        myroot = Tk()
        print 'Inside'
        player_loc  = findLoc(state, np.array([0, 0, 0, 1]))
        wall_loc    = findLoc(state, np.array([0, 0, 1, 0]))
        pit_loc     = findLoc(state, np.array([0, 1, 0, 0]))
        goal_loc    = findLoc(state, np.array([1, 0, 0, 0]))
        myapp = ui(myroot, player_loc, wall_loc, goal_loc, pit_loc)
        myroot.title("Reinforced")
        myroot.mainloop()
        
    print('Initial State:')
    print( dispGrid(state) ) 
    
    status = 1
    
    while( status == 1):
        qval = model.predict(state.reshape(1,64), batch_size=1)
        action = (np.argmax(qval))
        
        print('Move #: %s; Taking action: %s' % (i, action))
        state, valid = makeMove(state, action)
        
        if(ui_flag):
            print 'UI Action, ', action
            if action == 0:
                myapp.move_up()
            elif(action == 1):
                myapp.move_down()
            elif(action == 2):
                myapp.move_left()
            elif(action == 3):
                myapp.move_right()
            else:
                pass
                
        
        print(dispGrid(state))
        reward = getReward(state)
        
        if reward != -1:
            status = 0
            print('Reward: %s' % (reward,))
        
        i += 1
        
        if( i > 10):
            print('Game lost; too many moves.')
            break
        
        time.sleep(1.0)


def testUIAlgo(init=0):
    i = 0
    player_loc = None
    wall_loc = None
    pit_loc = None
    goal_loc = None
    myapp = None
    myroot = None
    
    if init == 0:
        state = initGrid()
    elif init == 1:
        state = initGridPlayer()
    elif init == 2:
        state = initGridRand()
        
    myroot = Tk()
#     myroot = Tk()
    player_loc  = findLoc(state, np.array([0, 0, 0, 1]))
    wall_loc    = findLoc(state, np.array([0, 0, 1, 0]))
    pit_loc     = findLoc(state, np.array([0, 1, 0, 0]))
    goal_loc    = findLoc(state, np.array([1, 0, 0, 0]))
    myapp = ui(myroot, player_loc, wall_loc, goal_loc, pit_loc)
    myroot.title("Reinforced")
#     myroot.mainloop()
        
        
    print('Initial State:')
    print( dispGrid(state) ) 

    
    valid = False
    status = 1
    
    while( status == 1):
        qval = model.predict(state.reshape(1,64), batch_size=1)
        action = (np.argmax(qval))
        
        print('Move #: %s; Taking action: %s' % (i, action))
        state, valid= makeMove(state, action)
        
        
        print 'UI Action, ', action
        if valid:
            if action == 0:
                print 'Moving up'
                myapp.move_up()
            elif(action == 1):
                print 'Moving down'
                myapp.move_down()
            elif(action == 2):
                print 'Moving left'
                myapp.move_left()
            elif(action == 3):
                print 'Moving right'
                myapp.move_right()
            else:
                pass
                
        
        print(dispGrid(state))
        reward = getReward(state)
        
        if reward != -1:
            status = 0
            print('Reward: %s' % (reward,))
        
        i += 1
        
        if( i > 10):
            print('Game lost; too many moves.')
            break
        
        myroot.update()
        time.sleep(1.0)


def testAlgoHard(init = 0):
    model.compile(loss='mse', optimizer=rms)
    
    
    epochs      =   1000
    gamma       =   0.9
    epsilon     =   1
    batchSize   =   40
    buffer      =   80
    replay = []
    
    h = 0
    for i in range(epochs):
        state   =   initGridPlayer()
        
        status  =   1
        
        while( status == 1):
            qval = model.predict(state.reshape(1, 64), batch_size = 1)
            
            if(random.random() < epsilon):
                action = np.random.randint(0, dimension[0])
            else:
                action = (np.argmax(qval))
            
            new_state, valid = makeMove(state, action)
            reward  = getReward(new_state)
            
            if(len(replay) < buffer):
                replay.append(state, action, reward, new_state)
            else:
                if( h < (buffer-1)):
                    h += 1
                else:
                    h = 0
                
                replay[h] = (state, action, reward, new_state)
                
                minibatch = random.sample(replay, batchSize)
                X_train = []
                y_train = []
                
                for memory in minibatch:
                    old_state, action, reward, new_state = memory
                    old_qval = model.predict(old_state.reshape(1, 64), batch_size=1)
                    
                    newQ = model.predict(new_state.reshape(1, 64), batch_size=1)
                    maxQ = np.max(newQ)
                    
                    y = np.zeros((1, dimension[0]))
                    y[:] = old_qval[:]
                    
                    if reward == -1:
                        update = (reward + gamma*maxQ)
                    else:
                        update = reward
                    
                    y[0][action] = update
                    X_train.append(old_state.reshape(64, ))
                    y_train.append(y.reshape(dimension[0]))
                    
                X_train = np.array(X_train)
                y_train = np.array(y_train)
                print("Game #: %s" % (i,))
                model.fit(X_train, y_train, batch_size=batchSize, nb_epoch=1, verbose=1)
                state = new_state
                
            if reward != -1:
                status = 0
            clear_output(wait=True)
        if( epsilon > 0.1):
            epsilon -= (1/epochs)
                    
    

def main():
    epochs  = 1000
    gamma   = 0.9
    epsilon = 1
    
    for i in range(epochs):
        
        state = initGrid()
        status= 1
        
        while( status == 1):
            qval = model.predict(state.reshape(1, dimension[0]*dimension[1]*dimension[2]), batch_size=1)
            if(random.random() < epsilon):
                action = np.random.randint(0, dimension[0])
            else:
                action = np.argmax(qval)
                
            new_state, valid = makeMove(state, action)
            reward = getReward(new_state)
            newQ = model.predict(new_state.reshape(1, dimension[0]*dimension[1]*dimension[2]), batch_size=1)
            maxQ = np.max(newQ)
            
            y = np.zeros((1, dimension[0]))
            y[:] = qval[:]
            
            if reward == -1:
                update = reward + gamma*maxQ
            else:
                update = reward
            
            y[0][action] = update
            print("Game # :%s" % (i,))
            
            model.fit(state.reshape(1, 64), y, batch_size=1, nb_epoch=1, verbose=1)
            state = new_state
            
            if reward != -1:
                status = 0
            clear_output(wait=True)
            
        if epsilon > 0.1:
            epsilon -= (1/epochs)

def start_ui( pos_p, pos_w, pos_g, pos_pit):
    root = Tk()
    app = ui(root, pos_p, pos_w, pos_g, pos_pit)
    root.title("Tic-Tac-Toe")
    
    return app
    


main()

#testAlgoHard(init=0)
# testAlgo(init = 0, ui_flag=True)
testUIAlgo(init = 0)
