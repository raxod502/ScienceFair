from sat import *
from time import *

def mkexpr():
    SIZE = 3
    rows = []
    for r in range(1, SIZE**2+1):
        for n in range(1, SIZE**2+1):
            columns = []
            for c in range(1, SIZE**2+1):
                exprs = [Expr(r*100+c*10+n)]
                for c2 in range(1, c):
                    exprs.append(Expr('not', [Expr(r*100+c2*10+n)]))
                for c2 in range(c+1, SIZE**2+1):
                    exprs.append(Expr('not', [Expr(r*100+c2*10+n)]))
                columns.append(Expr('and', exprs))
            rows.append(Expr('or', columns))
    rexpr = Expr('and', rows)

    columns = []
    for c in range(1, SIZE**2+1):
        for n in range(1, SIZE**2+1):
            rows = []
            for r in range(1, SIZE**2+1):
                exprs = [Expr(r*100+c*10+n)]
                for r2 in range(1, r):
                    exprs.append(Expr('not', [Expr(r2*100+c*10+n)]))
                for r2 in range(r+1, SIZE**2+1):
                    exprs.append(Expr('not', [Expr(r2*100+c*10+n)]))
                rows.append(Expr('and', exprs))
            columns.append(Expr('or', rows))
    cexpr = Expr('and', columns)

    boxes = []
    for br in range(SIZE):
        for bc in range(SIZE):
            for n in range(1, SIZE**2+1):
                cells = []
                for r in range(1, SIZE+1):
                    for c in range(1, SIZE+1):
                        exprs = [Expr((SIZE*br+r)*100+(SIZE*bc+c)*10+n)]
                        for r2 in range(1, SIZE+1):
                            for c2 in range(1, SIZE+1):
                                if r2 < r or c2 < c or r2 > r or c2 > c:
                                    exprs.append(Expr('not', [Expr((SIZE*br+r2)*100+(SIZE*bc+c2)*10+n)]))
                        cells.append(Expr('and', exprs))
                boxes.append(Expr('or', cells))
    bexpr = Expr('and', boxes)

    cells = []
    for r in range(1, SIZE**2+1):
        for c in range(1, SIZE**2+1):
            nums = []
            for n in range(1, SIZE**2+1):
                nums.append(Expr(r*100+c*10+n))
            cells.append(Expr('or', nums))
    nexpr = Expr('and', cells)

    rows = []
    for r in range(1, SIZE**2+1):
        for c in range(1, SIZE**2+1):
            for n1 in range(1, SIZE**2+1):
                for n2 in range(1, SIZE**2+1):
                    if n1 != n2:
                        rows.append(Expr('or', [Expr('not', [Expr(r*100+c*10+n1)]), Expr('not', [Expr(r*100+c*10+n2)])]))
    rexpr2 = Expr('and', rows)

    columns = []
    for c in range(1, SIZE**2+1):
        for r in range(1, SIZE**2+1):
            for n1 in range(1, SIZE**2+1):
                for n2 in range(1, SIZE**2+1):
                    if n1 != n2:
                        columns.append(Expr('or', [Expr('not', [Expr(r*100+c*10+n1)]), Expr('not', [Expr(r*100+c*10+n2)])]))
    cexpr2 = Expr('and', columns)

    boxes = []
    for br in range(SIZE):
        for bc in range(SIZE):
            for r in range(1, SIZE+1):
                for c in range(1, SIZE+1):
                    for n1 in range(1, SIZE**2+1):
                        for n2 in range(1, SIZE**2+1):
                            if n1 != n2:
                                boxes.append(Expr('or', [Expr('not', [Expr(r*100+c*10+n1)]), Expr('not', [Expr(r*100+c*10+n2)])]))
    bexpr2 = Expr('and', boxes)

    cells = []
    for r in range(1, SIZE**2+1):
        for c in range(1, SIZE**2+1):
            nums = []
            for n1 in range(1, SIZE**2+1):
                for n2 in range(1, SIZE**2+1):
                    if n1 != n2:
                        nums.append(Expr('or', [Expr('not', [Expr(r*100+c*10+n1)]), Expr('not', [Expr(r*100+c*10+n2)])]))
            cells.append(Expr('or', nums))
    nexpr2 = Expr('and', cells)

    expr = Expr('and', [rexpr, cexpr, bexpr, nexpr, rexpr2, cexpr2, nexpr2])

    return expr

def clean(sudoku):
    return sudoku.replace(' ', '').replace('_', '.').replace('\n\n', '\n')

def solve(sudoku, expr):
    SIZE = 3
    sudoku = clean(sudoku)
    rows = sudoku.split('\n')
    for i in range(len(rows)):
        rows[i] = list(rows[i])

    vardict = {}

    for i in range(SIZE**2):
        for j in range(SIZE**2):
            if rows[i][j] != '.':
                for n in range(1, SIZE**2+1):
                    vardict[(i+1)*100+(j+1)*10+n] = str(rows[i][j] == str(n)).lower()

    t = time()
    solution, vardict, count = sat(expr, vardict)
    t = time() - t

    solved = [['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0'],
              ['0','0','0','0','0','0','0','0','0']]

    for k in vardict:
        if vardict[k] == 'true':
            solved[int(str(k)[0])-1][int(str(k)[1])-1] = str(k)[2]

    for i in range(len(solved)):
        solved[i] = ''.join(solved[i])
    solved = '\n'.join(solved)

    return solved, t, count

if __name__ == '__main__':
    print('Working...')
    expr = mkexpr()
    sudoku = '''
...1.4...
.4.....7.
...7.5...
9.53.64.7
.........
3.14.26.8
...6.9...
.5.....9.
...2.1...
'''[1:-1]
    res = solve(sudoku, expr)
    print('Found solution:')
    print('---------------')
    print(res[0])
    print('---------------')
    print('Stats for nerds:', res[1:])
