import pygame
import math 
from queue import PriorityQueue

RED = (255,0,0)
GREEN = (0,255,0)
BLUE = (0,0,255)
BLACK = (0,0,0)
WHITE = (255,255,255)
ORANGE = (255,165,0)
TURQUOISE = (64, 224, 208)
PURPLE = (128,0,128)
GREY = (128,128,128)
# RED = (255,0,0)


WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("A star algorithm")

class Node:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col
    
    def is_closed(self):
        return self.color == ORANGE
    
    def is_open(self):
        return self.color == TURQUOISE
    
    def is_barrier(self):
        return self.color == BLACK
    
    def is_start(self):
        return self.color == RED
    
    def is_end(self):
        return self.color == GREEN
    
    def reset(self):
        self.color = WHITE

    def make_closed(self):
        self.color = ORANGE

    def make_open(self):
        self.color = TURQUOISE

    def make_barrier(self):
        self.color = BLACK

    def make_start(self):
        self.color = RED
    
    def make_dest(self):
        self.color = GREEN

    def make_path(self):
        self.color = BLUE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        self.neighbours = []
        if (self.row < self.total_rows-1 and not grid[self.row+1][self.col].is_barrier()):  #UP
            self.neighbours.append(grid[self.row+1][self.col])

        if (self.row > 0 and not grid[self.row-1][self.col].is_barrier()):  #DOWN
            self.neighbours.append(grid[self.row-1][self.col])

        if (self.col < self.total_rows-1 and not grid[self.row][self.col+1].is_barrier()):  #RIGHT
            self.neighbours.append(grid[self.row][self.col+1])

        if (self.col > 0 and not grid[self.row][self.col-1].is_barrier()):  #LEFT
            self.neighbours.append(grid[self.row][self.col-1])



    def lt(self, other):
        return False
    
def manhattan(pt1, pt2):
    x1, y1 = pt1
    x2, y2 = pt2
    return abs(x2-x1) + abs(y2-y1)

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            node = Node(i, j, gap, rows)
            grid[i].append(node)
    return grid 

def gridlines(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0,i*gap), (width, i*gap))
    for i in range(rows):
        pygame.draw.line(win, GREY, (i*gap, 0), (i*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)
    for i in grid:
        for node in i:
            node.draw(win)
    gridlines(win, rows, width)
    pygame.display.update()

def clicked_fn(pos, rows, width):
    gap = width // rows
    x, y = pos
    row = x // gap
    col = y // gap
    return row, col

def reconstruct_path(come_set, cur, draw):
    while cur in come_set:
        cur = come_set[cur]
        cur.make_path()
        draw()

def astar(draw, grid, start, dest):
    cnt = 0
    open_set = PriorityQueue()
    open_set.put((0, cnt, start))
    come_set = {}
    g_score = {node : float("inf") for row in grid for node in row}
    g_score[start] = 0
    f_score = {node : float("inf") for row in grid for node in row}
    f_score[start] = manhattan(start.get_pos(), dest.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        cur = open_set.get()[2]
        open_set_hash.remove(cur)
        if cur == dest:
            reconstruct_path(come_set, dest, draw)
            start.make_start()
            dest.make_dest()
            return True
    
        for neighbour in cur.neighbours:
            temp = g_score[cur] + 1
            if temp < g_score[neighbour]:
                come_set[neighbour] = cur
                g_score[neighbour] = temp
                f_score[neighbour] = temp + manhattan(neighbour.get_pos(), dest.get_pos())
                if neighbour not in open_set_hash:
                    cnt += 1
                    open_set.put((f_score[neighbour], cnt, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        draw()
        if cur != start:
            cur.make_closed()
    return False



    

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, width)
    start = None
    dest = None
    loop = True
    started = False
    while loop:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                loop = False
            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = clicked_fn(pos, ROWS, width)
                node = grid[row][col]
                if not start and node != dest:
                    start = node
                    start.make_start()
                elif not dest and node != start:
                    dest = node
                    dest.make_dest()
                elif node != start and node != dest:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = clicked_fn(pos, ROWS, width)
                node = grid[row][col]
                node.reset()
                if node == start:
                    start = None
                elif node == dest:
                    dest = None
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and dest:
                    for row in grid:
                        for node in row:
                            node.update_neighbours(grid)
                    astar(lambda: draw(win, grid, ROWS, width), grid, start, dest)
                if event.key == pygame.K_c:
                    start = None
                    dest = None
                    grid = make_grid(ROWS, width)
                if event.key == pygame.K_ESCAPE:
                    loop = False

    pygame.quit()
main(WIN, WIDTH)
