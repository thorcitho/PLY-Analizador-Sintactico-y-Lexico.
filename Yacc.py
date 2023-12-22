import ply.lex as lex
import ply.yacc as yacc

tokens = (
    'INT', 'FLOAT', 'ID', 'NUMBER',
    'SEMICOLON', 'LPAREN', 'RPAREN', 'LBRACKET', 'RBRACKET', 'LBRACE', 'RBRACE',
    'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'MODULO', 'EQUALS', 'LESS_THAN',
    'GREATER_THAN', 'LESS_EQUAL', 'GREATER_EQUAL', 'EQUAL_EQUAL', 'NOT_EQUAL',
    'BREAK', 'TRUE', 'DO', 'WHILE'
)


t_SEMICOLON = r';'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACKET = r'\['
t_RBRACKET = r'\]'
t_LBRACE = r'\{'
t_RBRACE = r'\}'
t_PLUS = r'\+'
t_MINUS = r'-'
t_EQUALS = r'='
t_LESS_THAN = r'<'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_MODULO = r'%'
t_GREATER_THAN = r'>'
t_LESS_EQUAL = r'<='
t_GREATER_EQUAL = r'>='
t_EQUAL_EQUAL = r'=='
t_NOT_EQUAL = r'!='

def t_INT(t):
    r'int'
    return t

def t_FLOAT(t):
    r'float'
    return t

def t_ID(t):
    r'[a-zA-Z_][a-zA-Z0-9_]*'
    reserved = {
        'int': 'INT',
        'float': 'FLOAT',
        'break': 'BREAK',
        'true': 'TRUE',
        'do': 'DO',
        'while': 'WHILE'
    }
    t.type = reserved.get(t.value, 'ID')
    return t

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_ARRAY(t):
    r'float\[([0-9]+)\][a-zA-Z_][a-zA-Z0-9_]*'
    return t


def t_error(t):
    print(f"Caracter ilegal '{t.value[0]}'")
    t.lexer.skip(1)


def p_statements(p):
    '''
    statements : statement SEMICOLON statements
               | statement SEMICOLON
               
    '''
    pass

def p_statement(p):
    '''
    statement : variable_declaration
              | array_declaration
              | while_loop
    '''
    p[0] = p[1]

def p_variable_declaration(p):
    '''
    variable_declaration : INT ID
                         | FLOAT ID
    '''
    print("Declaración de variable:", p[1], p[2])



def p_array_declaration(p):
    '''
    array_declaration : data_type LBRACKET expression RBRACKET ID
                      | ID LBRACKET expression RBRACKET ID
    '''
    print(f"Declaración de array: {p[1]} [{p[3]}] {p[5]}")


def p_while_loop(p):
    '''
    while_loop : WHILE LPAREN TRUE RPAREN LBRACE do_assignment SEMICOLON WHILE LPAREN RPAREN RBRACE
                | WHILE LPAREN TRUE RPAREN LBRACE do_assignment WHILE LPAREN array_declaration RPAREN RBRACE
    '''
    print("While Loop encontrado")

def p_do_assignment(p):
    '''
    do_assignment : DO assignment SEMICOLON while_condition
                  | DO assignment SEMICOLON RBRACE
    '''
    print("Asignación y condición encontradas en do-while")

def p_while_condition(p):
    '''
    while_condition : WHILE LPAREN condition RPAREN
    '''
    print("Condición de bucle while encontrada")

def p_condition(p):
    '''
    condition : expression LESS_THAN expression
              | expression GREATER_THAN expression
              | expression LESS_EQUAL expression
              | expression GREATER_EQUAL expression
              | expression EQUAL_EQUAL expression
              | expression NOT_EQUAL expression
    '''
    print("Condición encontrada")

def p_data_type(p):
    '''
    data_type : INT
              | FLOAT
    '''
    p[0] = p[1]

def p_assignment(p):
    '''
    assignment : ID EQUALS expression
    '''
    print("Asignación encontrada")

def p_expression(p):
    '''
    expression : ID PLUS NUMBER
               | ID MINUS ID
               | ID TIMES ID
               | ID DIVIDE ID
               | ID MODULO ID
               | array_access LESS_THAN ID
               | array_access GREATER_THAN ID
               | array_access LESS_EQUAL ID
               | array_access GREATER_EQUAL ID
               | array_access EQUAL_EQUAL ID
               | array_access NOT_EQUAL ID
               | LPAREN expression RPAREN
               | ID
               | NUMBER
    '''
    print("Expresión encontrada")

def p_array_access(p):
    '''
    array_access : ID LBRACKET expression RBRACKET
                 | ID LBRACKET NUMBER RBRACKET
    '''
    print("Acceso a array encontrado")

def p_error(p):
    if p:
        print(f"Error de sintaxis en el token '{p.value}' en la línea {p.lineno}, posición {p.lexpos}")
    else:
        print("Error de sintaxis en la entrada")

lexer = lex.lex()
parser = yacc.yacc()


def read_code_from_file(filename):
    with open(filename, 'r') as file:
        code = file.read()
    return code

filename = 'cod.txt'
code = read_code_from_file(filename)

lexer = lex.lex()
parser = yacc.yacc()

lexer.input(code)
for tok in lexer:
    print(tok)

try:
    parser.parse(code)
except SyntaxError as e:
    print("Error de sintaxis:", e)
