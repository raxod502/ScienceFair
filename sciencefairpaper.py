from sudoku import *
from random import randint

def sym(i):
    if i < 120:
        return 'None\t\t'
    elif i < 240:
        return 'Diagonal\t'
    elif i < 360:
        return 'Orthogonal\t'
    else:
        return 'Both\t\t'

sudokus = open('./sudokus.txt', 'r+')
ratings = open('./ratings.txt', 'r+')
times = open('./times.txt', 'r+')
callsatr = open('./countsatr.txt', 'r+')
callsimplify = open('./countsimplify.txt', 'r+')
calldeduce = open('./countdeduce.txt', 'r+')

sudokulist = sudokus.read().replace('\n\n', '\n').split('\n')
ratinglist = ratings.read().replace('\n\n', '\n').split('\n')
timelist = times.read().replace('\n\n', '\n').split('\n')
satrlist = callsatr.read().replace('\n\n', '\n').split('\n')
simplifylist = callsimplify.read().replace('\n\n', '\n').split('\n')
deducelist = calldeduce.read().replace('\n\n', '\n').split('\n')

sudokus.close()
ratings.close()
times.close()
callsatr.close()
callsimplify.close()
calldeduce.close()

sudokulist = sudokulist[:-1]

for i in range(len(sudokulist)):
    sudoku = list(sudokulist[i])
    for j in tuple(range(81, 0, -9)):
        sudoku.insert(j, '\n')
    sudokulist[i] = ''.join(sudoku)[:-1]

datalist = []

for i in range(480):
    datalist.append(sym(i) + str(ratinglist[i]) + '\t\t' + str(int(float(timelist[i]) * 1000) / 1000) + '\t\t' + str(satrlist[i]) + '\t\t' + str(simplifylist[i]) + '\t\t' + str(deducelist[i]))

print(('\n'.join(datalist)))
