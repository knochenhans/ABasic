from lexer import *
from parser import *
import subprocess


class InterpreterLine():
    def __init__(self, line: str):
        self.line = ''


class Interpreter():
    def __init__(self) -> None:
        self.proc = subprocess.Popen('python', stdin=subprocess.PIPE, shell=True)

    def run_cmd(self, cmd: str) -> None:
        self.proc.stdin.write(str.encode(cmd + '\n'))

    def run(self, ast: AST):
        for node in ast.nodes:
            if isinstance(node, NodePrint):
                self.run_cmd(f'print("{node.literal}")')

        self.proc.communicate(b'')

# p = Parser()
# lexer = Lexer()

# basic_code = '''PRINT "Videotitel-Programm "
#                 PRINT "von Franz Maier"
#                 PRINT'''

# tokens = lexer.lex(basic_code.splitlines())
# ast = p.parse(tokens)
# interpreter = Interpreter()

# interpreter.run(ast)
