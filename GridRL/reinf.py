import numpy as np
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation
from keras.optimizers import RMSprop
from scipy.cluster.hierarchy import is_monotonic


dimension = (4,4,4)

def randPair(start, end):
    return np.random.randint(start,end), np.random.randint(start, end)

def findLoc(state, obj):
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            if (state[i, j] == obj).all():
                return i,j

def initGrid():
    state = np.zeros(dimension)
    
    state[0, 1] = np.array([0, 0, 0, 1])
    state[2, 2] = np.array([0, 0, 1, 0])
    state[1, 1] = np.array([0, 1 ,0, 0])
    state[3, 3] = np.array([1 ,0 ,0 ,0])
    
    return state

def initGridPlayer():
    state = np.zeros(dimension)
    
    state[randPair(0, 4)] = np.array([0, 0, 0, 1])
    state[2, 2] = np.array([0, 0, 1, 0])
    state[1, 1] = np.array([0, 1 ,0, 0])
    state[3, 3] = np.array([1 ,0 ,0 ,0])
    
    agent = findLoc(state, np.array([0, 0, 1, 1]))
    wall  = findLoc(state, np.array([0, 0, 1, 0]))
    pit   = findLoc(state, np.array([0 ,1 ,0, 0]))
    goal  = findLoc(state, np.array([1 ,0 ,0, 0]))
    
    if( not agent or not wall or not goal or not pit):
        return initGridPlayer()
    
    return state

def initGridRand():
    state = np.zeros(dimension)
    
    state[randPair(0, 4)] = np.array([0, 0, 0, 1])
    state[randPair(0, 4)] = np.array([0, 0, 1, 0])
    state[randPair(0, 4)] = np.array([0, 1 ,0, 0])
    state[randPair(0, 4)] = np.array([1 ,0 ,0 ,0])
    
    agent = findLoc(state, np.array([0, 0, 0, 1]))
    wall  = findLoc(state, np.array([0, 0, 1, 0]))
    pit   = findLoc(state, np.array([0 ,1 ,0, 0]))
    goal  = findLoc(state, np.array([1 ,0 ,0, 0]))
    
    if( not agent or not wall or not goal or not pit):
        return initGridPlayer()
    
    return state

def makeMove(state, action):
    player_loc  = findLoc(state, np.array([0, 0, 0, 1]))
    wall_loc    = findLoc(state, np.array([0, 0, 1, 0]))
    pit_loc     = findLoc(state, np.array([0, 1, 0, 0]))
    goal_loc    = findLoc(state, np.array([1, 0, 0, 0]))
    
    state = np.zeros(dimension)
    
    is_move = False
    
    if action == 0:
        new_loc = (player_loc[0] - 1, player_loc[1])
        if new_loc != wall_loc:
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][3] = 1
                is_move = True
    
    elif action==1:
        new_loc = (player_loc[0] + 1, player_loc[1])
        if (new_loc != wall_loc):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][3] = 1
                is_move = True
    #left (column - 1)
    elif action==2:
        new_loc = (player_loc[0], player_loc[1] - 1)
        if (new_loc != wall_loc):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][3] = 1
                is_move = True
    #right (column + 1)
    elif action==3:
        new_loc = (player_loc[0], player_loc[1] + 1)
        if (new_loc != wall_loc):
            if ((np.array(new_loc) <= (3,3)).all() and (np.array(new_loc) >= (0,0)).all()):
                state[new_loc][3] = 1
                is_move = True

    new_player_loc = findLoc(state, np.array([0,0,0,1]))
    if (not new_player_loc):
        state[player_loc] = np.array([0,0,0,1])
    #re-place pit
    state[pit_loc][1] = 1
    #re-place wall
    state[wall_loc][2] = 1
    #re-place goal
    state[goal_loc][0] = 1

    return state,is_move

def getLoc(state, level):
    for i in range(dimension[0]):
        for j in range(dimension[1]):
            if state[i, j][level] == 1:
                return i,j

def getReward(state):
    player_loc = getLoc(state, 3)
    pit_loc    = getLoc(state, 1)
    goal_loc   = getLoc(state, 0)
    
    if player_loc == pit_loc:
        return -10
    elif player_loc == goal_loc:
        return 10
    else:
        return -1
    
def dispGrid(state):
    grid = ('*'*dimension[0]+'\n')*dimension[1]
    player_loc = findLoc(state, np.array([0,0,0,1]))
    wall_loc = findLoc(state, np.array([0,0,1,0]))
    pit_loc = findLoc(state, np.array([0,1,0,0]))
    goal_loc = findLoc(state, np.array([1,0,0,0]))
    

    if player_loc:
#         print player_loc
        loc = player_loc[1]+player_loc[0]*(dimension[0]+1)
        grid = grid[:loc]+'P'+grid[loc+1:]
    if wall_loc:
#         print wall_loc
        loc = wall_loc[1]+ wall_loc[0]*(dimension[0]+1)
        grid = grid[:loc]+'W'+grid[loc+1:]
    if goal_loc:
#         print goal_loc
        loc = goal_loc[1]+goal_loc[0]*(dimension[0]+1)
        grid = grid[:loc]+'+'+grid[loc+1:]
    if pit_loc:
#         print pit_loc
        loc = pit_loc[1]+pit_loc[0]*(dimension[0]+1)
        grid = grid[:loc]+'-'+grid[loc+1:]

    return grid

def main():
    state = initGrid()
    print dispGrid(state)
    
    state = makeMove(state, 3)
    state = makeMove(state, 1)
    state = makeMove(state, 3)
    state = makeMove(state, 1)
    
   
    print('Reward: %s' % (getReward(state),))
    print dispGrid(state)
    
    
    model = Sequential()
    model.add(Dense(164, init='lecun_uniform', input_shape=(64,)))
    model.add(Activation('relu'))
    
    
    model.add(Dense(150, init='lecun_uniform'))
    model.add(Activation('relu'))
    
    
    model.add(Dense(4, init='lecun_uniform'))
    model.add(Activation('linear'))
    
    rms= RMSprop()
    model.compile(loss='mse', optimizer=rms)
        
    print model.predict(state.reshape(1,64), batch_size=1)
    
    
# if __name__ == "__main__":
#     main()

model = Sequential()
model.add(Dense(164, init='lecun_uniform', input_shape=(64,)))
model.add(Activation('relu'))


model.add(Dense(150, init='lecun_uniform'))
model.add(Activation('relu'))


model.add(Dense(4, init='lecun_uniform'))
model.add(Activation('linear'))

rms= RMSprop()
model.compile(loss='mse', optimizer=rms)
    

