from sudoku import *

sudokus = open('./sudokus.txt', 'r+')
ratings = open('./ratings.txt', 'r+')
times = open('./times.txt', 'w+')
countsatr = open('./countsatr.txt', 'w+')
countsimplify = open('./countsimplify.txt', 'w+')
countdeduce = open('./countdeduce.txt', 'w+')

sudokulist = sudokus.read().replace('\n\n', '\n').split('\n')
ratinglist = ratings.read().replace('\n\n', '\n').split('\n')

sudokus.close()
ratings.close()

sudokulist = sudokulist[:-1]

for i in range(len(sudokulist)):
    sudoku = list(sudokulist[i])
    for j in tuple(range(81, 0, -9)):
        sudoku.insert(j, '\n')
    sudokulist[i] = ''.join(sudoku)[:-1]

expr = mkexpr()

for i in range(len(sudokulist)):
    solved, t, count = solve(sudokulist[i], expr)
    times.write(str(t) + '\n')
    countsatr.write(str(count[0]) + '\n')
    countsimplify.write(str(count[1]) + '\n')
    countdeduce.write(str(count[2]) + '\n')
    print((i+1, 'puzzles solved.'))

times.close()
countsatr.close()
countsimplify.close()
countdeduce.close()
