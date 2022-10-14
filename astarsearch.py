from re import A
from tkinter import *


class Tile:
    def __init__(self,cost = 1,pos = None,parent = None):
        self.pos =pos
        self.cost = cost
        self.parent = parent
        self.start = False
        self.end = False
        self.display = None
        self.canvas = None


    def __eq__(self,other):
        return self.pos == other.pos

    def flip_cost(self): #flips cost between 1 and 10. ie: wall or no wall
        if self.cost == 10:
            self.canvas.itemconfig(self.display, fill='gray')
            self.cost = 1
        elif self.cost == 1:    
            self.canvas.itemconfig(self.display, fill='blue')
            self.cost = 10

    def change_display_color(self,color):
        if self.canvas is None: return
        self.canvas.itemconfig(self.display, fill=color)
        self.canvas.update()


"""
Start node => .pos == 1
Goal node => .pos == 2
cost to travel to node => .cost
"""


def create_grid(height,width,c):
    tile_list = []
    for i in range(width):
        tile_list.append([])
        for j in range(height):
            temp_tile = Tile()
            temp_tile.canvas = c
            tile_list[i].append(temp_tile)
    return tile_list


def print_grid(grid):
    for i in range(len(grid)):
        s = ""
        for j in range(len(grid[i])):
            if grid[i][j].start:
                s += "S"
            elif grid[i][j].end:
                s += "E"
            else:
                s += str(grid[i][j].cost)
            s += " "
        print(s)

def return_path(current_node,grid):
    path = []
    result = [[-1 for i in range(len(grid[0]))] for j in range(len(grid))]
    current = current_node
    while current is not None:
        if not grid[current.pos[0]][current.pos[1]].start and not grid[current.pos[0]][current.pos[1]].end:
            grid[current.pos[0]][current.pos[1]].change_display_color('black')
        path.append(current.pos)
        current = current.parent
    path = path[::-1]
    start_value = 0

    for i in range(len(path)):
        result[path[i][0]][path[i][1]] = start_value
        start_value +=1
    return result

def search(grid,cost,start,end,c):
    start_node = Tile(1,tuple(start))
    start_node.canvas = c
    start_node.g = start_node.h = start_node.f = 0
    end_node = Tile(1,tuple(end))
    end_node.canvas = c
    end_node.g = end_node.h = end_node.f = 0

    yet_to_visit_list = []

    visited_list = []

    yet_to_visit_list.append(start_node)

    outer_iterations = 0
    max_iterations = (len(grid)/2) ** 10

    move = [[-1,0], #up [0]
            [0,-1], #left [1]
            [1, 0], #down [2]
            [0, 1]] #right [3]

    while len(yet_to_visit_list) > 0:
        outer_iterations += 1
        current_node = yet_to_visit_list[0]
        current_index = 0
        for index,item in enumerate(yet_to_visit_list):
            if item.f < current_node.f:
                current_node = item
                current_index = index

        
        if outer_iterations > max_iterations:
            print("reached maxed iterations, returning")
            return return_path(current_node,grid)

        yet_to_visit_list.pop(current_index)
        visited_list.append(current_node)

        if current_node == end_node:
            print(f"current iteration: {outer_iterations} / {max_iterations}")
            return return_path(current_node, grid)

        children = []

        for new_position in move:
            node_position = (current_node.pos[0] + new_position[0], current_node.pos[1] + new_position[1])

            if  (node_position[0] > len(grid)-1 or
                 node_position[0] < 0 or
                 node_position[1] > len(grid[0])-1 or
                 node_position[1] < 0):
                 continue
            if grid[node_position[0]][node_position[1]].cost != 1:
                continue
            new_node = Tile(1,node_position, current_node)
            new_node.canvas = c
            children.append(new_node)

        for child in children:
            if len([visited_child for visited_child in visited_list if visited_child == child]) > 0:
                continue
            child.g = current_node.g + cost
            child.h = ((child.pos[0] - end_node.pos[0] **2) +
                        child.pos[1] - end_node.pos[1] **2)
            child.f = child.g + child.h

            if len([i for i in yet_to_visit_list if child == i and child.g > i.g]) > 0:
                continue
            yet_to_visit_list.append(child)
        

def set_start(grid,start,canvas):
    grid[start[0]][start[1]].start = True
    canvas.itemconfig(grid[start[0]][start[1]].display, fill='green')

def set_end(grid,end,canvas):
    grid[end[0]][end[1]].end = True
    canvas.itemconfig(grid[end[0]][end[1]].display, fill='red')

def reset(grid,start,end,canvas):
    for i,val in enumerate(grid):
        for j,v in enumerate(grid[i]):
            canvas.itemconfig(grid[i][j].display, fill='gray')
            grid[i][j].cost = 1
    set_start(grid,start,canvas) 
    set_end(grid,end,canvas)
    

def start_search(cost,start,end,c):
    path = search(grid,cost,start,end,c)
    if path is None: 
        print("invalid search, start or end node is on a wall")
    else:
        print("search completed")
    

def tile_click(event):
    x = event.x
    y = event.y
    tile = grid[y//square_width][x//square_width]
    tile.flip_cost()
    return tile

def main():
    grid_width = 10
    grid_height = 10

    global grid
    global square_width
    
    #Squares are nxn pixels
    square_width = 20
    root = Tk()
    canvas = Canvas(root, width=grid_width*square_width, height = grid_height*square_width)
    
    grid = create_grid(grid_width,grid_height,canvas)
    start = [2,2]
    end = [grid_height-3,grid_width-3]
    cost = 10
    
    #set up grid in canvas
    for x in range(0,grid_width*square_width,square_width):
        for y in range(0,grid_height*square_width,square_width):
            a = canvas.create_rectangle(x,y,x+square_width,y+square_width, fill ='gray')
            grid[y//square_width][x//square_width].display = a

    canvas.bind('<Button-1>',tile_click)
    canvas.pack()

    set_start(grid,start,canvas)
    set_end(grid,end,canvas)

    reset_button = Button(root,text="Reset", command=lambda: reset(grid,start,end,canvas))
    reset_button.pack()

    search_button = Button(root,text="Start Search", command=lambda: start_search(cost,start,end,canvas))
    search_button.pack()

    root.mainloop()


if __name__ == "__main__":
    main()