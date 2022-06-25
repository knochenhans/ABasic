import unittest
from lexer import *
from parser import *
from interpreter import Interpreter


class TestLexer(unittest.TestCase):

    def test1(self):
        lexer = Lexer()

        # print(lexer.lex_file('st1.bas'))

        lines = []
        lines.append('abc test xyz')
        lines.append('another "test test" 456')
        lines.append('123 test')

        tokens = lexer.lex(lines)

        self.assertEqual(tokens[0].value, 'abc')
        self.assertEqual(tokens[0].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[0].line, 0)
        # self.assertEqual(tokens[0].id, 0)
        self.assertEqual(tokens[1].value, 'test')
        self.assertEqual(tokens[1].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[1].line, 0)
        # self.assertEqual(tokens[1].id, 1)
        self.assertEqual(tokens[2].value, 'xyz')
        self.assertEqual(tokens[2].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[2].line, 0)
        # self.assertEqual(tokens[2].id, 2)
        self.assertEqual(tokens[3].value, 'another')
        self.assertEqual(tokens[3].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[3].line, 1)
        # self.assertEqual(tokens[3].id, 3)
        self.assertEqual(tokens[4].value, '"')
        self.assertEqual(tokens[4].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[4].line, 1)
        # self.assertEqual(tokens[4].id, 4)
        self.assertEqual(tokens[5].value, 'test test')
        self.assertEqual(tokens[5].type, TOKEN_TYPE.LITERAL)
        self.assertEqual(tokens[5].line, 1)
        # self.assertEqual(tokens[5].id, 5)
        self.assertEqual(tokens[6].value, '"')
        self.assertEqual(tokens[6].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[6].line, 1)
        # self.assertEqual(tokens[6].id, 6)
        self.assertEqual(tokens[7].value, '456')
        self.assertEqual(tokens[7].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[7].line, 1)
        # self.assertEqual(tokens[7].id, 7)
        self.assertEqual(tokens[8].value, '123')
        self.assertEqual(tokens[8].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[8].line, 2)
        # self.assertEqual(tokens[8].id, 8)
        self.assertEqual(tokens[9].value, 'test')
        self.assertEqual(tokens[9].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[9].line, 2)
        # self.assertEqual(tokens[9].id, 9)

    def test2(self):
        lexer = Lexer()

        lines = []
        lines.append('abc1b')

        tokens = lexer.lex(lines)

        self.assertEqual(tokens[0].value, 'abc1b')
        self.assertEqual(tokens[0].type, TOKEN_TYPE.IDENTIFIER)

    def test3(self):
        lexer = Lexer()

        lines = []
        lines.append('n= 5*3')

        tokens = lexer.lex(lines)

        self.assertEqual(tokens[0].value, 'n')
        self.assertEqual(tokens[0].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[1].value, '=')
        self.assertEqual(tokens[1].type, TOKEN_TYPE.OPERATOR)
        self.assertEqual(tokens[2].value, '5')
        self.assertEqual(tokens[2].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[3].value, '*')
        self.assertEqual(tokens[3].type, TOKEN_TYPE.OPERATOR)
        self.assertEqual(tokens[4].value, '3')
        self.assertEqual(tokens[4].type, TOKEN_TYPE.NUMBER)

    def test4(self):
        lexer = Lexer()

        lines = []
        lines.append('DIM numbers(100)')

        tokens = lexer.lex(lines)

        self.assertEqual(tokens[0].value, 'DIM')
        self.assertEqual(tokens[0].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[1].value, 'numbers')
        self.assertEqual(tokens[1].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[2].value, '(')
        self.assertEqual(tokens[2].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[3].value, '100')
        self.assertEqual(tokens[3].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[4].value, ')')
        self.assertEqual(tokens[4].type, TOKEN_TYPE.SEPARATOR)

    def test5(self):
        lexer = Lexer()

        lines = []
        lines.append('a "" b')

        tokens = lexer.lex(lines)

        self.assertEqual(tokens[0].value, 'a')
        self.assertEqual(tokens[0].type, TOKEN_TYPE.IDENTIFIER)
        # self.assertEqual(tokens[0].id, 0)
        self.assertEqual(tokens[1].value, '"')
        self.assertEqual(tokens[1].type, TOKEN_TYPE.SEPARATOR)
        # self.assertEqual(tokens[1].id, 1)
        self.assertEqual(tokens[2].value, '"')
        self.assertEqual(tokens[2].type, TOKEN_TYPE.SEPARATOR)
        # self.assertEqual(tokens[2].id, 2)
        self.assertEqual(tokens[3].value, 'b')
        self.assertEqual(tokens[3].type, TOKEN_TYPE.IDENTIFIER)
        # self.assertEqual(tokens[3].id, 3)

    def test_st1(self):
        lexer = Lexer()

        tokens = lexer.lex_file('examples/st1.bas')

        # Area (20,25), AREAFILL STEP (50, 50)

        self.assertEqual(tokens[0].value, 'Area')
        self.assertEqual(tokens[0].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[1].value, '(')
        self.assertEqual(tokens[1].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[2].value, '20')
        self.assertEqual(tokens[2].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[3].value, ',')
        self.assertEqual(tokens[3].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[4].value, '25')
        self.assertEqual(tokens[4].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[5].value, ')')
        self.assertEqual(tokens[5].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[6].value, ',')
        self.assertEqual(tokens[6].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[7].value, 'AREAFILL')
        self.assertEqual(tokens[7].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[8].value, 'STEP')
        self.assertEqual(tokens[8].type, TOKEN_TYPE.IDENTIFIER)
        self.assertEqual(tokens[9].value, '(')
        self.assertEqual(tokens[9].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[10].value, '50')
        self.assertEqual(tokens[10].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[11].value, ',')
        self.assertEqual(tokens[11].type, TOKEN_TYPE.SEPARATOR)
        self.assertEqual(tokens[12].value, '50')
        self.assertEqual(tokens[12].type, TOKEN_TYPE.NUMBER)
        self.assertEqual(tokens[13].value, ')')
        self.assertEqual(tokens[13].type, TOKEN_TYPE.SEPARATOR)

    def test_general(self):
        lexer = Lexer()

        tokens = lexer.lex_file('examples/data.bas')
        # tokens = lexer.lex(['GADGET 1,1,"",(50,20)-(150,30),2'])
        # tokens = lexer.lex(['GADGET 2, 1, "0", (62,50)-(239,70), LONGINT'])

        for t in tokens:
            print(f'{t.value} | {t.type}')

    def test_numbers1(self):
        lexer = Lexer()

        tokens = lexer.lex(['12.3'])

        for t in tokens:
            print(f'{t.value} | {t.type}')

    def test_numbers2(self):
        lexer = Lexer()

        tokens = lexer.lex(['-3'])

        for t in tokens:
            print(f'{t.value} | {t.type}')

    def test_goto(self):
        lexer = Lexer()

        tokens = lexer.lex(['Anfang:'])

        self.assertEqual(tokens[0].value, 'Anfang')
        self.assertEqual(tokens[1].value, ':')

    def test_colons(self):
        lexer = Lexer()

        tokens = lexer.lex(['x = 3:x=1:print "test"'])

        self.assertEqual(tokens[0].value, 'x')
        self.assertEqual(tokens[1].value, '=')
        self.assertEqual(tokens[2].value, '3')
        self.assertEqual(tokens[3].value, ':')
        self.assertEqual(tokens[4].value, 'x')
        self.assertEqual(tokens[5].value, '=')
        self.assertEqual(tokens[6].value, '1')
        self.assertEqual(tokens[7].value, ':')
        self.assertEqual(tokens[8].value, 'print')
        self.assertEqual(tokens[9].value, '"')
        self.assertEqual(tokens[10].value, 'test')
        self.assertEqual(tokens[11].value, '"')


class TestParser(unittest.TestCase):

    def print_unary_operation(self, exp: NodeUnaryOperation):
        print(exp.operation_type)

        if isinstance(exp.a, NodeConstant):
            print(exp.a.value)
        elif isinstance(exp.a, NodeVariable):
            print(exp.a.name)
        elif isinstance(exp.a, NodeUnaryOperation):
            self.print_unary_operation(exp.a)

    def print_binary_operation(self, exp: NodeBinaryOperation):
        if isinstance(exp.a, NodeConstant):
            print(exp.a.value)
        elif isinstance(exp.a, NodeVariable):
            print(exp.a.name)
        elif isinstance(exp.a, NodeBinaryOperation):
            self.print_binary_operation(exp.a)

        print(exp.operation_type)

        if isinstance(exp.b, NodeConstant):
            print(exp.b.value)
        elif isinstance(exp.b, NodeVariable):
            print(exp.b.name)
        elif isinstance(exp.b, NodeBinaryOperation):
            self.print_binary_operation(exp.b)

    def print_assignment(self, assignment: NodeAssignment):
        if isinstance(assignment.variable, NodeVariable):
            print(assignment.variable.name)

        print('=')

        if isinstance(assignment.expression, NodeUnaryOperation):
            self.print_unary_operation(assignment.expression)
        if isinstance(assignment.expression, NodeBinaryOperation):
            self.print_binary_operation(assignment.expression)

    def print_expression(self, exp: NodeExpression):
        if isinstance(exp, NodeConstant):
            print(exp.value)
        elif isinstance(exp, NodeVariable):
            print(exp.name)
        elif isinstance(exp, NodeBinaryOperation):
            self.print_binary_operation(exp)

    def test_print1(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''print " 1+1 "'''
        python_code = '''print(" 1+1 ")'''

        tokens = lexer.lex(basic_code.splitlines())
        ast = p.parse(tokens)
        self.assertEqual(p.generate(ast).strip(), python_code)

    # def test_print2(self):
    #     p = Parser()
    #     lexer = Lexer()

    #     basic_code = '''print hallo test'''
    #     python_code = '''print("hallo test")'''

    #     tokens = lexer.lex(basic_code.splitlines())
    #     ast = p.parse(tokens)
    #     self.assertEqual(p.generate(ast).strip(), python_code)

    # def test_print3(self):
    #     p = Parser()
    #     lexer = Lexer()

    #     basic_code = '''print    '''
    #     python_code = '''print("")'''

    #     tokens = lexer.lex(basic_code.splitlines())
    #     ast = p.parse(tokens)
    #     self.assertEqual(p.generate(ast).strip(), python_code)

    def test_print4(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''PRINT "Average is "; 3; " units/month."'''
        python_code = '''print("Average is 3 units/month.")'''

        tokens = lexer.lex(basic_code.splitlines())
        ast = p.parse(tokens)
        self.assertEqual(p.generate(ast).strip(), python_code)

    def test_lineend(self):
        p = Parser()

        tokens = []
        tokens.append(Token(0, TOKEN_TYPE.IDENTIFIER, ''))
        tokens.append(Token(0, TOKEN_TYPE.IDENTIFIER, ''))
        tokens.append(Token(0, TOKEN_TYPE.IDENTIFIER, ''))
        tokens.append(Token(1, TOKEN_TYPE.IDENTIFIER, ''))
        tokens.append(Token(1, TOKEN_TYPE.IDENTIFIER, ''))
        tokens.append(Token(1, TOKEN_TYPE.IDENTIFIER, ''))

        popped_tokens, tokens = p.pop_until(tokens)

        self.assertEqual(len(tokens), 3)
        self.assertEqual(len(popped_tokens), 3)

    def test_colons(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''print "x":print "y":print "hallo "'''
        python_code = '''print("x")\nprint("y")\nprint("hallo ")'''

        tokens = lexer.lex(basic_code.splitlines())
        ast = p.parse(tokens)
        self.assertEqual(p.generate(ast).strip(), python_code)

    def test_string(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''print "x "; 3; " hallo"'''
        python_code = '''print("x 3 hallo")'''

        tokens = lexer.lex(basic_code.splitlines())
        ast = p.parse(tokens)
        self.assertEqual(p.generate(ast).strip(), python_code)

    def test_assign1(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''x = 3'''
        python_code = '''x = 3'''

        tokens = lexer.lex(basic_code.splitlines())
        ast = p.parse(tokens)
        self.assertEqual(p.generate(ast).strip(), python_code)

    def test_assign2(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''x = 3.4'''
        python_code = '''x = 3.4'''

        tokens = lexer.lex(basic_code.splitlines())
        ast = p.parse(tokens)
        self.assertEqual(p.generate(ast).strip(), python_code)

    def test_exp1(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '1 * 2'

        tokens = lexer.lex(basic_code.splitlines())
        expression = p.parse_additive_expression(tokens)

        self.assertEqual(expression.a.value, 1)
        self.assertEqual(expression.b.value, 2)
        self.assertEqual(expression.operation_type, OPERATION_TYPE.MULTIPLY)

    def test_exp2(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '1 + 2 - 3 + 4 - 5'

        tokens = lexer.lex(basic_code.splitlines())
        expression = p.parse_additive_expression(tokens)

        self.print_binary_operation(expression)

    def test_exp3(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''x + y * x + z'''

        tokens = lexer.lex(basic_code.splitlines())
        expression = p.parse_additive_expression(tokens)

        self.print_binary_operation(expression)

    def test_exp4(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '''-3'''

        tokens = lexer.lex(basic_code.splitlines())
        expression = p.parse_additive_expression(tokens)

        self.print_unary_operation(expression)

    def test_exp5(self):
        p = Parser()
        lexer = Lexer()

        basic_code = 'x = 1 + (2 + 3) + 1'
        # basic_code = 'x = -1'

        tokens = lexer.lex(basic_code.splitlines())
        expression = p.parse(tokens)

        self.print_assignment(expression.nodes[0])

    def test_exp6(self):
        p = Parser()
        lexer = Lexer()

        basic_code = '(1 + 2) * 3'

        tokens = lexer.lex(basic_code.splitlines())
        expression = p.parse(tokens)

        self.print_expression(expression.nodes[0])

    # def test_general(self):
    #     p = Parser()
    #     lexer = Lexer()

    #     basic_code = '''PRINT "Videotitel-Programm "
    #                     PRINT "von Franz Maier"
    #                     PRINT'''

    #     tokens = lexer.lex(basic_code.splitlines())
    #     ast = p.parse(tokens)
    #     interpreter = Interpreter()

    #     interpreter.run(ast)

        # with open('/tmp/output.py', 'w') as file:
        #     file.write(p.generate(ast))


if __name__ == '__main__':
    unittest.main()
