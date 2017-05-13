import sys
import pygame
import math
import heapq
from pygame.locals import *
import threading
import time
import serial


# Adjust the size of the board and the cells
cell_size = 30
num_cells = 20


# Dictionary of Cells where a tuple (immutable set) of (x,y) coordinates
# is used as keys
cells = {}

for x in range(22):
    for y in range(28):
        cells[(x, y)] = {'state': None,   # None, Wall, Goal, Start Are the possible states. None is walkable
                         'f_score': None,  # f() = g() + h() This is used to determine next cell to process
                         # The heuristic score, We use straight-line distance:
                         # sqrt((x1-x0)^2 + (y1-y0)^2)
                         'h_score': None,
                         'g_score': None,  # The cost to arrive to this cell, from the start cell
                         'parent': None}  # In order to walk the found path, keep track of how we arrived to each cell

# Colors
black = (0, 0, 0)             # Wall Cells
gray = (112, 128, 144)      # Default Cells
bright_green = (0, 204, 102)  # Start Cell
red = (255, 44, 0)          # Goal Cell
orange = (255, 175, 0)      # Open Cells
blue = (0, 124, 204)        # Closed Cells
white = (250, 250, 250)       # Not used, yet

# PyGame stuff to set up the window
pygame.init()
size = width, height = (cell_size * num_cells) + 2, (cell_size * num_cells) + 2
screen = pygame.display.set_mode(size)
pygame.display.set_caption = ('Pathfinder')


start_placed = goal_placed = needs_refresh = step_started = False
last_wall = None
start = None
goal = None
open_list = []      # our priority queue of opened cells' f_scores
pq_dict = {}
closed_list = {}    # A dictionary of closed cells
# Could be 'manhattan' or 'crow' anything else is assumed to be 'zero'
heuristic = 'manhattan'



def showBoard(screen, board):
    screen.blit(board, (0, 0))
    pygame.display.flip()


# Function to Draw the initial board.

def initBoard(board):
    background = pygame.Surface(board.get_size())
    background = background.convert()
    background.fill(gray)

    # Draw Grid lines
    # for i in range(0, (cell_size * num_cells) + 1)[::cell_size]:
    #    pygame.draw.line(background, black, (i, 0),
    #                     (i, cell_size * num_cells), 2)
    #   pygame.draw.line(background, black, (0, i),
    #                    (cell_size * num_cells, i), 2)
    return background


# Function in attempt to beautify my code, nothing more.

def calc_f(node):
    cells[node]['f_score'] = cells[node]['h_score'] + cells[node]['g_score']

start = 1, 19
goal = [(7, 14), (15, 5), (3, 3)]
goal_temp = goal[:]


def calc_h(node):
    global heuristic
    x0, y0 = node
    cells[node]['h_score'] = 0
    for x in goal:
        x1, y1 = x[0], x[1]
        cells[node]['h_score'] += (2 * abs(x1 - x0) + abs(y1 - y0)) * 10


def onBoard(node):
    x, y = node
    return x >= 0 and x < num_cells and y >= 0 and y < num_cells


# Return a list of adjacent orthoganal walkable cells

def orthoganals(current):
    x, y = current

    N = x - 1, y
    E = x, y + 1
    S = x + 1, y
    W = x, y - 1

    directions = [N, E, S, W]
    return [x for x in directions if onBoard(x) and cells[x]['state'] != 'Wall' and not x in closed_list]


# Check if diag is blocked by a wall, making it unwalkable from current

def blocked_diagnol(current, diag):
    x, y = current

    N = x - 1, y
    E = x, y + 1
    S = x + 1, y
    W = x, y - 1
    NE = x - 1, y + 1
    SE = x + 1, y + 1
    SW = x + 1, y - 1
    NW = x - 1, y - 1

    if diag == NE:
        return cells[N]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
    elif diag == SE:
        return cells[S]['state'] == 'Wall' or cells[E]['state'] == 'Wall'
    elif diag == SW:
        return cells[S]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
    elif diag == NW:
        return cells[N]['state'] == 'Wall' or cells[W]['state'] == 'Wall'
    else:
        return False  # Technically, you've done goofed if you arrive here.


# Update a child node with information from parent, such as g_score and
# the parent's coords

def update_child(parent, child, cost_to_travel):
    cells[child]['g_score'] = cells[parent]['g_score'] + cost_to_travel
    cells[child]['parent'] = parent


# Display the shortest path found

def unwind_path(coord, slow):
    if cells[coord]['parent'] is not None:
        left, top = coord
        left = (left * cell_size) + 2
        top = (top * cell_size) + 2
        r = pygame.Rect(left, top, cell_size, cell_size)
        pygame.draw.rect(board, white, r, 0)
        if slow:
            showBoard(screen, board)
        unwind_path(cells[coord]['parent'], slow)


path = []


def save_path(coord, slow):
    if cells[coord]['parent'] is not None:
        left, top = coord
        global path

        path.append(coord)
        save_path(cells[coord]['parent'], slow)

# Recursive function to process the current node, which is the node with
# the smallest f_score from the list of open nodes


def move(direction):
    R = 1, 0
    L = -1, 0
    U = 0, -1
    D = 0, 1
    if direction == R:
        return 'right'
    if direction == L:
        return 'left'
    if direction == U:
        return 'up'
    if direction == D:
        return 'down'


PATH = []


def processNode(coord, slow, step):
    global goal, open_list, closed_list, pq_dict, board, screen, needs_refresh
    if coord in goal and len(goal) > 1:
        print 'find one'
        goal.remove(coord)
    elif coord in goal:
        print 'find last'
        goal = coord
        print "Cost %d\n" % cells[goal]['g_score']
        unwind_path(cells[goal]['parent'], slow)
        save_path(cells[goal]['parent'], slow)
        print 'fuck'
        path.reverse()
        # from pprint import pprint
        # pprint(path)
        a, b = start
        global PATH
        for i, j in path:
            direction = i - a, j - b
            PATH.append(move(direction))
            a, b = i, j
            a, b = i, j
            # print direction
        needs_refresh = True
        print PATH

        return

    if coord == goal:
        print "Cost %d\n" % cells[goal]['g_score']
        unwind_path(cells[goal]['parent'], slow)
        needs_refresh = True
        return

    # l will be a list of walkable adjacents that we've found a new shortest
    # path to
    l = []
    for x in orthoganals(coord):
        # If x hasn't been visited before
        if cells[x]['g_score'] is None:
            update_child(coord, x, cost_to_travel=10)
            l.append(x)
        # Else if we've found a faster route to x
        elif cells[x]['g_score'] > cells[coord]['g_score'] + 10:
            update_child(coord, x, cost_to_travel=10)
            l.append(x)

    for x in l:
        # If we found a shorter path to x
        # Then we remove the old f_score from the heap and dictionary
        if cells[x]['f_score'] in pq_dict:
            if len(pq_dict[cells[x]['f_score']]) > 1:
                pq_dict[cells[x]['f_score']].remove(x)
            else:
                pq_dict.pop(cells[x]['f_score'])
            open_list.remove(cells[x]['f_score'])
        # Update x with the new f and h score (technically don't need to do h
        # if already calculated)
        calc_h(x)
        calc_f(x)
        # Add f to heap and dictionary
        open_list.append(cells[x]['f_score'])
        if cells[x]['f_score'] in pq_dict:
            pq_dict[cells[x]['f_score']].append(x)
        else:
            pq_dict[cells[x]['f_score']] = [x]

    heapq.heapify(open_list)

    if not step:
        if len(open_list) == 0:
            print 'NO POSSIBLE PATH!'
            return
        f = heapq.heappop(open_list)
        if len(pq_dict[f]) > 1:
            node = pq_dict[f].pop()

        else:
            node = pq_dict.pop(f)[0]

        heapq.heapify(open_list)
        closed_list[node] = True

        processNode(node, slow, step)


# Start the search for the shortest path from start to goal

def findPath(slow, step):
    if start is not None and goal is not None:
        cells[start]['g_score'] = 0
        calc_h(start)
        calc_f(start)
        closed_list[start] = True
        processNode(start, slow, step)


# Clean up code a little bit: This function draws a cell at (x,y)

def draw_cell(x, y, size, color):
    r = pygame.Rect(x, y, size, size)
    pygame.draw.rect(board, color, r, 0)


def draw_goal():
    global goal_temp
    for x in goal_temp:
        x_index, y_index = x[0], x[1]
        cells[(x_index, y_index)]['state'] = 'Goal'
        left = x_index * cell_size + 2
        top = y_index * cell_size + 2
        r = pygame.Rect(left, top, cell_size, cell_size)
        pygame.draw.rect(board, red, r, 0)



board = initBoard(screen)

findPath(slow=False, step=False)
draw_goal()
# showBoard(screen, board)
screen.blit(board, (0, 0))
pygame.image.save(board, 'test.jpg')

PATH.append('off')
hjr = []
flag = 'off'
n = 0
for x in PATH:
    if x == flag:
        n = n + 1
    else:
        n = n + 1
        hjr.append(str(flag) + ',' + str(n))
        flag = x
        n = 0
from pprint import pprint
hjr.pop(0)
pprint(hjr)
flag = 'right'
shm = {'right': 0, 'up': 90, 'left': 180, 'down': 270}


def run(zhiling):
    ser = serial.Serial(port='/dev/ttyUSB0', baudrate=115200)
    try:
        ser.write(zhiling)
        while True:
            line = ser.readline().strip()
            print line
            if line.find('OK') != -1:
                break
        ser.close()
        time.sleep(0.5)
    except:
        print 'serial is not open'
        # print 'turn right'


for x in hjr:
    direct, n = x.split(',')
    if (shm[direct] - shm[flag]) in [90, -270]:
        # run('left rotating:9000,90\r\n')
        print 'left'
    if (shm[direct] - shm[flag]) in [-90, 270]:
        # run('right rotating:9000,90\r\n')
        print 'right'
    n = int(n) * 10
    # run('move straight:300,' + str(n) + '\r\n')
    # print 'move straight:300,' + str(n) + '\r\n'
    flag = direct
