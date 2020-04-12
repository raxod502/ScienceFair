class Expr():
    def __init__(self, oper, args=[]):
        self.oper = oper
        self.args = args
    def __str__(self):
        result = '(' + str(self.oper)
        if self.args:
            result += ', ['
            for arg in self.args:
                result += str(arg) + ', '
            result = result[:-2] + ']'
        result += ')'
        return result
    def __eq__(self, other):
        if type(self) == type(other):
            if self.oper == other.oper and self.args == other.args:
                return True
        return False
    def __ne__(self, other):
        return not self == other
    def __hash__(self):
        if self.oper in ['and', 'or', 'not']:
            num = {'and':2,'or':3,'not':5}[self.oper]
        if var(self.oper):
            num = self.oper
        for arg in self.args:
            num *= 7
            num += hash(arg)
        return num
    def simplify(self, vardict):
        count = 1
        if self.oper in ['false', 'true']:
            return self.oper, count
        if self.oper in vardict:
            return vardict[self.oper], count
        if var(self.oper):
            return self, count
        a = []
        for arg in self.args:
            result = arg.simplify(vardict)
            a.append(result[0])
            count += result[1]
        if self.oper == 'not':
            if a[0] == 'false':
                return 'true', count
            if a[0] == 'true':
                return 'false', count
            else:
                return Expr('not', [a[0]]), count
        if self.oper == 'or':
            if 'true' in a:
                return 'true', count
            false = True
            b = []
            for arg in a:
                if arg != 'false':
                    false = False
                    b.append(arg)
            if false:
                return 'false', count
            if len(b) == 1:
                return b[0], count
            return Expr('or', b), count
        if self.oper == 'and':
            if 'false' in a:
                return 'false', count
            true = True
            b = []
            for arg in a:
                if arg != 'true':
                    true = False
                    b.append(arg)
            if true:
                return 'true', count
            if len(b) == 1:
                return b[0], count
            return Expr('and', b), count
    def deduce(self):
        count = 1
        if self.oper in ['false', 'true']:
            return set({}), set({}), count
        if var(self.oper):
            return set({self.oper}), set({}), count
        if self.oper == 'not' and var(self.args[0].oper):
            return set({}), set({self.args[0].oper}), count
        else:
            changeslistpos = []
            changeslistneg = []
            cd = False
            for i in range(len(self.args)):
                result = self.args[i].deduce()
                count += result[2]
                if self.args[i] == Expr('false'):
                    return set({}), set({}), count
                changeslistpos.append(result[0])
                changeslistneg.append(result[1])
            changespos = changeslistpos[0]
            changesneg = changeslistneg[0]
            if self.oper == 'and':
                for i in range(1, len(self.args)):
                    changespos = changespos.union(changeslistpos[i])
                    changesneg = changesneg.union(changeslistneg[i])
                false = False
                for arg in self.args:
                    if arg.oper == 'false':
                        false = True
                        break
                if false:
                    cd = True
            if self.oper == 'or':
                for i in range(1, len(self.args)):
                    if self.args[i] != 'false':
                        changespos = changespos.intersection(changeslistpos[i])
                        changesneg = changesneg.intersection(changeslistneg[i])
            if contradiction(changespos, changesneg) or cd:
                self = Expr('false')
                return set({}), set({}), count
            return changespos, changesneg, count
    def reduce(self, negate=False):
        if negate:
            if self.oper == 'and':
                self.oper = 'or'
                for i in range(len(self.args)):
                    self.args[i] = self.args[i].negate()
            elif self.oper == 'or':
                self.oper = 'and'
                for i in range(len(self.args)):
                    self.args[i] = self.args[i].negate()
            elif self.oper == 'not':
                self = self.args[0].reduce()
            elif var(self.oper):
                self = Expr('not', [Expr(self.oper)])
            elif self.oper == 'false':
                self.oper = 'true'
            elif self.oper == 'true':
                self.oper = 'false'
            else:
                print((self.oper))
                raise Exception('Unidentified operator')
        else:
            if self.oper == 'not':
                self = self.args[0].negate()
            elif self.oper in ['and', 'or']:
                for i in range(len(self.args)):
                    self.args[i] = self.args[i].reduce()
            elif var(self.oper) or self.oper in ['true', 'false']:
                pass
            else:
                print((self.oper))
                raise Exception('Unidentified operator')
        return self
    def negate(self):
        return self.reduce(negate=True)
    def getvar(self):
        if var(self.oper):
            return self.oper
        for arg in self.args:
            result = arg.getvar()
            if var(result):
                return result
        return None

def display(self):
    if type(self) == str:
        return self
    else:
        return self.display()

def var(self):
    return type(self) == int

def contradiction(changespos, changesneg):
    for change in changespos:
        if change in changesneg:
            return True
    return False

def adeduce(exp, vardict):
    count1, count2 = 0, 0
    while True:
        result = exp.simplify(vardict)
        exp = result[0]
        count1 += result[1]
        if type(exp) == str:
            break
        result = exp.deduce()
        changespos, changesneg = result[0], result[1]
        count2 += result[2]
        if not changespos and not changesneg:
            break
        for change in changespos:
            vardict[change] = 'true'
        for change in changesneg:
            vardict[change] = 'false'
        if type(exp) == str:
            exp = Expr(exp)
    return exp, count1, count2

def satr(exp, vardict):
    count = [1, 0, 0]
    vardict = dict(vardict)
    exp, count[1], count[2] = adeduce(exp, vardict)
    if exp == 'false' or exp == 'true':
        return [exp, vardict, count]
    var = exp.getvar()
    vardict[var] = 'true'
    result = satr(exp, vardict)
    count[0] += result[2][0]
    if result[0] == 'true':
        result[2] = count
        return result
    vardict[var] = 'false'
    result = satr(exp, vardict)
    result[2][0] += count[0]
    return result

def sat(expr, vardict={}):
    expr = expr.reduce()
    expr, count1 = expr.simplify(vardict)
    if type(expr) == str:
        return expr, {}
    result = satr(expr, vardict)
    result[2][1] += count1
    return result

if __name__ == '__main__':
    print((sat(Expr('and', [Expr(1), Expr(2), Expr(3)]))))
