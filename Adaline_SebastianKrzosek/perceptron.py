import numpy as np
import random


class Perceptron(object):

    def __init__(self, no_of_inputs, learning_rate=0.1, iterations=1000):
        self.iterations = iterations
        self.no_of_inputs = no_of_inputs
        self.learning_rate = learning_rate
        self.weights = np.random.rand(self.no_of_inputs+1)

    def train(self, train, labels):
        time = 0 
        best_time = 0 
        val = 0  
        best_val = 0 
        pocket = self.weights
        for _ in range(self.iterations):
            i = random.randrange(len(train))
            prediction = self.output(train[i])

            if labels[i] - prediction == 0:
                time +=1
                for input, label in zip(train, labels): 
                    if label - self.output(input): 
                        val += 1
                    #porownanie wag
                if val > best_val  and  time > best_time:
                    best_val = val
                    best_time = time
                    pocket = self.weights #zapisywanie najlepszej wagi
            else:
                #aktualizacja wag
                self.weights[1:] += self.learning_rate * (labels[i] - prediction) * train[i]
                self.weights[0] += self.learning_rate * (labels[i] - prediction)
                val = 0
                time = 0
    

    def output(self, inputs):
        summ = np.dot(inputs, self.weights[1:])+self.weights[0]
        if summ > 0:
            activation = 1
        else:
            activation = 0
        return activation
