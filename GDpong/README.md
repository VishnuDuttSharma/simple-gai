## GDpong: Gradient Descent based Pong

This is a very simple game of pong where the bat should move left or right to avoid the ball hitting the ground/base. In the best scenario, the bat should move with the same velocity as that of the ball.
However in this case, the output, the velocity (in x-direction) of the bat is dependent on four parameters: 
(1) velocity (in x-direction) 
(2) velocity (in y-direction) 
(3) ball position (x-coordinate) 
(4) ball position (y-coordination)

The last two are scaled down to get a faster concergence.

The vector changes using gradient descent with desired output for each game being the ball's velocity(which is chosen randomly at the start of the game). The learning rate is also scaled by the score in the game(number of times bat succefully hit the ball back).