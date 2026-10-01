from itertools import pairwise, product

from toolkit.errors import CalcError


class Calc:
    """This class contains all the functions required for the calculator."""
    def __init__(self):
        """
        expression - list of tokens
        answer - value of expression
        """
        self.expression = []
        self.orig_expression = []
        self.answer = 0

    def tokenization(self, input1):
        """
        This function splits the expression into a list of tokens.
        :param input1: the expression passed through parser in __main__
        """
        if not input1 or not input1.strip():
            raise CalcError('Empty sequence.')
        self.orig_expression = input1
        symbols = [x for x in input1 if x != ' ']
        possible_symbols = [['0123456789.', 'number'], ['+-', 'operator1'], ['*/%', 'operator2']]
        tokens = []
        mode = ''
        for n, sym in enumerate(symbols):
            found = False
            for sublist in possible_symbols:
                if sym in sublist[0]:
                    found = True
                    s = '0123456789.'
                    if 0 < n < len(symbols)-1 and sym in '+-' and symbols[n-1] not in s and symbols[n+1] in s:
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
                raise CalcError('Unknown symbol.')
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
            if len(tokens0)-1 > n > 0 and t == ' ' and tokens0[n-1] in digits and tokens0[n+1] in digits:
                raise CalcError('Invalid space.')
        if any(x for x in '+-*/.' if x in tokens0) and not any(x for x in '0123456789' if x in tokens0):
            raise CalcError('Invalid sequence.')

        invalid_sequences = [''.join(x) for x in product('*/.', repeat=2)] + ['+*', '-*', '+/', '-/', '///', '***']
        invalid_sequences.remove('//')
        invalid_sequences.remove('**')

        def token_validation(token, nxt=None):
            """
            This function checks if the token is valid.
            :param token: the token.
            :param nxt: the next token in the list.
            """
            if token.count('.') > 1:
                raise CalcError('Invalid float number format.')
            if (token == '/' or token == "//" or token == "%") and nxt not in '+-*/.' and float(nxt) == 0:
                raise CalcError('Division by zero / modulo zero.')
            if nxt and any(x for x in invalid_sequences if x in token+nxt):
                raise CalcError('Invalid sequence.')

        for token1, nxt1 in pairwise(tokens):
            token_validation(token1, nxt1)

        token_validation(tokens[-1])
        if tokens[-1] in '+-*/':
            raise CalcError('Invalid terminating symbol.')

        if '+' in tokens[0] or '-' in tokens[0]:
            if '+' not in tokens[0]:
                if len(tokens[0]) % 2 == 0:
                    tokens.pop(0)
                else:
                    tokens.pop(0)
                    if float(tokens[0]) < 0:
                        tokens[0] = tokens[0][1:]
                    else:
                        tokens[0] = '-' + tokens[0]
            else:
                tokens.pop(0)
        elif tokens[0] in '*/':
            raise CalcError('Invalid starting symbol.')

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
            try:
                a = float(expr[n - 1])
                b = float(expr[n + 1])
            except (ValueError, TypeError, IndexError):
                raise CalcError('Invalid sequence.')
            else:
                expr[n - 1] = expr[n + 1] = 'Z'

                if set(operator) <= {'+', '-'}:
                    operator = '-' if operator.count('-') % 2 else '+'

                if operator == '+':
                    expr[n] = a + b
                if operator == '-':
                    expr[n] = a - b
                if operator == '*':
                    expr[n] = a * b
                if operator == '**':
                    expr[n] = a ** b
                if operator == '/':
                    expr[n] = a / b
                if operator == '//':
                    expr[n] = a // b
                if operator == '%':
                    expr[n] = a % b
                expr[n] = round(expr[n], 10)
                expr = [x for x in expr if x != 'Z']
                n -= 2
                return n, expr

        k = 0
        while k < len(exp) - 1:
            if k >= len(exp) - 1:
                break
            elem = exp[k]
            if elem in ['*', '/', '//', '%', '**']:
                k, exp = operation(exp, k, elem)
            k += 1
        k = 0
        while k < len(exp) - 1:
            elem = exp[k]
            if ('+' in elem or '-' in elem) and not any(x for x in elem if x in '0123456789.'):
                k, exp = operation(exp, k, elem)
            k += 1

        try:
            c = float(exp[0])
        except (ValueError, IndexError):
            raise CalcError('Invalid sequence.')
        else:
            if int(c) == c:
                self.answer = int(c)
            else:
                self.answer = c
            return self.answer
