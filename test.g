// test.g
?program : stmt+

?stmt: ID | MOD

MOD.99 : "mod"
ID : LETTER (LETTER | DIGIT | "-")*

%import common.LETTER
%import common.DIGIT
%import common.WS
%ignore WS