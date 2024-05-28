import enum
import sys
class Lexer:
    def __init__(self, input):
        self.source = input + '\n' # Source code to lex as a string. Append a newline to simplify lexing/parsing the last token/statement.
        self.curChar = ''   # Current character in the string.
        self.curPos = -1    # Current position in the string.
        self.nextChar()

    # Process the next character.
    def nextChar(self):
        self.curPos += 1
        if self.curPos >= len(self.source):
            self.curChar = '\0'  # EOF
        else:
            self.curChar = self.source[self.curPos]

    # Return the lookahead character.
    def peek(self):
        if self.curPos + 1 >= len(self.source):
            return '\0'
        return self.source[self.curPos+1]

    def abort(self, message):
        sys.exit("Lexing error. " + message)
    
    def skipWhitespace(self):
        if self.curChar == ' ' or self.curChar == '\t' or self.curChar == '\r':
            self.nextChar()
    def skipComments(self):
        if self.curChar == '#':
            while self.curChar != '\n':
                self.nextChar()

    #is ths curr char a token
    def getToken(self): # this will spit out token one by one
        self.skipWhitespace()  
        self.skipComments()

        token = None
        if self.curChar == '+':
            if(self.peek() == '='):
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar, TokenType.PLUSEQ)
            else:
                token = Token(self.curChar, TokenType.PLUS)
        elif self.curChar == '-':
            if(self.peek() == '='):
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar, TokenType.MINUSEQ)
            else:
                token = Token(self.curChar, TokenType.MINUS)
        elif self.curChar == '*':
            if(self.peek() == '='):
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar, TokenType.ASTERISKEQ)
            else:
                token = Token(self.curChar, TokenType.ASTERISK)
        elif self.curChar == '/':
            if(self.peek() == '='):
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar, TokenType.SLASHEQ)
            else:
                token = Token(self.curChar, TokenType.SLASH)

        elif self.curChar == '=':
            if self.peek() == '=': 
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar,TokenType.EQEQ)
            else: 
                token = Token(self.curChar, TokenType.EQ)
        
        elif self.curChar == '>':
            if self.peek() == '=': 
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar,TokenType.GTEQ)
            else: 
                token = Token(self.curChar, TokenType.GT)
        elif self.curChar == '<':
            if self.peek() == '=': 
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar,TokenType.LTEQ)
            else: 
                token = Token(self.curChar, TokenType.LT)
        elif self.curChar == '!':
            if self.peek() == '=': 
                lastchar = self.curChar
                self.nextChar()
                token = Token(lastchar+self.curChar,TokenType.NOTEQ)
            else: 
                self.abort("expected != got !"+self.peek())

        elif self.curChar == '\"':

            self.nextChar()
            startpos = self.curPos

            while self.curChar != '\"':
                if self.curChar == '\r' or self.curChar == '\n' or self.curChar == '\t' or self.curChar == '\\' or self.curChar == '%':
                    self.abort("Illegal character in string.")
                self.nextChar()
            
            token = Token(self.source[startpos : self.curPos], TokenType.STRING)

        elif self.curChar.isdigit():
            startpos = self.curPos
            cnt = 0
            while (self.curChar.isdigit() or self.curChar == '.'):
                if(self.curChar == '.'):
                    if(cnt == 1):
                        self.abort("expecting a number after \".\" point got :->"+ self.curChar )
                    else:
                        cnt = cnt+1 
                        if(not self.peek().isdigit() ):
                            self.abort("expecting a number after \".\" point got :->"+ self.curChar )

                self.nextChar()

            token = Token(self.source[startpos : self.curPos+1], TokenType.NUMBER)

        elif self.curChar.isalpha() or self.curChar == '_':
            # this will be identifier or keyword 
            # jab tak alphabest mileneg which are allowed tab tak leo and check kro ke keyword to nhi hai 
            # else isko identifier me daaldo 
            startpos = self.curPos
            while(self.peek().isalnum() or self.peek() == '_'):
                self.nextChar()

            toktext = self.source[startpos : self.curPos + 1 ]
            keyword = Token.isKeyword(toktext)
            if( keyword == None ):
                token = Token(toktext,TokenType.IDENT)
            else: 
                token = Token(toktext, keyword)

        elif self.curChar == '\n':
            token = Token(self.curChar, TokenType.NEWLINE)
        elif self.curChar == '\0':
            token = Token(self.curChar, TokenType.EOF)
        else: 
            self.abort("wrong token : " + self.curChar +"<- ")

        self.nextChar()
        return token        


        

class Token:
    def __init__(self, tokenText, tokenKind):
        self.text = tokenText
        self.kind = tokenKind

    @staticmethod
    def isKeyword(str):
        for kind in TokenType :
            if( kind.name == str and kind.value >= 100 and kind.value < 200):
                return kind
        return None
   
    
class TokenType(enum.Enum):
    EOF = -1
    NEWLINE = 0
    NUMBER = 1
    IDENT = 2
    STRING = 3
    # Keywords.
    LABEL = 101
    GOTO = 102
    PRINT = 103
    INPUT = 104
    LET = 105
    IF = 106
    THEN = 107
    ENDIF = 108
    WHILE = 109
    REPEAT = 110
    ENDWHILE = 111
	# Operators.
    EQ = 201  
    PLUS = 202
    MINUS = 203
    ASTERISK = 204
    SLASH = 205
    EQEQ = 206
    NOTEQ = 207
    LT = 208
    LTEQ = 209
    GT = 210
    GTEQ = 211
    PLUSEQ = 212
    MINUSEQ = 213
    SLASHEQ = 214
    ASTERISKEQ = 215


