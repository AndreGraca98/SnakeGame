import  os, time, cv2
from typing import Tuple
import numpy as np
import threading

class Grid:
    def __init__(self, grid_shape=(32,32), square_size=10):
        assert grid_shape[0] == grid_shape[1] and square_size >= 10

        self.sq_size = square_size
        self.grid_shape = grid_shape

        self.reset()

    def reset(self):
        self.grid = np.zeros(self.grid_shape)
        self.resized_grid = cv2.resize(self.grid, tuple(s*self.sq_size for s in self.grid.shape))
        
    def set_on_grid(self, points):
        if isinstance(points[0], list):
            for point in points:
                self.grid[point[0]][point[1]]=1 
        else:
            self.grid[points[0]][points[1]]=1 
        
        self.resized_grid = cv2.resize(self.grid, tuple(s*self.sq_size for s in self.grid.shape), interpolation=cv2.INTER_NEAREST)

    def set_off(self):
        self.reset()

    def draw_lines(self):
        lines_color = (255,255,255)  # (0,0,0)

        for r in range(-1, self.grid_shape[0]):
            row = r*self.sq_size-1
            cv2.line(self.resized_grid, (row, 0), (row, self.resized_grid.shape[0]), lines_color, 1, 1)
        
        for c in range(-1, self.grid_shape[1]):
            column = c*self.sq_size-1
            cv2.line(self.resized_grid, (0, column), (self.resized_grid.shape[1], column), lines_color, 1, 1)

    def show(self):
        self.draw_lines()
        cv2.imshow('Grid', self.resized_grid)
        self.set_off()
    

def nothing():
    pass

class Snake:
    def __init__(self, grid_shape: Tuple):
        self.grid_shape = grid_shape
        r = np.random.randint(0, grid_shape[0])
        c = np.random.randint(0, grid_shape[1])

        self.points = [[r,c]]
        self.length = len(self.points)
        self.snake_speed=100
        
        self.current_direction = nothing
        self.moves = {
                65361:self.move_left,
                65363:self.move_right,
                65362:self.move_up,
                65364:self.move_down,
                }

    def eat(self):
        self.points = self.points + [self.points[-1]] 

    def move(self):
        next_pnt = self.get_next_point()

        if isinstance(next_pnt, list):
            if next_pnt[0] < 0 or next_pnt[1] < 0 or \
                next_pnt[0] > self.grid_shape[0]-1 or next_pnt[1] > self.grid_shape[1]-1:
                return

            self.points = [next_pnt] + self.points[:-1] if len(self.points) > 1 else [next_pnt] 

        elif next_pnt:
            return True
        
    def move_left(self):
        return [self.points[0][0], self.points[0][1] - 1]

    def move_right(self):
        return [self.points[0][0], self.points[0][1] + 1]
        
    def move_up(self):
        return [self.points[0][0] - 1, self.points[0][1]]
        
    def move_down(self):
        return [self.points[0][0] + 1, self.points[0][1]]

    def get_next_point(self):
        """ speed -> wait time in miliseconds """
        p = cv2.waitKeyEx(self.snake_speed)

        if p in [ord('q'), 27]:
            return True
        elif p in self.moves.keys():
            self.current_direction = self.moves.get(p)
            return self.moves.get(p)()

        elif p == ord('e'):
            self.eat()

        else:
            return self.current_direction()


class Food:
    def __init__(self, grid_shape: Tuple):
        self.grid_shape = grid_shape
        
        self.add_new_point()
        
    def add_new_point(self):
        r = np.random.randint(0, self.grid_shape[0])
        c = np.random.randint(0, self.grid_shape[1])

        self.point = [r,c]

    

def main():
    g = Grid(grid_shape=(20,20), square_size=32)
    s = Snake(grid_shape=g.grid_shape)
    f = Food(grid_shape=g.grid_shape)

    flag = True    

    while 1:
        exit_key = s.move()
        if exit_key:
            break
        
        if s.points[0] == f.point and flag:
            s.eat()
            f.add_new_point()
            flag = False
        elif s.points[0] != f.point and not flag:
            flag = True


        g.set_on_grid(s.points)
        g.set_on_grid(f.point)
        g.show()



if __name__ == '__main__':
    main()






    # while(1):
    #     cv2.imshow('',np.zeros(2))
    #     k = cv2.waitKeyEx(0)
    #     if k==27:    # Esc key to stop
    #         break
    #     elif k==-1:  # normally -1 returned,so don't print it
    #         continue
    #     else: 
    #         print(k) # else print its value

