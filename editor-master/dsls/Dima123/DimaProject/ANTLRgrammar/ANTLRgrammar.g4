grammar ANTLRgrammar; 

grammar_: grammarDecl (lexer_rule | parser_rule)+; 
grammarDecl : grammarType grammar_name SEMI; 
lexer_rule : lexer_name COLON (operand)* SEMI; 
operand : LBRACE? (string | lexer_name | parser_name ) OPERATION? RBRACE?; 
parser_rule : parser_name COLON (operand)* SEMI; 
grammarType : GRAMMAR; 
grammar_name : (NAME | LEXER_NAME | PARSER_NAME); 
lexer_name : LEXER_NAME; 
parser_name : PARSER_NAME; 
string : STRING; 
// post_operation : string | lexer_name | parser_name | in_braces OPERATION; 
// in_braces : LBRACE (string | lexer_name | parser_name | post_operation) RBRACE; 

GRAMMAR : 'grammar'; 
STRING : QUOTE SYM QUOTE; 
LEXER_NAME: SMALL_LETTER SYM; 
PARSER_NAME: BIG_LETTER SYM; 
NAME : (BIG_LETTER | SMALL_LETTER) SYM; 
SEMI : ';'; 
COLON : ':'; 
QUOTE : '\''; 
OPERATION : OPERATIONF; 

// fragment PARSER_NAMEF : ('A' .. 'Z' | '_')+; 
// fragment LEXER_NAMEF : ('a' .. 'z' | '_')+; 
// fragment GRAMMAR_NAMEF : ('A' .. 'Z' | 'a' .. 'z')+; 
fragment BIG_LETTER : 'A'..'Z'; 
fragment SMALL_LETTER : 'a'..'z'; 
fragment SYM : ('A'..'Z'| '\t' | '\r' | '\n' | 'a'..'z' | '0'..'9' | '_' | '-' | '.' | '(' | ')' | '{' | '}' | '[' | ']' | '<' | '>' | '=')*; 
fragment OPERATIONF : '*' | '+' | '?'; 
fragment LBRACE : '('; 
fragment RBRACE : ')'; 

SPACE: [ \t\r\n] -> skip; 
