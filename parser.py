from enum import Enum, auto
import re
from lexer import Lexer, Token, TOKEN_TYPE


class OPERATION_TYPE(Enum):
    ADD = auto()
    SUBTRACT = auto()
    MULTIPLY = auto()
    DIVIDE = auto()
    COMPARE_LT = auto()
    COMPARE_GT = auto()


class Node():
    def __init__(self):
        pass


class NodeStatement(Node):
    def __init__(self):
        pass


class NodeExpression(Node):
    def __init__(self, node: Node):
        self.node = node


class NodeVariable(Node):
    def __init__(self, name: str):
        self.name = name


class NodeConstant(Node):
    def __init__(self, value):
        self.value = value


class NodeConstantInt(NodeConstant):
    def __init__(self, value: int):
        self.value = value


class NodeConstantFloat(NodeConstant):
    def __init__(self, value: float):
        self.value = value


class NodeConstantString(NodeConstant):
    def __init__(self, value: str):
        self.value = value


class NodeAssignment(Node):
    def __init__(self, variable: NodeVariable, expression: NodeExpression):
        self.variable = variable
        self.expression = expression


class NodeBinaryOperation(Node):
    def __init__(self, a: Node, b: Node, type: OPERATION_TYPE):
        self.a = a
        self.b = b
        self.type = type


class If(Node):
    def __init__(self, condition: NodeBinaryOperation, if_statements: list[NodeStatement]):
        self.condition = condition
        self.if_statements = if_statements


class IfElse(Node):
    def __init__(self, condition: NodeBinaryOperation, if_statements: list[NodeStatement], else_statements: list[NodeStatement]):
        self.condition = condition
        self.if_statements = if_statements
        self.else_statements = else_statements


class NodePrint(Node):
    def __init__(self, string: NodeConstantString):
        self.string = string


class AST():
    def __init__(self, nodes=list[Node]):
        self.nodes = nodes


class Parser():
    def __init__(self):
        pass

    def pop_until(self, tokens: list[Token], end: str = '\n') -> tuple[list[Token], list[Token]]:
        popped_tokens = []

        idx = 0
        starting_line = tokens[0].line

        while idx < len(tokens):
            # Pop until linebreak
            if end == '\n':
                if tokens[idx].line != starting_line:
                    popped_tokens = tokens[:idx]
                    tokens = tokens[idx:]
                    break

            # Pop until colon
            if end == ':':
                if tokens[idx].type == TOKEN_TYPE.SEPARATOR:
                    if tokens[idx].value == ':':
                        popped_tokens = tokens[:idx]
                        # Don’t include separator
                        tokens = tokens[idx + len(tokens[idx].value):]
                        break
            idx += 1

        if not popped_tokens:
            popped_tokens = tokens
            tokens = []

        return popped_tokens, tokens

    def parse_constant(self, token: Token) -> NodeConstant:
        if token.value.isnumeric():
            return NodeConstantInt(int(token.value))
        elif re.match(r'[0-9]+\.[0-9]+', token.value):
            return NodeConstantFloat(float(token.value))
        raise Exception('Unknown constant type')

    def parse_assign(self, tokens: list[Token]) -> NodeAssignment:
        if len(tokens) >= 2:
            if tokens[1].type == TOKEN_TYPE.OPERATOR and tokens[1].value == '=':
                if tokens[2].type == TOKEN_TYPE.NUMBER:
                    variable = NodeVariable(tokens[0].value)
                    try:
                        # expression = self.parse_constant(tokens[2])
                        expression = self.parse_exp(tokens[2:])
                    except Exception:
                        print('Error parsing assign')
                    else:
                        tokens.pop(0)
                        tokens.pop(0)
                        tokens.pop(0)
                        return NodeAssignment(variable, expression)

        raise Exception

    def parse_string(self, tokens: list[Token]) -> NodeConstantString:
        string = ''

        while tokens:
            token = tokens[0]

            if token.type == TOKEN_TYPE.SEPARATOR and token.value == '"':
                tokens.pop(0)
            elif token.type == TOKEN_TYPE.LITERAL:
                string += token.value
                tokens.pop(0)
            elif token.type == TOKEN_TYPE.NUMBER:
                # string += ' ' + token.value
                string += token.value
                tokens.pop(0)

                # If more tokens follow, add space
                # if tokens:
                #     string += ' '
            elif token.type == TOKEN_TYPE.SEPARATOR and token.value == ';':
                tokens.pop(0)

        return NodeConstantString(string)

    def parse_identifier(self, tokens: list[Token]) -> Node:
        token = tokens[0]

        match token.value.lower():
            case 'print':
                tokens.pop(0)
                return NodePrint(self.parse_string(tokens))
            case _:
                return self.parse_assign(tokens)
        raise Exception

    # def eval(self, number_l: NodeConstant, number_r: NodeConstant, operator: str) -> NodeConstant:
    #     match operator:
    #         case '+':
    #             return number_l.value + number_r.value
    #         case '-':
    #             return number_l.value - number_r.value
    #         case '*':
    #             return number_l.value * number_r.value
    #         case '/':
    #             return number_l.value / number_r.value
    #     raise Exception('Unknown operator')

    def get_operator_type(self, token: Token) -> OPERATION_TYPE:
        match token.value:
            case '+':
                return OPERATION_TYPE.ADD
            case '-':
                return OPERATION_TYPE.SUBTRACT
            case '*':
                return OPERATION_TYPE.MULTIPLY
            case '/':
                return OPERATION_TYPE.DIVIDE
            case '<':
                return OPERATION_TYPE.COMPARE_LT
            case '>':
                return OPERATION_TYPE.COMPARE_GT
        raise Exception('Unknown operator')

    def parse_exp(self, tokens: list[Token]) -> NodeExpression:
        match len(tokens):
            case 1:
                if tokens[0].type == TOKEN_TYPE.NUMBER:
                    return NodeExpression(self.parse_constant(tokens[0]))
            case 3:
                number_l = None
                number_r = None
                operator = ''

                if tokens[0].type == TOKEN_TYPE.NUMBER:
                    number_l = self.parse_constant(tokens[0])

                if tokens[1].type == TOKEN_TYPE.OPERATOR:
                    operator = self.get_operator_type(tokens[1])

                if tokens[2].type == TOKEN_TYPE.NUMBER:
                    number_r = self.parse_constant(tokens[2])

                if number_l and number_r and operator:
                    return NodeExpression(NodeBinaryOperation(number_l, number_r, operator))
        raise Exception('Failed parsing expression')

    def parse(self, tokens: list[Token]) -> AST:
        nodes = []

        while tokens:
            # Split into lines by colons
            line, tokens = self.pop_until(tokens, ':')

            while line:
                token = line[0]

                match token.type:
                    case TOKEN_TYPE.IDENTIFIER:
                        try:
                            nodes.append(self.parse_identifier(line))
                        except Exception:
                            print('Parser error')

        return AST(nodes)

    def generate_exp(self, expression: NodeExpression) -> str:
        output = ''

        if isinstance(expression.node, NodeConstantInt) or isinstance(expression.node, NodeConstantFloat):
            output = expression.node.value

        return str(output)

    def generate(self, ast: AST) -> str:
        output = ''

        for node in ast.nodes:
            if isinstance(node, NodePrint):
                output += f'print("{node.string.value}")'
            if isinstance(node, NodeAssignment):
                output += f'{node.variable.name} = {self.generate_exp(node.expression)}'
            if isinstance(node, NodeBinaryOperation):
                pass

            output += '\n'

        return output
