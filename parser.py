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


# class UNARY_OPERATION_TYPE(Enum):
#     NEGATION = auto()


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
    def __init__(self, variable: NodeVariable, expression: Node):
        self.variable = variable
        self.expression = expression


class NodeUnaryOperation(Node):
    def __init__(self, a: Node, operation_type: OPERATION_TYPE):
        self.a = a
        self.operation_type = operation_type


class NodeBinaryOperation(Node):
    def __init__(self, a: Node, b: Node, operation_type: OPERATION_TYPE):
        self.a = a
        self.b = b
        self.operation_type = operation_type


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
        raise Exception('Failed parsing constant: Unknown constant type')

    def parse_assign(self, tokens: list[Token]) -> NodeAssignment:
        if len(tokens) > 2:
            if tokens[1].type == TOKEN_TYPE.OPERATOR and tokens[1].value == '=':
                variable = NodeVariable(tokens[0].value)
                expression = self.parse_additive_expression(tokens[2:])
                return NodeAssignment(variable, expression)

        raise Exception('Failed parsing assign')

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

    def parse_expression(self, tokens: list[Token]) -> Node:
        # Assign
        try:
            assign = self.parse_assign(tokens)
        except Exception:
            pass
        else:
            return assign

        # Binary operator / Unary operator / Constant / Variable
        try:
            expression = self.parse_additive_expression(tokens)
        except Exception:
            pass
        else:
            return expression

        raise Exception('Failed parsing expression')

    def parse_identifier(self, tokens: list[Token]) -> Node:
        token = tokens[0]

        match token.value.lower():
            case 'print':
                tokens.pop(0)
                return NodePrint(self.parse_string(tokens))
            case _:
                return self.parse_expression(tokens)

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

    def parse_exp_identifier(self, token: Token) -> Node:
        match token.type:
            case TOKEN_TYPE.NUMBER:
                return self.parse_constant(token)
            case TOKEN_TYPE.IDENTIFIER:
                return NodeVariable(token.value)
        raise Exception('Unknown identifier in expression')

    def parse_factor(self, tokens: list[Token]) -> Node:
        token = tokens.pop(0)

        if token.type == TOKEN_TYPE.SEPARATOR:
            if token.value == '(':
                # "(" <exp> ")"
                expression = self.parse_additive_expression(tokens)

                token = tokens.pop(0)

                if token.type == TOKEN_TYPE.SEPARATOR:
                    if token.value == ')':
                        return expression
                    else:
                        raise Exception('Failed parsing factor: Missing closing parenthesis')

        elif token.type == TOKEN_TYPE.OPERATOR:
            # <unary_op> <factor>
            operator = self.get_operator_type(token)
            factor = self.parse_factor(tokens)
            return NodeUnaryOperation(factor, operator)

        elif token.type == TOKEN_TYPE.NUMBER or token.type == TOKEN_TYPE.IDENTIFIER:
            return self.parse_exp_identifier(token)

        raise Exception('Failed parsing factor')

    def parse_term(self, tokens: list[Token]) -> Node:
        # <factor> { ("*" | "/") <factor> }
        term = self.parse_factor(tokens)

        if len(tokens) > 0:
            next = tokens[0]

            while next.type == TOKEN_TYPE.OPERATOR and (next.value == '*' or next.value == '/'):
                operator = self.get_operator_type(tokens.pop(0))
                next_term = self.parse_factor(tokens)
                term = NodeBinaryOperation(term, next_term, operator)

                if len(tokens) > 0:
                    next = tokens[0]
                else:
                    break

        return term

    def parse_additive_expression(self, tokens: list[Token]) -> Node:
        # <term> { ("+" | "-") <term> }
        term = self.parse_term(tokens)

        if len(tokens) > 0:
            next = tokens[0]

            while next.type == TOKEN_TYPE.OPERATOR and (next.value == '+' or next.value == '-'):
                operator = self.get_operator_type(tokens.pop(0))
                next_term = self.parse_term(tokens)
                term = NodeBinaryOperation(term, next_term, operator)

                if len(tokens) > 0:
                    next = tokens[0]
                else:
                    break

        return term

    def parse(self, tokens: list[Token]) -> AST:
        nodes = []

        while tokens:
            # Split into lines by colons
            line, tokens = self.pop_until(tokens, ':')

            while line:
                token = line[0]

                try:
                    match token.type:
                        case TOKEN_TYPE.IDENTIFIER:
                            nodes.append(self.parse_identifier(line))
                        case _:
                            nodes.append(self.parse_expression(line))
                    line = []
                except Exception:
                    print('Parser error')

        return AST(nodes)

    def generate_exp(self, expression: NodeExpression) -> str:
        output = ''

        if isinstance(expression, NodeConstantInt) or isinstance(expression, NodeConstantFloat):
            output = expression.value

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
