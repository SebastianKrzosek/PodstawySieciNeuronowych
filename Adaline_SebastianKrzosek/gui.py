import pygame
import numpy as np
from dataset import *
from adaline import *
import random

pygame.init()

# inicjalizacja okna
screen = pygame.display.set_mode((580,480))
# wysokość i szerokość kafli
width, height = 40, 40
# w - liczba kolumn, h- liczba wierszy
w, h = 7, 7
margin = 5
# kolory 
red = (255, 0, 0)
white = (255, 255, 255)
grid = np.zeros((h, w))
# font
font = pygame.font.Font('freesansbold.ttf', 39)
# znaczki liczb
nums = [font.render('0', True, red,  white),
          font.render('1', True, red,  white),
          font.render('2', True, red,  white),
          font.render('3', True, red,  white),
          font.render('4', True, red,  white),
          font.render('5', True, red,  white),
          font.render('6', True, red,  white),
          font.render('7', True, red,  white),
          font.render('8', True, red,  white),
          font.render('9', True, red,  white)]

text = [font.render('<', True, red,  white),
        font.render('^', True, red,  white),
        font.render('>', True, red,  white),
        font.render('v', True, red,  white)]          
# wpisywanie tekstu w guziki
numsRect = []
textRect = []
for i in range(len(text)):
    textRect.append(text[i].get_rect().move((w+1)*(width+margin)+5, 5+45*i))
for i in range(len(nums)):
    numsRect.append(nums[i].get_rect().move(
        (w)*(width+margin)+5, 5+45*i))

#TWORZENIE PERCEPTRONOW ADALINE
adalines = []
input_size = 7
for i in range(10):
    adalines.append(Adaline(input_size*input_size))
training_inputs = [ np.ravel(n) for n in number ] # training_data_x 
# trenowanie
for i in range(10):
    labels = np.zeros(10) # training_data_y
    labels[i] = 1 
    adalines[i].train(training_inputs, labels)

# gora
def move_up(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[(row+1) % 7, column]
    return new_grid

# dol
def move_down(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[(row-1) % 7, column]
    return new_grid

# prawo
def move_right(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[row, (column-1) % 7]
    return new_grid

# lewo
def move_left(grid, new_grid):
    for row in range(h):
        for column in range(w):
            new_grid[row, column] = grid[row, (column+1) % 7]
    return new_grid

# liczby z dataset
def draw_digit(digit):
    return np.array(number[digit])

# Opcje ruchy + rysowanie
def draw_nums(position, grid):
    new_grid = grid.copy()
    if position["row"] == 0 and position["column"] == h+1:
        return move_left(grid, new_grid)
    elif position['row'] == 1 and position["column"] == h+1:
        return move_up(grid, new_grid)
    elif position['row'] == 2 and position["column"] == h+1:
        return move_right(grid, new_grid)
    elif position['row'] == 3 and position["column"] == h+1:
        return move_down(grid, new_grid)
    if position['column'] == w:
        if position['row'] < 10:
            return draw_digit(position['row'])
    return grid

#wypisuje w konsoli wynik
def adaline_result(grid):
    maxi = -10 # mala wartosc poczatkowa
    index = 0
    for i in range(len(adalines)): # szukanie maksimum z wynikow
        res =adalines[i].predict(np.ravel(grid))
        if res > maxi:
            maxi = res
            index = i
    print(index)

# main 
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            column = pos[0] // (width + margin) 
            row = pos[1] // (height + margin)
            # malowanie kafelkow 
            try:
                if grid[row, column] == 0:
                   grid[row, column] = 1
                else:
                    grid[row, column] = 0
            except:
                grid = draw_nums({'row': row, 'column': column}, grid.copy())
            # wynik
            print('---RESULT---')
            adaline_result(grid)

    # Rysowanie guzikow
    for i in range(len(numsRect)):
        screen.blit(nums[i], numsRect[i])
    for i in range(len(textRect)):
        screen.blit(text[i], textRect[i])
    # Rysowanie planszy 
    for row in range(h):
        for column in range(w):
            color = white
            if grid[row, column] == 1:
                color = red
            pygame.draw.rect(screen, color,
                             [(margin + width) * column + margin,
                              (margin + height) * row + margin,
                              width,
                              height])
    pygame.display.flip()
pygame.quit()
