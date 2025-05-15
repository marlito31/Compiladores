class SaMInterpreter:

    def __init__(self):
        self.stack = []  # Pilha inicial vazia
        self.program = []  # Código do programa (samcode)
        self.pc = 0  # Contador de programa (inicialmente no início)
        self.fbr = 0  # Contador frame
        self.sp = 0  # Contador de pilha

    def load_program_from_file(self, filename):
        with open(filename, 'r') as file:
            self.program = [
                line.strip() for line in file.readlines() if line.strip()
            ]

    def execute(self):
        while self.pc < len(self.program):
            instr = self.program[self.pc]
            self.pc += 1
            self.process_instruction(instr)

    def process_instruction(self, instruction):
        parts = instruction.split()
        command = parts[0]

        if command == "PUSHIMM":
            if len(parts) < 2:
                print("Erro: Não há argumentos suficientes para a operação PUSHIMM")
                return
            else:
                value = int(parts[1])
                self.stack.append(value)
                self.sp += 1
        elif command == "PUSHIMMC":
            if len(parts) < 2:
                print("Erro: Não há argumentos suficientes para a operação PUSHIMMC")
                return
            else:
                value = ord(parts[1])
                self.stack.append(value)
                self.sp += 1
        elif command == "PUSHIND":
            if len(self.stack) >= 1:
                index = self.stack.pop()
                if 0 <= index < len(self.stack):
                    self.stack.append(self.stack[index])
                else:
                    print("Erro: Índice fora do limite da pilha")
                    return
            else:
                print("Erro: Não há valores suficientes para a operação PUSHIND")
                return
        elif command == "STOREIND":
            if len(self.stack) >= 2:
                value = self.stack.pop()
                index = self.stack.pop()
                self.sp -= 2
                if 0 <= index < len(self.stack):
                    self.stack[index] = value
                else:
                    print("Erro: Índice fora do limite da pilha")
                    return
            else:
                print("Erro: Não há valores suficientes para a operação STOREIND")
                return
        elif command == "ADDSP":
            if int(parts[1]) >= 0:
                value = int(parts[1])
                while value > 0:
                    self.stack.append(None)
                    self.sp += 1
                    value -= 1
            else:
                print("Erro: Não há argumentos suficientes para a operação ADDSP")
                return
        elif command == "PUSHSP":
            self.stack.append(self.sp)
            self.sp += 1
        elif command == "POPSP":
            self.sp = self.stack.pop()         
        elif command == "POP":
            if self.stack:
                self.stack.pop()
                self.sp -= 1
            else:
                print("Erro: Pilha vazia")
                return
        elif command == "ADD":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                self.sp -= 1
            else:
                print("Erro: Não há valores suficientes para a operação ADD")
                return
        elif command == "SUB":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                self.sp -= 1
            else:
                print("Erro: Não há valores suficientes para a operação SUB")
                return
        elif command == "TIMES":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                self.sp -= 1
            else:
                print("Erro: Não há valores suficientes para a operação MUL")
                return
        elif command == "DIV":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if b != 0:
                    self.stack.append(a // b)
                else:
                    print("Erro: Divisão por zero")
                    return
            else:
                print("Erro: Não há valores suficientes para a operação DIV")
                return
        elif command == "MOD":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if b != 0:
                    self.stack.append(a % b)
                else:
                    print("Erro: Divisão por zero")
                    return
        elif command == "NOT":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a == 0:
                    a = 1
                    self.stack.append(a)
                else:
                    a = 0
                    self.stack.append(a)
            else:
                print("Erro: Não há valores suficientes para a operação NOT")
                return        
        elif command == "OR":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if a == 1 or b == 1:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação OR")
                return
        elif command == "AND":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if a == 1 and b == 1:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação AND")
                return
        elif command == "GREATER":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if a > b:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação GREATER")
                return
        elif command == "LESS":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if a < b:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação LESS")
                return
        elif command == "EQUAL":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1   
                if a == b:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação EQUAL")
                return
        elif command == "ISNIL":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a == 0:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação ISNIL")
                return
        elif command == "ISPOS":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a > 0:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação ISPOS")
                return
        elif command == "ISNEG":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a < 0:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação ISNEG")
                return
        elif command == "CMP":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if a == b:
                    self.stack.append(0)
                elif a < b:
                    self.stack.append(-1)
                else:
                    self.stack.append(1)
            else:
                print("Erro: Não há valores suficientes para a operação CMP")
                return
        elif command == "DUP":
            if len(self.stack) >= 1:
                a = self.stack[-1]
                self.stack.append(a)
                self.sp += 1
            else:
                print("Erro: Não há valores suficientes para a operação DUP")
                return
        elif command == "SWAP":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a)
                self.stack.append(b)
            else:
                print("Erro: Não há valores suficientes para a operação SWAP")
                return
        elif command == "PRINT":
            if self.stack:
                print(self.stack[-1])  # Imprime o valor no topo da pilha
            else:
                print("Erro: Pilha vazia")
                return
        elif command == "STOP":
            print("Execução terminada.")
            return
        elif command == "JUMP":
            self.pc = int(
                parts[1]
            ) - 1  # Atualiza o contador de programa para o valor fornecido
        elif command == "JUMPC":
            if self.stack and self.stack[-1] == 1:
                self.pc = int(
                    parts[1]
                ) - 1  # Salta para o rótulo indicado, se o topo da pilha for 1
            else:
                print("Erro: JUMPIF não saltou, topo da pilha não é 1")
                return
        else:
            print(f"Erro: Instrução desconhecida '{command}'")
            return


filename = 'program.sam'
interpreter = SaMInterpreter()
interpreter.load_program_from_file(filename)
interpreter.execute()
