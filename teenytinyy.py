from lex import *
from parse import *

def main():
    print("Teeny Tiny Compiler")
    if len(sys.argv) != 2:
        sys.exit("Error: Compiler needs source file as argument.")
    with open(sys.argv[1], 'r') as inputFile:
        source = inputFile.read()


    # Initialize the lexer and parser.
    lexer = Lexer(source)

    # token = lexer.getToken()
    # while token.kind != TokenType.EOF:
    #     print(token.kind)
    #     token = lexer.getToken()
    parser = Parser(lexer)

    parser.program() # Start the parser.
    print("Parsing completed.")
#  Lexer is done :) Parser in progress
main()