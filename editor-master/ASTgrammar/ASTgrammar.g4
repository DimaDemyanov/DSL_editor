grammar ASTgrammar;
    t : '(' n (l t )* ')';
    n : '[' txt  (c )* ']';
    l : '<' txt  (c )* '>';
    c : '{' txt '=' txt '}';
    txt : SYMBOL ( SYMBOL)*;
    SPACE: [ \t\r\n] -> skip;
    SYMBOL: ~( '(' | ')' | '[' | ']' | '<' | '>' | '{' | '}' );