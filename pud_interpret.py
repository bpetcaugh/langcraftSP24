print("My new DUCK language.")

input = "2 * 4"
tokens = Lexer(input)
ast = Parser(tokens)
result = Interpreter(ast)
print(result)