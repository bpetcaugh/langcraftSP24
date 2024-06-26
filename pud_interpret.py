from enum import Enum
import re
import sys

'''
Some additional thoughts:
1. Where do I check the grammar?
2. How do I handle multiple lines of commands? (???)
3. Where do I store variables as I'm interpreting code?

'''

class Type(Enum):
    IDENTIFIER = "IDENTIFIER"
    OPERATOR = "OPERATOR"
    EOC = "ENDOFCOMMAND"
    EQUALS = "EQUALS"
    NUMBER = "NUMBER"


class Lexer:
    def __init__(self, i):
        self.i = i.split()
        self.out = []


    def lex(self):
        #patterns to check
        p_add = r'\+'
        p_sub = r'\-'
        p_digits = r'^\d+$'

        for token in self.i:
            if re.fullmatch(p_add, token):
                self.out.append({"Type": Type.OPERATOR, "value":token})
            elif re.fullmatch(p_digits, token):
                self.out.append({"Type": Type.NUMBER, "value":token})

        return self.out

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.it = iter(self.tokens)
        self.current_token = next(self.it, None)

    def next_token(self):
        """ Advances to the next token, if available. """
        self.current_token = next(self.it, None)

    def parse(self):
        '''
        BEFORE you build the AST, check that the command is
        a valid grammar. 
        '''

        """ Parses the tokens into an AST based on simple arithmetic rules. """
        if not self.current_token:
            return None  # Early exit if there are no tokens

        # Start with the first literal
        left = {'Type': 'Literal', 'value': self.current_token['value']}
        self.next_token()

        # Process as long as there are tokens and the current token is an operator
        while self.current_token and self.current_token['Type'] == Type.OPERATOR:
            operator = self.current_token['value']
            self.next_token()
            if not self.current_token or self.current_token['Type'] != Type.NUMBER:
                raise ValueError("Expected a number after operator")
            
            right = {'Type': 'Literal', 'value': self.current_token['value']}
            left = {
                'Type': 'BinaryOperation',
                'operator': operator,
                'left': left,
                'right': right
            }
            self.next_token()

        return left

def pretty_print_ast(ast, indent=0):
    """ Recursively prints the AST in a human-readable format with indentation. """
    if ast['Type'] == 'Literal':
        print(' ' * indent + f"Literal({ast['value']})")
    elif ast['Type'] == 'BinaryOperation':
        print(' ' * indent + f"BinaryOperation({ast['operator']})")
        print(' ' * indent + '├─ left:')
        pretty_print_ast(ast['left'], indent + 4)
        print(' ' * indent + '└─ right:')
        pretty_print_ast(ast['right'], indent + 4)

class Interpreter:
    def __init__(self):
        pass

    def evaluate_ast(self, ast):
        """ Recursively evaluates the AST to compute the result of the expression. """
        if ast['Type'] == 'Literal':
            return int(ast['value'])  # Convert the value to an integer and return it

        elif ast['Type'] == 'BinaryOperation':
            left_val = self.evaluate_ast(ast['left'])  # Recursively evaluate the left child
            right_val = self.evaluate_ast(ast['right'])  # Recursively evaluate the right child

            # Perform the operation based on the operator
            if ast['operator'] == '+':
                return left_val + right_val
            elif ast['operator'] == '-':
                return left_val - right_val
            elif ast['operator'] == '*':
                return left_val * right_val
            elif ast['operator'] == '/':
                if right_val == 0:
                    raise ValueError("Division by zero")  # Handle division by zero
                return left_val / right_val
            else:
                raise ValueError(f"Unsupported operator: {ast['operator']}")

input = ""
debug = False

# Run file without command line
# with open("test.pud", "r") as file:
#     input = file.read().replace("\n", " ")

################################################################
#Check for Puddle file type, and run on command line
if len(sys.argv) > 1:
    if not sys.argv[1].endswith('.pud'):
        print("Error: The file is not a Puddle file.")
        sys.exit()

try:
    with open(sys.argv[1], 'r') as file:
        input = file.read().replace("\n", " ")
except FileNotFoundError:
    print("Error: The file does not exist.")
except Exception as e:
    print(f"An error occurred: {e}")
################################################################

if debug:
    print("\n--------INPUT--------")
    print(input)

tokens = Lexer(input).lex()

if debug:
    print("\n--------TOKENS--------")
    print("")
    for t in tokens:
        print(t)
    print("")

ast = Parser(tokens).parse()

if debug:
    print("\n--------AST--------")
    print(ast)

result = Interpreter().evaluate_ast(ast)

if debug:
    print("\n--------RESULT--------")
    print(f" The result of your line of code is: {result}\n")
else:
    print(result)