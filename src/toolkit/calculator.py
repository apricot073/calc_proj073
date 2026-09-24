from errors import CalcError
from itertools import product


class Calc():
    """This class contains all the functions required for the calculator."""
    def __init__(self):
        """
        expression - list of tokens
        answer - value of expression
        """
        self.expression = []
        self.orig_expression = []
        self.answer = 0

    def tokenization(self, input1=None):
        """
        This function splits the expression into a list of tokens.
        :param input1: the expression passed through parser in __main__
        """
        if not input1 or set(input1) == {' '}:
            CalcError('Empty sequence.')
        self.orig_expression = input1
        symbols = [x for x in list(input1) if x != ' ']
        digits = ['0123456789.', 'number']
        operators1 = ['+-', 'operator1']
        operators2 = ['*/', 'operator2']
        possible_symbols = [digits, operators1, operators2]
        tokens = []
        mode = ''
        for n, sym in enumerate(symbols):
            found = False
            for sublist in possible_symbols:
                if sym in sublist[0]:
                    found = True
                    if 0 < n < len(symbols)-1 and sym in '+-' and symbols[n-1] not in '0123456789.' and symbols[n+1] in '0123456789.':
                        mode = 'number'
                        tokens.append(sym)
                    else:
                        if mode == sublist[1]:
                            tokens[-1] += sym
                        else:
                            mode = sublist[1]
                            tokens.append(sym)
                    break
            if not found:
                CalcError('Unknown symbol.')
        self.expression = tokens

    def validation(self):
        """
        This function checks the tokens for validity in accordance with the rules.
        """
        tokens = self.expression
        tokens0 = self.orig_expression

        while '  ' in tokens0:
            tokens0 = tokens0.replace('  ', ' ')
        digits = '0123456789.'
        for n, t in enumerate(tokens0):
            if t == ' ' and tokens0[n-1] in digits and tokens0[n+1] in digits:
                CalcError('Invalid space.')

        invalid_sequences = [''.join(x) for x in product('*/.', repeat=2)] + ['+*', '-*', '+/', '-/']

        def token_validation(token, nxt=None):
            if token.count('.') > 1:
                CalcError('Invalid float number format.')
            if token == '/' and nxt and float(nxt) == 0:
                CalcError('Division by zero.')
            if nxt and any(x for x in invalid_sequences if x in token+nxt):
                CalcError('Invalid sequence.')

        for token1, nxt1 in zip(tokens, tokens[1:]):
            token_validation(token1, nxt1)

        token_validation(tokens[-1])
        if tokens[-1] in '+-*/':
            CalcError('Invalid terminating symbol.')

        if tokens[0] in '+-':
            tokens[0] += tokens[1]
            tokens.pop(1)
        elif tokens[0] in '*/':
            CalcError('Invalid starting symbol.')

    def calculation(self):
        """
        This function calculates the value of the expression in accordance with the rules.
        :return: the aforementioned value.
        """
        exp = self.expression

        def operation(expr, n, operator):
            """
            This function performs an operation on two number tokens, with an operator token at index n between them.
            :param expr: the full list of tokens at the time of the function call.
            :param n: the number of operator token in the list.
            :param operator: the operator token itself.
            :return: index at which is the obtained value and the modified expression.
            """
            a = float(expr[n - 1])
            b = float(expr[n + 1])
            expr[n - 1] = expr[n + 1] = 'Z'

            if set(operator) == {'+'}:
                operator = '+'
            if set(operator) == {'-'}:
                if len(operator) % 2 == 0:
                    operator = '+'
                else:
                    operator = '-'

            if operator == '+':
                expr[n] = a+b
            if operator == '-':
                expr[n] = a-b
            if operator == '*':
                expr[n] = a*b
            if operator == '/':
                expr[n] = a/b
            expr[n] = round(expr[n], 4) # пока что не считать за ошибку
            expr = [x for x in expr if x != 'Z']
            n -= 2
            return n, expr

        k = 0
        while k < len(exp) - 1:
            if k >= len(exp) - 1:
                break
            elem = exp[k]
            if elem in ['*', '/']:
                k, exp = operation(exp, k, elem)
            k += 1
        k = 0
        while k < len(exp) - 1:
            elem = exp[k]
            if ('+' in elem or '-' in elem) and not any(x for x in elem if x in '0123456789.'):
                k, exp = operation(exp, k, elem)
            k += 1
        c = float(exp[0])
        if int(c) == c:
            self.answer = int(c)
        else:
            self.answer = c

        return self.answer


tests = [' ']
test_calc = Calc()
for test in tests:
    test_calc.tokenization(test)
    test_calc.validation()
    test_calc.calculation()
