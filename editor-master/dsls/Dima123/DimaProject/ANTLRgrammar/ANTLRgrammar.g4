grammar ANTLRgrammar; 

grammar_: grammar_decl (lexer_command | lexer_rule | parser_rule )+; 
grammar_decl : grammarType grammar_name SEMI; 
lexer_command : lexer_name COLON alternative ARROW command SEMI; 
lexer_rule : lexer_name COLON operand+ SEMI; 
parser_rule : parser_name COLON operand+ SEMI; 
operand : LBRACE operand RBRACE 
// | LSBRACE operand RSBRACE 
| operand POST_OPERATION 
| PRED_OPERATION operand 
| (string | lexer_name | parser_name)+; 
grammarType : GRAMMAR; 
grammar_name : (NAME | LEXER_NAME | PARSER_NAME); 
lexer_name : LEXER_NAME; 
parser_name : PARSER_NAME; 
lexer_command_ : LEXER_COMMAND; 
string : STRING; 
command : COMMAND; 
alternative: ALTERNATIVE; 

GRAMMAR : 'grammar'; 
COMMAND: ('skip' | 'more'); 
ALTERNATIVE: LSBRACE AL_SYM RSBRACE; 
STRING : QUOTE SYM QUOTE; 
LEXER_NAME: BIG_LETTER SYM_NAME; 
PARSER_NAME: SMALL_LETTER SYM_NAME; 
NAME : (BIG_LETTER | SMALL_LETTER) SYM; 
SEMI : ';'; 
COLON : ':'; 
QUOTE : '\''; 
POST_OPERATION : POST_OPERATIONF; 
PRED_OPERATION : PRED_OPERATIONF; 


fragment BIG_LETTER : 'A'..'Z'; 
fragment SMALL_LETTER : 'a'..'z'; 
LSBRACE : '['; 
RSBRACE : ']'; 
fragment AL_SYM : ('A'..'Z'| '\\t' | '\\r' | '\\n' | ' ' | 'a'..'z' | '0'..'9' | '_' | '-' | '.' | '(' | ')' | '{' | '}' | '[' | ']' | '<' | '>' | '=')*; 
fragment SYM_NAME : ('A'..'Z'| '\t' | '\r' | '\n' | 'a'..'z' | '0'..'9' | '_')*; 
fragment SYM : ('A'..'Z'| '\t' | '\r' | '\n' | 'a'..'z' | '0'..'9' | '_' | '-' | '.' | '(' | ')' | '{' | '}' | '[' | ']' | '<' | '>' | '=')*; 
fragment POST_OPERATIONF : '*' | '+' | '?'; 
fragment PRED_OPERATIONF : '~'; 
LBRACE : '('; 
RBRACE : ')'; 

ARROW : '->'; 

SPACE: [ \t\r\n] -> skip; 
