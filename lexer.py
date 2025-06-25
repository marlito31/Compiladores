import re

keywords = {
    'Se':'IF',
    'Então':'THEN',
    'Senao':'ELIF',
    'Enquanto':'WHILE',
    'E':'AND',
    'Ou':'OR',
    'Nao':'NOT',
    'Caractere':'CHAR',
    'Definição':'DEF',
    'Inteiro':'INT',
    'Real':'REAL'
}

Token_types = [
    ('REALNUMBER', r'\b\d+\b\.\d+\b'),
    ('NUMBER',     r'\b\d+\b'),
    ('IDENTIFIER', r'\b[a-zA-Z_]\w*\b'),
    ('ATTRIBUTION', r'<-'),
    ('OPERATOR',   r'(>=|<=|==|!=|>|<|[\+\-\*/=])'),
    ('DELIMITER',  r'[(){};,]'),
    ('WHITESPACE', r'[ \t]+'),
    ('NEWLINE',    r'\n'),
    ('UNKNOWN',    r'.')  # qualquer outro caractere

]

token_regex = '|'.join(f'(?P<{nome}>{pattern})' for nome, pattern in Token_types)
compiled_regex = re.compile(token_regex)

def lexer(source_code):

    tokens = []
    line_number = 1
    col_number = 1

    for match in compiled_regex.finditer(source_code):
        token_type = match.lastgroup
        lexeme = match.group(token_type)

        # Atualiza posição antes de tratar o token
        start_col = col_number
        col_number += len(lexeme)

        if token_type == 'NEWLINE':
            line_number += 1
            col_number = 1
            continue
        elif token_type == 'WHITESPACE':
            continue
        elif token_type == 'UNKNOWN':
            print(f"[Erro léxico] Caractere inválido '{lexeme}' na linha {line_num}, coluna {start_col}")
            continue

        # Se for IDENTIFIER, verificar se é palavra-chave
        if token_type == 'IDENTIFIER' and lexeme in keywords:
            token_type = keywords[lexeme]

        tokens.append({
            'type': token_type,
            'value': lexeme,
            'line': line_number,
            'column': start_col
        })

    return tokens

def read_file(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()

source_code = read_file('teste.ptbr')

tokens = lexer(source_code)

for token in tokens:
    print(token)