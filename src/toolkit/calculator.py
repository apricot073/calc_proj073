from toolkit.errors import calcError

class Calc():
    def __init__(self):
        self.userinput = ""
        self.expression = []
        self.answer = 0

    def tokenization(self, inp):
        se = self.expression
        simvoly = [x for x in list(inp) if x != ' ']
        if simvoly == []:
            raise calcError('Empty sequence.')
        oper = '+-*/'
        if simvoly[0] in '0123456789' and any(x for x in oper if x in simvoly):
            if any(x for x in ['**', '//', '+++', '---'] if x in simvoly):
                raise calcError('Unsupported operator sequence.')
            mode = -1
            # 0 - num, 1 - sym
            cifry = '0123456789'
            for g, sym in enumerate(simvoly):
                if sym in cifry:
                    if mode == 0:
                        se[-1] += sym
                    else:
                        mode = 0
                        se.append(sym)
                else:
                    A = g < len(simvoly) - 1 and simvoly[g + 1] in cifry
                    if (sym == '-' or sym == '+') and A and simvoly[g - 1] not in cifry:
                        mode = 0
                        se.append(sym)
                    elif sym == '.' and A and simvoly[g - 1] in cifry:
                        if not '.' in se[-1]:
                            se[-1] += sym
                        else:
                            raise calcError('Invalid format of a float number')
                    else:
                        mode = 1
                        se.append(sym)
        else:
            self.expression = float(''.join(simvoly))
        if type(self.expression) == list and any(x for x in self.expression if x[-1] == '.'):
            raise calcError('Unsupported terminating symbol')
    def calculation(self):
        se = self.expression
        def Z(se,n,el):
            a = float(se[n - 1])
            b = float(se[n + 1])
            se[n - 1] = se[n + 1] = 'Z'
            if el == '+':
                se[n] = a+b
            if el == '-':
                se[n] = a-b
            if el == '*':
                se[n] = a*b
            if el == '/':
                se[n] = a/b
            se = [x for x in se if x != 'Z']
            n -= 2
            return n,se

        if type(se) == list:
            n = 0
            while n < len(se) - 1:
                if n >= len(se) - 1: break
                elem = se[n]
                if elem in ['*', '/']:
                    n, se = Z(se, n, elem)
                n += 1
            n = 0
            while n < len(se) - 1:
                elem = se[n]
                if elem in ['+', '-']:
                    n, se = Z(se, n, elem)
                n += 1
            c = float(se[0])
            if int(c) == c:
                self.answer = int(c)
            else:
                self.answer = c
        else:
            c = se
            if int(c) == c:
                self.answer = int(c)
            else:
                self.answer = c
        return self.answer