OP_LOGIC_ONE_CHAR_SET = set(['!','&', '|'])
OP_RELATIONAL_ONE_CHAR_SET = set(['<','>','='])
OP_ARITIMETIC_ONE_CHAR_SET = set(['+','-','*',"/"])
DELIMETER_CHAR_SET = set(['.', '{' , '}' , ';' , ',' , '(' , ')' ,']','['])

STOP_ERRORS = set(['!','&','|','=','>','<','+','-','*','/','.','{','}',';','(',')',']','[',','])

ASCII = [chr(i) for i in range(32, 127) if i != 34]


REGEX_BLOCK_COMMENT_PATTERN = r'/\*.*?\*/'