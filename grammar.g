program : stmt+

?stmt : exp
    | def_stmt
    | print_stmt

?print_stmt : "(" "print-num" exp ")"   -> print_num
    | "(" "print-bool" exp ")"          -> print_bool

?exp : BOOL_VAL
    | SIGNED_INT
    | variable
    | num_op
    | logical_op
    | fun_exp
    | fun_call
    | if_exp

?num_op : plus | minus | multiply | divide | modulus | greater | smaller | equal
?plus     : "(" "+" exp exp+ ")"
?minus    : "(" "-" exp exp ")"
?multiply : "(" "*" exp exp+ ")"
?divide   : "(" "/" exp exp ")"
?modulus  : "(" "mod" exp exp ")"
?greater  : "(" ">" exp exp ")"
?smaller  : "(" "<" exp exp ")"
?equal    : "(" "=" exp exp+ ")"

?logical_op : and_op | or_op | not_op
?and_op : "(" "and" exp exp+ ")"
?or_op  : "(" "or" exp exp+ ")"
not_op : "(" "not" exp ")"

?def_stmt : "(" "define" variable exp ")"
?variable : ID

?fun_exp : "(" "fun" fun_ids fun_body ")"
fun_ids  : "(" ID* ")"
?fun_body : exp
fun_call : "(" fun_exp param* ")"
    | "(" fun_name param* ")"
?param    : exp
?fun_name : ID

?if_exp : "(" "if" test_exp than_exp else_exp ")"
?test_exp : exp
?than_exp : exp
?else_exp : exp

ID : LETTER (LETTER | DIGIT | "-")*
BOOL_VAL : "#t" | "#f"

%import common.SIGNED_INT
%import common.LETTER
%import common.DIGIT
%import common.WS
%ignore WS