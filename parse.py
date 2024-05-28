import sys
from lex import *

class Parser:
    def __init__(self,lexer):
        self.lexer = lexer
        self.curToken = None
        self.peekToken = None
        self.nextToken()
        self.nextToken()


    def checkToken(self,kind):   # Return true if the current token matches.
        return kind == self.curToken.kind

    def checkPeek(self, kind):
        return kind == self.peekToken.kind

    def nextToken(self):
        self.curToken = self.peekToken
        self.peekToken = self.lexer.getToken()
        
    def match(self, kind):
        if( not self.checkToken(kind)):
            self.abort("Expected " + kind.name + ", got " + self.curToken.kind.name)
        self.nextToken()

    def nl(self):
        print("NEWLINE")
        #checking if this is a match for new line else abort 
        self.match(TokenType.NEWLINE)
        #we also allow multiple newlines so..
        while(self.checkToken(TokenType.NEWLINE)):
            self.nextToken()

    def program(self):
        print("PROGRAM")

        # Parse all the statements in the program.
        while not self.checkToken(TokenType.EOF):
            self.statement()

    def statement(self):

        print("PROGRAM")
        if(self.checkToken(TokenType.PRINT)):
            print("STATEMENT-PRINT")
            self.nextToken()
            if(self.checkToken(TokenType.STRING)):
                self.nextToken()
            else:
                self.expression()
            self.nl()
        elif self.checkToken(TokenType.IF):
            self.nextToken()
            self.comparision()

            self.match(TokenType.THEN)
            self.nl()

            while( not self.checkToken(TokenType.ENDIF)):
                self.statement()
                self.match(TokenType.ENDIF)
            
            


    def abort(self,err):
        pass

