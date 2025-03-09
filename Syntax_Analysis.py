import sys
from sly import Lexer, Parser

class DLangLexer(Lexer):

    # Define names of tokens
    tokens ={LE, GE, EQ, NE, AND, OR, INT, DOUBLE, STRING, IDENTIFIER, NOTHING, INTK, DOUBLEK, BOOL, BOOLK, STRINGK, INTERFACE, NULL, FOR, WHILE, IF, ELSE, RETURN, BREAK, ARRAYINSTANCE, OUTPUT, INPUTINT, INPUTLINE}
    
    # Single-character literals can be recognized without token names
    # If you use separate tokens for each literal, that is fine too
    literals = {'+', '-', '*', '/', '%', '<', '>', '=','!', ';', ',', '.', '[', ']','(',')','{','}'}
    
    # Specify things to ignore
    ignore = ' \t\r' # space, tab, and carriage return
    ignore_comment1= r'\/\*[^"]*\*\/' # c-style multi-line comment (note: test with input from file)
    ignore_comment = r'\/\/.*' # single line comment
    ignore_newline=r'\n+' # end of line

    # Specify REs for each token
    STRING = r'\"(.)*\"'
    DOUBLE = r'[0-9]+\.[0-9]*([E][+-]?\d+)?'
    INT = r'[0-9]+'
    EQ = r'=='
    NE = r'!='
    LE = r'<='
    GE = r'>='
    AND = r'&&' 
    OR =  r'\|\|'
    IDENTIFIER = r'[a-zA-Z_][a-zA-Z0-9_]{0,49}'

    @_(STRING)
    def STRING_VAL(self, t):
        t.value = str(t.value)
        return t

    @_(INT)
    def NUMBER_INT(self, t):
        t.value = int(t.value)
        return t

    @_(DOUBLE)
    def NUMBER_DOUBLE(self, t):
        t.value = float(t.value)
        return t

    @_(r'True')
    def BOOL_TRUE(self, t):
        return True

    @_(r'False')
    def BOOL_FALSE(self, t):
        return False

    # IDENTIFIER lexemes overlap with keywords.
    # To avoid confusion, we do token remaping.
    # Alternatively, you can specify each keywork before IDENTIFIER
    IDENTIFIER['nothing'] = NOTHING
    IDENTIFIER['int'] = INTK
    IDENTIFIER['double'] = DOUBLEK
    IDENTIFIER['string'] = STRINGK
    IDENTIFIER['bool'] = BOOLK
    IDENTIFIER['True'] = BOOL
    IDENTIFIER['False'] = BOOL
    IDENTIFIER['null'] = NULL
    IDENTIFIER['for'] = FOR
    IDENTIFIER['while'] = WHILE
    IDENTIFIER['if'] = IF
    IDENTIFIER['else'] = ELSE
    IDENTIFIER['return'] = RETURN
    IDENTIFIER['ArrayInstance'] = ARRAYINSTANCE
    IDENTIFIER['Output'] = OUTPUT
    IDENTIFIER['InputInt'] = INPUTINT
    IDENTIFIER['InputLine'] = INPUTLINE


    def error(self,t):
        print ("Invalid character '%s'" % t.value[0])
        self.index+=1

class DLangParser(Parser):

    tokens = DLangLexer.tokens
    precedence = (
        ('nonassoc', EQ, NE, LE, GE, AND, OR, '<', '>'),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', 'UMINUS'),
        ('nonassoc', '=')
    )

    def __init__(self):
        self.IDENTIFIERs = { }


    # Program -> Decl+
    @_('Decls')
    def Program(self, p): 
        print('Parsing completed successfully!') # If we get here with no issues, bottom-up parsing is successful!
        return p
    
    @_('Decl Decls ','Decl')
    def Decls(self, p):
        #print(p)
        return p
    

    # Decl -> VariableDecl | FunctionDecl
    @_('VariableDecl', 'FunctionDecl')
    def Decl(self, p):
        # print('Found Decl')
        return p

    # VariableDecl -> Variable;
    @_('Variable ";"')
    def VariableDecl(self, p):
        print('Found VariableDecl')
        return p

    # Variable -> Type ident
    @_('Type IDENTIFIER')
    def Variable(self, p):
        return p

    # Type -> int | double | bool | string    
    @_('INTK', 'DOUBLEK', 'BOOLK', 'STRINGK')
    def Type(self, p):
        return p

    # Define parsing rules for function declarations, either with or without return types.
    @_('Type IDENTIFIER "(" Formals ")" StmtBlock', 'NOTHING IDENTIFIER "(" Formals ")" StmtBlock', )
    def FunctionDecl(self, p):
        print('Found Function Declaration')
        return p

    # Define parsing rules for statement blocks.
    @_('"{" VariableDecls Stmts "}"')
    def StmtBlock(self, p):
        print("Found Statement Block")
        return p

    # Define parsing rules for formal parameters.
    @_('Variables', 'Epsilon')
    def Formals(self, p):
        print('Found Formal Parameters')
        return p

    @_('Variable "," Variables ', 'Variable')
    def Variables(self, p):
        return p

    @_('VariableDecl VariableDecls', 'Epsilon')
    def VariableDecls(self, p):
        return p

    @_('Stmt Stmts', 'Epsilon')
    def Stmts(self, p):
        return p

    # Define parsing rules for statements, including expressions, loops, and control flow statements.
    @_('ExprQ ";"', 'IfStmt', 'WhileStmt', 'ForStmt', 'BreakStmt', 'ReturnStmt', 'OutputStmt', 'StmtBlock')
    def Stmt(self, p):
        print("Found Statement")
        return p

    @_('Expr', 'Epsilon')
    def ExprQ(self, p):
        return p

    # Define parsing rules for if statements.
    @_('IF "(" Expr ")" Stmt ElseQ')
    def IfStmt(self, p):
        print("Found If Statement")
        return p

    @_('ELSE Stmt', 'Epsilon')
    def ElseQ(self, p):
        return p

    # Define parsing rules for for statements.
    @_('FOR "(" ExprQ ";" Expr ";" ExprQ ")" Stmt ')
    def ForStmt(self, p):
        print("Found For Statement")
        return p

    # Define parsing rules for while statements.
    @_('WHILE "(" Expr ")" Stmt ')
    def WhileStmt(self, p):
        print("Found While Statement")
        return p

    # Define parsing rules for break statements.
    @_('BREAK ";"')
    def BreakStmt(self, p):
        print("Found Break Statement")
        return p

    # Define parsing rules for return statements.
    @_('RETURN ExprQ ";"')
    def ReturnStmt(self, p):
        print("Found Return Statement")
        return p

    # Define parsing rules for output statements.
    @_('OUTPUT "(" Exprs ")"')
    def OutputStmt(self, p):
        print("Found Output Statement")
        return p

    @_('Expr "," Exprs ', 'Expr')
    def Exprs(self, p):
        return p

    @_('IDENTIFIER "=" Expr', 'IDENTIFIER', 'Constant', 'Call', ' "(" Expr ")" ',
    'Expr "+" Expr', 'Expr "-" Expr', 'Expr "*" Expr', 'Expr "/" Expr', 'Expr "%" Expr', 'Expr "<" Expr', 'Expr LE Expr',
    'Expr ">" Expr', 'Expr GE Expr', 'Expr EQ Expr', 'Expr NE Expr', 'Expr AND Expr', 'Expr OR Expr', '"!" Expr',
    '"-" Expr %prec UMINUS',
    'INPUTINT "(" ")"', 'INPUTLINE "(" ")"')
    def Expr(self, p):
        print('Found Expression')
        return p

    # Define parsing rules for function calls.
    @_('IDENTIFIER "(" Actuals ")"')
    def Call(self, p):
        print("Found Function Call")
        return p

    # Define parsing rules for actual parameters.
    @_('Exprs', 'Epsilon')
    def Actuals(self, p):
        print("Found Actual Parameters")
        return p

    # Define parsing rules for constants.
    @_('intConstant ', ' doubleConstant ', ' boolConstant ', ' stringConstant ', ' null')
    def Constant(self, p):
        print("Found Constant")
        return p

    @_('STRING')
    def stringConstant(self, p):
        return p

    @_('NULL')
    def null(self, p):
        return p

    @_('INT')
    def intConstant(self, p):
        return p

    @_('DOUBLE')
    def doubleConstant(self, p):
        return p

    @_('BOOL')
    def boolConstant(self, p):
        return p

    @_('IDENTIFIER')
    def Decl(self, p):
        try:
            return self.IDENTIFIERs[p.IDENTIFIER]
        except LookupError:
            print("Undefined IDENT '%s'" % p.IDENTIFIER)
            return 0

    @_('')
    def Epsilon(self, p):
        pass

if __name__ == '__main__':

    # Expects DLang source from file
    
        # If there are two command-line arguments (including the script name)
        # Create instances of the lexer and parser
    lexer = DLangLexer()
    parser = DLangParser()
        # Open the file provided as a command-line argument
    with open('input.txt', 'r') as source:
    # Read the content of the file
        dlang_code = source.read()
        try:
        # Attempt to parse the DLang code using the lexer and parser
            parser.parse(lexer.tokenize(dlang_code))
        except EOFError:
                # If the end of the file is reached unexpectedly, exit with error code 1
            exit(1)
    
