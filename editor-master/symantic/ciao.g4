grammar ciao;

p : (n v? e? a? r? q? u)+ ;

n : ID ;

v : 'VAR' ( ID  ':=' atom )+ ;

e : 'REQUIRED' ( ID '(' variables ')' )+ ;

a : 'PROVIDED' ( ID '(' variables ')' )+ ;

r : 'INNER' ( ID '(' variables ')' )+ ;

q : 'QUERY' ( ID '(' variables ')' )+ ;

u : 'STATE' (ID '->' ( condition )? '/' ( action )? '->' ID)+ ;

condition :
  ID '(' values ')'  #funcCondition
  | expr             #exprCondition
  ;

action :
  ID ':=' expr        #exprAction
  | ID '(' values ')' #funcAction
  ;

variables : ID? (',' ID)* ;

values : expr? (',' expr)* ;

expr :
   MINUS expr                           #unaryMinusExpr
 | NOT expr                             #notExpr
 | expr op=(MULT | DIV) expr      #multiplicationExpr
 | expr op=(PLUS | MINUS) expr          #additiveExpr
 | expr op=(LTEQ | GTEQ | LT | GT) expr #relationalExpr
 | expr op=(EQ | NEQ) expr              #equalityExpr
 | expr AND expr                        #andExpr
 | expr OR expr                         #orExpr
 | ID '(' values ')'                    #func
 | atom                                 #atomExpr
 ;

 atom
  : '(' expr ')'   #parExpr
  | (INT | FLOAT)  #numberAtom
  | (TRUE | FALSE) #booleanAtom
  | ID             #idAtom
  | STRING         #stringAtom
  ;

OR : '||';
AND : '&&';
EQ : '==';
NEQ : '!=';
GT : '>';
LT : '<';
GTEQ : '>=';
LTEQ : '<=';
NOT : '!';
MINUS : '-';
PLUS : '+';
MULT : '*';
DIV : '/';

TRUE : 'True';
FALSE : 'False';


ID
 : [a-zA-Z_] [.a-zA-Z_0-9]*
 ;

INT
 : [0-9]+
 ;

FLOAT
 : [0-9]+ '.' [0-9]*
 | '.' [0-9]+
 ;

STRING
 : '"' (~["\r\n] | '""')* '"'
 ;

SPACE
: [ \t\r\n] -> skip
;
