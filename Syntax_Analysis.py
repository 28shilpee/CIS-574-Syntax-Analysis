from sly import Lexer, Parser

class DLangLexer(Lexer):
    tokens = {IDENT, INT_TYPE, DOUBLE_TYPE, BOOL_TYPE, STRING_TYPE, INT_CONST, DOUBLE_CONST, BOOL_CONST, STRING_CONST,
              IF, ELSE, WHILE, FOR, RETURN, BREAK, OUTPUT, INPUTINT, INPUTLINE, NOTHING, NULL,
              LE, GE, EQ, NE, AND, OR}
    literals = {';', ',', '(', ')', '{', '}', '=', '+', '-', '*', '/', '%', '<', '>', '!'}

    ignore = ' \t'

    # Ignore comments
    ignore_comment = r'//.*'

    # Keywords
    INT_TYPE = r'int'
    DOUBLE_TYPE = r'double'
    BOOL_TYPE = r'bool'
    STRING_TYPE = r'string'
    IF = r'if'
    ELSE = r'else'
    WHILE = r'while'
    FOR = r'for'
    RETURN = r'return'
    BREAK = r'break'
    OUTPUT = r'Output'
    INPUTINT = r'InputInt'
    INPUTLINE = r'InputLine'
    NOTHING = r'nothing'
    NULL = r'null'

    # Tokens
    IDENT = r'[a-zA-Z_][a-zA-Z0-9_]*'
    INT_CONST = r'\d+'
    DOUBLE_CONST = r'\d+\.\d*'
    BOOL_CONST = r'true|false'
    STRING_CONST = r'"[^"]*"'

    # Multi-character operators
    LE = r'<='
    GE = r'>='
    EQ = r'=='
    NE = r'!='
    AND = r'&&'
    OR = r'\|\|'

    @_(r'\n+')
    def newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Illegal character '{t.value[0]}' at line {self.lineno}")
        self.index += 1

class DLangParser(Parser):
    tokens = DLangLexer.tokens

    precedence = (
        ('nonassoc', IF),
        ('nonassoc', ELSE),
        ('right', '='),
        ('left', OR),
        ('left', AND),
        ('nonassoc', EQ, NE, '<', '>', LE, GE),
        ('left', '+', '-'),
        ('left', '*', '/', '%'),
        ('right', UMINUS, '!'),
    )

    @_('Decls')
    def Program(self, p):
        print("Found Program")

    @_('Decl Decls')
    def Decls(self, p):
        return [p.Decl] + p.Decls

    @_('Decl')
    def Decls(self, p):
        return [p.Decl]

    @_('VariableDecl', 'FunctionDecl')
    def Decl(self, p):
        print(f"Found {p[0]}")

    @_('Variable ";"')
    def VariableDecl(self, p):
        print("Found VariableDecl")

    @_('Type IDENT')
    def Variable(self, p):
        print(f"Found Variable: {p.Type} {p.IDENT}")

    @_('INT_TYPE', 'DOUBLE_TYPE', 'BOOL_TYPE', 'STRING_TYPE')
    def Type(self, p):
        return p[0]

    @_('Type IDENT "(" Formals ")" StmtBlock',
       'NOTHING IDENT "(" Formals ")" StmtBlock')
    def FunctionDecl(self, p):
        print(f"Found FunctionDecl: {p[0]} {p.IDENT}")

    @_('VariableList', '')
    def Formals(self, p):
        print("Found Formals")

    @_('Variable "," VariableList')
    def VariableList(self, p):
        return [p.Variable] + p.VariableList

    @_('Variable')
    def VariableList(self, p):
        return [p.Variable]

    @_('"{" VariableDeclList StmtList "}"')
    def StmtBlock(self, p):
        print("Found StmtBlock")

    @_('VariableDecl VariableDeclList', '')
    def VariableDeclList(self, p):
        print("Found VariableDeclList")

    @_('Stmt StmtList', '')
    def StmtList(self, p):
        print("Found StmtList")

    @_('ExprStmt', 'IfStmt', 'WhileStmt', 'ForStmt', 'BreakStmt', 'ReturnStmt', 'OutputStmt', 'StmtBlock')
    def Stmt(self, p):
        print(f"Found Stmt: {p[0]}")

    @_('Expr ";"')
    def ExprStmt(self, p):
        print("Found ExprStmt")

    @_('IF "(" Expr ")" Stmt %prec IF')
    def IfStmt(self, p):
        print("Found If Statement")

    @_('IF "(" Expr ")" Stmt ELSE Stmt')
    def IfStmt(self, p):
        print("Found If-Else Statement")

    @_('WHILE "(" Expr ")" Stmt')
    def WhileStmt(self, p):
        print("Found WhileStmt")

    @_('FOR "(" ExprOpt ";" Expr ";" ExprOpt ")" Stmt')
    def ForStmt(self, p):
        print("Found ForStmt")

    @_('Expr', '')
    def ExprOpt(self, p):
        return p[0] if p else None

    @_('RETURN Expr ";"', 'RETURN ";"')
    def ReturnStmt(self, p):
        print("Found ReturnStmt")

    @_('BREAK ";"')
    def BreakStmt(self, p):
        print("Found BreakStmt")

    @_('OUTPUT "(" ExprList ")" ";"')
    def OutputStmt(self, p):
        print("Found OutputStmt")

    @_('Expr')
    def ExprList(self, p):
        return [p.Expr]

    @_('Expr "," ExprList')
    def ExprList(self, p):
        return [p.Expr] + p.ExprList

    @_('IDENT "=" Expr',
       'Expr OR Expr',
       'Expr AND Expr',
       'Expr EQ Expr',
       'Expr NE Expr',
       'Expr "<" Expr',
       'Expr ">" Expr',
       'Expr LE Expr',
       'Expr GE Expr',
       'Expr "+" Expr',
       'Expr "-" Expr',
       'Expr "*" Expr',
       'Expr "/" Expr',
       'Expr "%" Expr',
       '"-" Expr %prec UMINUS',
       '"!" Expr',
       '"(" Expr ")"',
       'IDENT',
       'Constant',
       'Call',
       'INPUTINT "(" ")"',
       'INPUTLINE "(" ")"')
    def Expr(self, p):
        print("Found Expr")

    @_('IDENT "(" Actuals ")"')
    def Call(self, p):
        print("Found Call")

    @_('ExprList', '')
    def Actuals(self, p):
        print("Found Actuals")

    @_('INT_CONST', 'DOUBLE_CONST', 'BOOL_CONST', 'STRING_CONST', 'NULL')
    def Constant(self, p):
        print(f"Found Constant: {p[0]}")

    def error(self, p):
        if p:
            print(f"Found syntax error at {p.type}")
        else:
            print("Found syntax error at EOF")

def debug_print_tokens(lexer, data):
    for token in lexer.tokenize(data):
        print(f"Token: type={token.type}, value={token.value}, line={token.lineno}, index={token.index}")

if __name__ == '__main__':
    lexer = DLangLexer()
    parser = DLangParser()
    
    print("DLang Parser")
    print("Enter 'file' to read from 'input.txt', or 'exit' to quit.")
    
    while True:
        user_input = input("Enter your choice (file/exit): ").lower()
        if user_input == 'exit':
            print("Exiting the program.")
            break
        elif user_input == 'file':
            try:
                with open('input.txt', 'r') as file:
                    data = file.read()
                print("Contents of 'input.txt':")
                print(data)
                print("\nTokenizing input:")
                debug_print_tokens(lexer, data)
                print("\nParsing code from 'input.txt':")
                result = parser.parse(lexer.tokenize(data))
                print("Parsing completed successfully!")
            except FileNotFoundError:
                print("Error: 'input.txt' not found.")
            except Exception as e:
                print(f"Parsing failed: {str(e)}")
        else:
            print("Invalid choice. Please enter 'file' or 'exit'.")