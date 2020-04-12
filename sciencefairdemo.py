from sudoku import *
from graphics import *
from random import randint

def pprint(sudoku):
    text = ''
    for char in sudoku:
        text += char
        if char != '\n':
            text += ' '
    return text

sudokus = open('./sudokus.txt', 'r+')
ratings = open('./ratings.txt', 'r+')

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

while True:
    try:
        win = GraphWin('Sudoku', 1275, 750)
        instructions = 'Please select a symmetry class.'
        text = Text(Point(140, 30), instructions)
        buttona = Button(Point(20, 60), Point(90, 100), 'None')
        buttonb = Button(Point(100, 60), Point(170, 100), 'Diagonal')
        buttonc = Button(Point(20, 110), Point(90, 150), 'Orthogonal')
        buttond = Button(Point(100, 110), Point(170, 150), 'Both')
        button2 = Button(Point(180, 110), Point(260, 150), 'Solve puzzle')
        sudoku_disp = Text(Point(100, 230), '')
        sudoku_disp.setFace('courier')
        answer_disp = Text(Point(250, 230), '')
        answer_disp.setFace('courier')
        nums = Text(Point(400, 230), '')
        for widget in text, buttona, buttonb, buttonc, buttond, button2, sudoku_disp, answer_disp, nums:
            widget.draw(win)
        while True:
            click = win.getMouse()
            if buttona.clicked(click) or buttonb.clicked(click) or buttonc.clicked(click) or buttond.clicked(click):
                try:
                    if buttona.clicked(click): num = 0
                    if buttonb.clicked(click): num = 1
                    if buttonc.clicked(click): num = 2
                    if buttond.clicked(click): num = 3
                    sudoku = sudokulist[120 * num + randint(0, 119)]
                    sudoku_disp.setText(pprint(sudoku))
                    answer_disp.setText('')
                    nums.setText('')
                except ValueError:
                    pass
            if button2.clicked(click) and sudoku_disp.getText():
                text.setText('The puzzle is solving.\nThis may take a while. Please wait.')
                solved, t, count = solve(sudoku, mkexpr())
                answer_disp.setText(pprint(solved))
                nums.setText('Time: ' + str(int(t * 1000) / 1000) + ' s\nCalls to satr: ' + str(count[0]) + '\nCalls to simplify: ' + str(count[1]) + '\nCalls to deduce: ' + str(count[2]))
                text.setText(instructions)
    except GraphicsError:
        win.close()

