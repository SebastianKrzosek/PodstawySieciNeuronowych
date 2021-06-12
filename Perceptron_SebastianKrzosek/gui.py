import pygame
import numpy as np
from perceptron import *
from dataset import *
import random

pygame.init()

# inicjalizacja okna
screen = pygame.display.set_mode((380,480))
# wysokość i szerokość kafli
width, height = 40, 40
# w - liczba kolumn, h- liczba wierszy
w, h = 5, 5
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
# wpisywanie tekstu w guziki
numsRect = []
for i in range(len(nums)):
    numsRect.append(nums[i].get_rect().move(
        (w)*(width+margin)+5, 5+45*i))

# --TWORZENIE PERCEPTRONOW--
perceptrons = []
input_size = 5
for i in range(10):
    perceptrons.append(Perceptron(input_size*input_size))
training_inputs = [ np.ravel(n) for n in number ]
# trenowanie
for i in range(10):
    labels = np.zeros(10)
    labels[i] = 1
    perceptrons[i].train(training_inputs, labels)

# liczby z dataset
def draw_digit(digit):
    return np.array(number[digit])

# rysuje liczby z guzikow
def draw_nums(position, grid):
    if position['column'] == w:
        if position['row'] < 10:
            return draw_digit(position['row'])
    return grid

#wypisuje w konsoli wynik
def perceptron_result(grid):
    for i in range(len(perceptrons)):
        print('{}: {}'.format(i,perceptrons[i].output(np.ravel(grid))))

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
            perceptron_result(grid)

    # Rysowanie guzikow
    for i in range(len(numsRect)):
        screen.blit(nums[i], numsRect[i])
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
