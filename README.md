# CIS-574-Syntax-Analysis
# DLang Parser
This project implements a syntax analyzer (parser) for DLang, a custom programming language. The parser is built using the SLY (Sly Lex Yacc) library in Python.

## Features
- Lexical analysis of DLang code
- Syntactic analysis based on DLang grammar
- Support for variable declarations, function declarations, control structures, and expressions
- Error reporting for syntax errors
- Debug mode for token visualization

## Requirements
- Python 3.6 or higher
- SLY library

To install SLY, run:
pip install sly
<<<<<<< HEAD

## Usage
1. Saved the parser code as `Syntax_Analysis.py`.
2. Created an `input.txt` file in the same directory with your DLang code.
3. Ran the code

python CIS-574-Syntax_Analysis.py

## DLang Grammar

The parser implements the following grammar:
- Program → Decl+
- Decl → VariableDecl | FunctionDecl
- VariableDecl → Variable;
- Variable → Type ident
- Type → int | double | bool | string
- FunctionDecl → Type ident ( Formals ) StmtBlock | nothing ident ( Formals ) StmtBlock
- Formals → Variable+, | ε
- StmtBlock → { VariableDecl* Stmt* }
- Stmt → <Expr> ; | IfStmt | WhileStmt | ForStmt | BreakStmt | ReturnStmt | OutputStmt | StmtBlock
- IfStmt → if ( Expr ) Stmt <else Stmt>
- WhileStmt → while ( Expr ) Stmt
- ForStmt → for ( <Expr> ; Expr ; <Expr> ) Stmt
- ReturnStmt → return <Expr> ;
- BreakStmt → break ;
- OutputStmt → Output ( Expr+, ) ;
- Expr → [Various expression types]

## Output
The parser will print "Found <construct>" for each valid program construct it encounters. If parsing completes successfully, it will print "Parsing completed successfully!". In case of syntax errors, it will report the error location.

## Error Handling
The parser provides error messages for:
- Illegal characters in the input
- Syntax errors, specifying the token where the error occurred

## Limitations
- The parser may have some shift/reduce conflicts due to the nature of the SLY LALR(1) parser generator.
- Error recovery is limited; the parser will stop at the first syntax error encountered.
=======
>>>>>>> 14022983c82e29ae56978bf271898965193a38e1
