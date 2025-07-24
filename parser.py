import ast

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.pos = 0

    def lookahead(self):
        return self.tokens[self.pos][0]

    def match(self, expected):
        if self.lookahead() == expected:
            self.pos += 1
        else:
            raise SyntaxError(f"Esperado {expected}, encontrado {self.lookahead()}")

    
    def programa(self):
        self.comando_lista()

    
    def comando_lista(self):
        if self.lookahead() in ['IF', 'WHILE', 'DEF', 'INT', 'REAL', 'CHAR', 'IDENTIFIER']:
            self.comando()
            self.comando_lista()
        # senão ε (vazio)

    
    def comando(self):
        aux = self.lookahead()
        if aux == 'IF':
            self.condicional()
        elif aux == 'WHILE':
            self.repeticao()
        elif aux == 'DEF':
            self.funcao_def()
        elif aux in ['INT', 'REAL', 'CHAR']:
            self.definicao()
        elif aux == 'IDENTIFIER':
            self.atribuicao()
        else:
            raise SyntaxError(f"Comando inesperado: {aux}")

    def definicao(self):
        self.tipo()
        self.match('IDENTIFIER')
        self.match('DELIMITER_LIN')

    def tipo(self):
        if self.lookahead() in ['INT', 'REAL', 'CHAR']:
            self.match(self.lookahead())
        else:
            raise SyntaxError("Tipo esperado")

    def atribuicao(self):
        self.match('IDENTIFIER')
        self.match('ATTRIBUTION')
        self.expressao()
        self.match('DELIMITER_LIN')

    # Expressao → ExpressaoOR
    def expressao(self):
        self.expressao_or()

    def expressao_or(self):
        self.expressao_and()
        while self.lookahead() == 'OR':
            self.match('OR')
            self.expressao_and()

    def expressao_and(self):
        self.expressao_not()
        while self.lookahead() == 'AND':
            self.match('AND')
            self.expressao_not()

    def expressao_not(self):
        if self.lookahead() == 'NOT':
            self.match('NOT')
            self.expressao_not()
        else:
            self.expressao_relacional()

    def expressao_relacional(self):
        self.expressao_aritmetica()
        if self.lookahead() == 'OPERATOR_COMP':
            self.match('OPERATOR_COMP')
            self.expressao_aritmetica()

    def expressao_aritmetica(self):
        self.termo_aritmetico()
        while self.lookahead() == 'OPERATOR_ARIT':
            self.match('OPERATOR_ARIT')
            self.termo_aritmetico()

    def termo_aritmetico(self):
        if self.lookahead() == 'LPARENT':
            self.match('LPARENT')
            self.expressao()
            self.match('RPARENT')
        elif self.lookahead() == 'IDENTIFIER':
            self.match('IDENTIFIER')
        elif self.lookahead() == 'NUMBER':
            self.match('NUMBER')
        elif self.lookahead() == 'REALNUMBER':
            self.match('REALNUMBER')
        else:
            raise SyntaxError("Expressão aritmética inválida")
        
    def condicional(self):
        self.match('IF')
        self.expressao()
        self.match('THEN')
        self.match('LCHAVE')
        self.comando_lista()
        self.match('RCHAVE')
        self.else_lista()

    def else_lista(self):
        if self.lookahead() == 'ELSE':
            self.match('ELSE')
            self.match('LCHAVE')
            self.comando_lista()
            self.match('RCHAVE')

    def repeticao(self):
        self.match('WHILE')
        self.expressao()
        self.match('LCHAVE')
        self.comando_lista()
        self.match('RCHAVE')

    def funcao_def(self):
        self.match('DEF')
        self.match('IDENTIFIER')
        self.match('LPARENT')
        self.comando_lista()
        self.match('RPARENT')


def read_tokens(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        tokens = ast.literal_eval(f.read())
    #print(tokens) 
    return tokens

tokens = read_tokens("tokens.txt")
parser = Parser(tokens)
parser.programa()
print("Código válido!")
