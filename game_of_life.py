import random
import time

DEAD = 0
LIVE = 1

class edgeError(Exception):
#	Custom error class to handle if situations
	pass

def dead_state(width, height):
    """Constuct an empty state with all cells set to DEAD.

    Parameters
    ----------
    width: the width of the state, in cells
    height: the height of the state, in cells

    Returns
    -------
    A state of dimensions width x height, with all cells set to DEAD
    """
    return [[DEAD for _ in range(height)] for _ in range(width)]


def random_state(width, height):
    """Construct a random state with all cells randomly set.

    Parameters
    ----------
    width: the width of the state, in cells
    height: the height of the state, in cells

    Returns
    -------
    A state of dimensions width x height, with all cells randomly set to either
        DEAD or LIVE with equal probability.
    """
    state = dead_state(width, height)
    for x in range(0, state_width(state)):
        for y in range(0, state_height(state)):
        	state[x][y] = random.randint(0,1)

    return state

def state_width(state):
    """Get the width of a state.

    Parameters
    ----------
    state: a Game state

    Returns
    -------
    The width of the input state
    """
    return len(state)

def state_height(state):
    """Get the height of a state.

    Parameters
    ----------
    state: a Game state

    Returns
    -------
    The height of the input state
    """
    return len(state[0])


def neighborCounter(statement):
	"""Function to get neighbor counter

	Parameters
	----------
	statement: Cell state

	Returns
	-------
	The counter according to cell state
	"""
	dead_or_alive = {
	LIVE: 1,
	DEAD: 0
	}
	return dead_or_alive.get(statement)

def isBelowZero(x):
	"""This is a subfunction of outOfEdgeControl
	Is cell coordinates out of edge(Below 0)?

	Parameters
	----------
	x: The coordinate number(x or y)

	Returns
	-------
	True: Yes it is below zero
	False: Above zero
	"""
	return (x<0)

def outOfEdgeControl(x,edge):
	"""This is a subfunction of edgeControl
	Is cell coordinates out of edge(Above width - height)?

	Parameters
	----------
	x: The coordinate number(x or y)
	edge: Edge(for x or y)

	"""
	statement = isBelowZero(x) #if x< 0 out of edge
	result = {
	True: True,  			   #for x<0
	False: (x>=edge)		   #if x>0 then
	}
	return result.get(statement)

def edgeControl(x,edge):
#	Main edge control function
	statement = outOfEdgeControl(x,edge) 
	result = {
	True: edgeError,
	}
#	import ipdb
#	ipdb.set_trace()
	return result.get(statement) #if out of range return edgeError
								 #else do nothing

def isLiveAndDies(cell,n_live_neighbors):
	#subfunction of isLiveAndDies2
	#1 means LIVE, 0 means DEAD
	""" Parameters
	----------
	cell: Our cell status (LIVE:1 or DEAD:0)
	n_live_neighbor: Living neighbor of given cell
	"""

	result = {
	1: (n_live_neighbors<=1 or n_live_neighbors>3) , #if its a living cell do
	0: 5    #if our cell is a DEAD cell value = 5
	}
	return result.get(cell)

def isLiveAndDies2(cell,n_live_neighbors):
#	sub function of isDeadAndLives
#	1 means LIVE, 0 means DEAD
	""" Parameters
	----------
	cell: Our cell status (LIVE:1 or DEAD:0)
	n_live_neighbor: Living neighbor of given cell
	"""
	statement = isLiveAndDies(cell,n_live_neighbors)
	result = {
	True: 0,		#if our cell is LIVE and dies bec of population
	False: 1,		#if our cell is LIVE and stays alive
	5: 5			#if our cell is DEAD value = 5 remains
	}
	return result.get(statement)

def isDeadAndLives(cell,n_live_neighbors):
	#sub function of calculateDeadOrAlive
	#1 means LIVE, means DEAD
	""" Parameters
	----------
	cell: Our cell status (LIVE:1 or DEAD:0)
	n_live_neighbor: Living neighbor of given cell
	"""
#	import ipdb
#	ipdb.set_trace()
	statement = isLiveAndDies2(cell,n_live_neighbors)
	result = {
	0: 0,	#if our cell is LIVE and dies cause of pop.
	1: 1,	#if our cell is LIVE and survive
	5: n_live_neighbors == 3 #if our cell is DEAD and has it enough neighbor?
	}
	return result.get(statement)

def calculateDeadOrAlive(cell,n_live_neighbors):
	""" Parameters
	----------
	cell: Our cell status (LIVE:1 or DEAD:0)
	n_live_neighbor: Living neighbor of given cell
	"""
#	Main function to calculate if the cell is LIVE or DEAD
	statement = isDeadAndLives(cell,n_live_neighbors)
	result = {
	0: 0,   	#if our cell is LIVE and dies cause of pop.
	1: 1,		#if our cell is LIVE and survive
	True: 1,	#if our cell is DEAD and revive of with enough pop.
	False: 0    #if our cell is DEAD and couldn't come to life bec lack of pop.
	}
	return result.get(statement)

def next_cell_value(cell_coords, state):
    """Get the next value of a single cell in a state.

    Parameters
    ----------
    cell_coords: an (x, y) tuple of the co-ordinates of a cell
    state: the current state of the Game board

    Returns
    -------
    The new state of the given cell - either DEAD or LIVE.
    """
    width = state_width(state)
    height = state_height(state)
    x = cell_coords[0]
    y = cell_coords[1]
    n_live_neighbors = 0

    # Iterate around this cell's neighbors

    for x1 in range((x-1), (x+1)+1):

    	try:							#for edge control
    		raise edgeControl(x1,width) #explained below
    	except edgeError: 				#if out of edge: continue
#   		import ipdb
#    		ipdb.set_trace()
    		continue
    	except TypeError: 				#I know that this line is really bad.
    		pass						#to aviod if i blocked the raise "nothing" error above

    	for y1 in range((y-1), (y+1)+1):

        	try:
        		raise edgeControl(y1,height)
        	except edgeError:
#        		import ipdb
#       		ipdb.set_trace()
        		continue
        	except TypeError:
        		pass

        	a = state[x1][y1]
        	n_live_neighbors += neighborCounter(a)

    own_cell = state[x][y]						
    n_live_neighbors -= neighborCounter(own_cell) #decreased own cell from neighbors
    cell = state[x][y]

    statement = calculateDeadOrAlive(cell,n_live_neighbors)
    return statement
#    import ipdb
#    ipdb.set_trace()

"""    if state[x][y] == LIVE:
        if n_live_neighbors <= 1:
            return DEAD
        elif n_live_neighbors <= 3:
            return LIVE
        else:
            return DEAD
    else:
        if n_live_neighbors == 3:
            return LIVE
        else:
            return DEAD
"""
def next_board_state(init_state):
    """Take a single step in the Game of Life.

    Parameters
    ----------
    init_state: the initial state of the Game board

    Returns
    -------
    The next state of the Game board, after taking one step for every cell in
        the previous state.
    """
    width = state_width(init_state)
    height = state_height(init_state)
    next_state = dead_state(width, height)

    for x in range(0, width):
        for y in range(0, height):
            next_state[x][y] = next_cell_value((x, y), init_state)

    return next_state

def display(state):
    """Displays a state by printing it to the terminal.

    Parameters
    ----------
    state: a Game state

    Returns
    -------
    Nothing - this is purely a display function.
    """
    display_as = {
        DEAD: ' ',
        LIVE: '*'
    }
    lines = []
    for y in range(0, state_height(state)):
        line = ''
        for x in range(0, state_width(state)):
            line += display_as[state[x][y]] * 2
        lines.append(line)
    print ("\n".join(lines))
    

def run_forever(init_state):
    """Runs the Game of Life forever, starting from the given initial state.

    Parameters
    ----------
    init_state: the Game state to start at

    Returns
    -------
    This function never returns - the program must be forcibly exited!
    """
    next_state = init_state
    while True:
        display(next_state)
        next_state = next_board_state(next_state)
        time.sleep(1.00)

if __name__ == "__main__":
    init_state = random_state(50, 25)
    # init_state = load_board_state('./toad.txt')
    run_forever(init_state)