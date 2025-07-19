EPSILON = 'ε'

productions = {
    'programa': [['ComandoLista']],
    
    'ComandoLista': [['Comando', 'ComandoLista'], [EPSILON]],
    
    'Comando': [['Condicional'], ['Repeticao'], ['Funcao_Def'], ['Definicao'], ['Atribuicao']],
    
    'Condicional': [['IF', 'Expressao', 'THEN', 'LCHAVE', 'ComandoLista', 'RCHAVE', 'Else_Lista']],
    
    'Else_Lista': [['ELSE', 'LCHAVE', 'ComandoLista', 'RCHAVE'], [EPSILON]],
    
    'Repeticao': [['WHILE', 'Expressao', 'LCHAVE', 'ComandoLista', 'RCHAVE']],
    
    'Funcao_Def': [['DEF', 'IDENTIFIER', 'LPARENT', 'ComandoLista', 'RPARENT']],
    
    'Definicao': [['tipo', 'IDENTIFIER', 'DELIMITER_LIN']],
    
    'tipo': [['INT'], ['REAL'], ['CHAR']],
    
    'Atribuicao': [['IDENTIFIER', 'ATTRIBUTION', 'Expressao', 'DELIMITER_LIN']],
    
    'Expressao': [['ExpressaoOR']],
    
    'ExpressaoOR': [['ExpressaoAND', 'ExpressaoOULinha']],
    
    'ExpressaoOULinha': [['OR', 'ExpressaoAND', 'ExpressaoOULinha'], [EPSILON]],
    
    'ExpressaoAND': [['ExpressaoNOT', 'ExpressaoANDLinha']],
    
    'ExpressaoANDLinha': [['AND', 'ExpressaoNOT', 'ExpressaoANDLinha'], [EPSILON]],
    
    'ExpressaoNOT': [['NOT', 'ExpressaoNOT'], ['ExpressaoRelacional']],
    
    'ExpressaoRelacional': [['ExpressaoAritmetica', 'ExpressaoRelacionalLinha']],
    
    'ExpressaoRelacionalLinha': [['OPERATOR_COMP', 'ExpressaoAritmetica'], [EPSILON]],
    
    'ExpressaoAritmetica': [['TermoAritmetico', 'ExpressaoAritLinha']],
    
    'ExpressaoAritLinha': [['OPERATOR_ARIT', 'TermoAritmetico', 'ExpressaoAritLinha'], [EPSILON]],
    
    'TermoAritmetico': [['LPARENT', 'ExpressaoRelacional', 'RPARENT'], ['IDENTIFIER'], ['NUMBER'], ['REALNUMBER']]
}

start_symbol = 'programa'

def compute_first(productions):
    first = {nt: set() for nt in productions}
    
    def first_of(symbol):
        if symbol == EPSILON:
            return {EPSILON}
        if symbol not in productions:
            # terminal
            return {symbol}
        result = set()
        for prod in productions[symbol]:
            for sym in prod:
                sym_first = first_of(sym)
                result |= (sym_first - {EPSILON})
                if EPSILON not in sym_first:
                    break
            else:
                result.add(EPSILON)
        return result
    
    for nt in productions:
        first[nt] = first_of(nt)
    return first

def compute_follow(productions, start_symbol, first):
    follow = {nt: set() for nt in productions}
    follow[start_symbol].add('$')  # fim da cadeia
    
    changed = True
    while changed:
        changed = False
        for nt in productions:
            for prod in productions[nt]:
                for i, sym in enumerate(prod):
                    if sym in productions:
                        after = prod[i+1:] if i+1 < len(prod) else []
                        first_of_after = set()
                        if after:
                            for s in after:
                                s_first = first[s] if s in first else {s}
                                first_of_after |= (s_first - {EPSILON})
                                if EPSILON not in s_first:
                                    break
                            else:
                                first_of_after.add(EPSILON)
                        else:
                            first_of_after.add(EPSILON)
                        
                        old = follow[sym].copy()
                        follow[sym] |= (first_of_after - {EPSILON})
                        if EPSILON in first_of_after:
                            follow[sym] |= follow[nt]
                        if old != follow[sym]:
                            changed = True
    return follow

def save_sets_to_file(first, follow, filename='first_follow.txt'):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write("Conjuntos FIRST:\n")
        for nt in sorted(first.keys()):
            f.write(f"{nt}: {{ {', '.join(sorted(first[nt]))} }}\n")
        f.write("\nConjuntos FOLLOW:\n")
        for nt in sorted(follow.keys()):
            f.write(f"{nt}: {{ {', '.join(sorted(follow[nt]))} }}\n")

def is_LL1(productions, first, follow):
    for nt in productions:
        prods = productions[nt]
        sets = []
        for prod in prods:
            prod_first = set()
            for sym in prod:
                sym_first = first[sym] if sym in first else {sym}
                prod_first |= (sym_first - {EPSILON})
                if EPSILON not in sym_first:
                    break
            else:
                prod_first.add(EPSILON)
            sets.append(prod_first)

        # Verifica interseção entre FIRST das produções
        for i in range(len(sets)):
            for j in range(i+1, len(sets)):
                inter = sets[i] & sets[j]
                if inter:
                    print(f"Conflito FIRST- FIRST no não-terminal '{nt}': interseção {inter} entre produções {i+1} e {j+1}")
                    return False
        
        # Se FIRST inclui ε, verificar conflito com FOLLOW
        for idx, s in enumerate(sets):
            if EPSILON in s:
                inter = s & follow[nt]
                if inter:
                    print(f"Conflito FIRST- FOLLOW no não-terminal '{nt}': interseção {inter} na produção {idx+1}")
                    return False
    return True

if __name__ == '__main__':
    first = compute_first(productions)
    follow = compute_follow(productions, start_symbol, first)
    save_sets_to_file(first, follow)

    print("Conjuntos FIRST e FOLLOW salvos em 'first_follow.txt'.")
    print()

    if is_LL1(productions, first, follow):
        print("A gramática É LL(1).")
    else:
        print("A gramática NÃO É LL(1).")


