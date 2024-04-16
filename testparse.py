class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.it = iter(self.tokens)
        self.current_token = next(self.it, None)  # Safely handle empty token list

    def next_token(self):
        """ Advances to the next token, if available. """
        self.current_token = next(self.it, None)

    def parse(self):
        """ Parses the tokens into an AST based on simple arithmetic rules. """
        if not self.current_token:
            return None  # Early exit if there are no tokens

        # Start with the first literal
        left = {'Type': 'Literal', 'value': self.current_token['value']}
        self.next_token()

        # Process as long as there are tokens and the current token is an operator
        while self.current_token and self.current_token['Type'] == 'Type.OPERATOR':
            operator = self.current_token['value']
            self.next_token()
            if not self.current_token or self.current_token['Type'] != 'Type.NUMBER':
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

# Example usage:
tokens = [
    {'Type': 'Type.NUMBER', 'value': '2'},
    {'Type': 'Type.OPERATOR', 'value': '+'},
    {'Type': 'Type.NUMBER', 'value': '4'},
    {'Type': 'Type.OPERATOR', 'value': '+'},
    {'Type': 'Type.NUMBER', 'value': '5'}
]

parser = Parser(tokens)
ast = parser.parse()
print(ast)
