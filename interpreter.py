import re

class SaMInterpreter:

    def __init__(self):
        self.stack = []  # Pilha inicial vazia
        self.program = []  # Código do programa (samcode)
        self.pc = 0  # Contador de programa (inicialmente no início)
        self.fbr = 0  # Contador frame
        self.sp = 0  # Contador de pilha
        self.memory = {}  # Memória para strings
        self.address = "A"  # Endereço de memória para strings

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
    
    def is_hexadecimal(self,s):
        try:
            int(s, 16)
            return True
        except (ValueError, TypeError):
            return False

    def process_instruction(self, instruction):
        parts = instruction.split()
        command = parts[0]

        if command == "PUSHIMM":
            if len(parts) < 2:
                print("Erro: Não há argumentos suficientes para a operação PUSHIMM")
                exit()
            else:
                value = int(parts[1])
                self.stack.append(value)
                self.sp += 1
        elif command == "PUSHIMMF":
            if len(parts) < 2:
                print("Erro: Não há argumentos suficientes para a operação PUSHIMMF")
                exit()
            else:
                value = float(parts[1])
                self.stack.append(value)
                self.sp += 1
        elif command == "PUSHIMMC":
            if len(parts) < 2:
                print("Erro: Não há argumentos suficientes para a operação PUSHIMMC")
                exit()
            else:
                value = ord(parts[1])
                self.stack.append(value)
                self.sp += 1
        elif command == "PUSHIMMSTR":
            if len(parts) < 2:
                print("Erro: Não há argumentos suficientes para a operação PUSHIMMSTR")
                exit()
            else:
                value = " ".join(parts[1:])
                match = re.match(r'"(.*?)"', value)
                if match:
                    string_value = match.group(1)
                    self.memory[self.address] = string_value
                    self.stack.append(self.address)
                    self.sp += 1
                    self.address = hex(int(self.address, 16) + 1)
                else:
                    print("Erro: Formato de string inválido")
                    exit()
        elif command == "PUSHIND":
            if len(self.stack) >= 1:
                index = self.stack.pop()
                if 0 <= index < len(self.stack):
                    self.stack.append(self.stack[index])
                else:
                    print("Erro: Índice fora do limite da pilha")
                    exit()
            else:
                print("Erro: Não há valores suficientes para a operação PUSHIND")
                exit()
        elif command == "STOREIND":
            if len(self.stack) >= 2:
                value = self.stack.pop()
                index = self.stack.pop()
                self.sp -= 2
                if 0 <= index < len(self.stack):
                    self.stack[index] = value
                else:
                    print("Erro: Índice fora do limite da pilha")
                    exit()
            else:
                print("Erro: Não há valores suficientes para a operação STOREIND")
                exit()
        elif command == "ADDSP":
            if int(parts[1]) >= 0 and len(parts) == 2:
                value = int(parts[1])
                while value > 0:
                    self.stack.append(None)
                    self.sp += 1
                    value -= 1
            else:
                print("Erro: Não há argumentos suficientes para a operação ADDSP")
                exit()
        elif command == "PUSHSP":
            if len(parts) == 1:
                self.stack.append(self.sp)
                self.sp += 1
            else:
                print("Erro")
                exit()
        elif command == "POPSP":
            self.sp = self.stack.pop()         
        elif command == "POP":
            if self.stack:
                self.stack.pop()
                self.sp -= 1
            else:
                print("Erro: Pilha vazia")
                exit()
        elif command == "PUSHOFF":
            if len(parts) == 2 and isinstance(parts[1],int):
                aux = self.fbr + int(parts[1])
                self.stack[self.sp] = self.stack[aux]
                self.sp += 1
            else:
                print("Erro")
                exit()
        elif command == "STOREOFF":
            if len(parts) == 2 and isinstance(parts[1],int):
                num = self.stack.pop()
                self.stack[self.fbr + int(parts[1])] = num
                self.sp -= 1
            else:
                print("Erro")
                exit()
        elif command == "PUSHFBR":
            if len(parts) == 1:
                self.stack.append(self.fbr)
                self.sp += 1
            else:
                print("Erro")
                exit()
        elif command == "POPFBR":
            if len(parts) == 1:
                self.fbr = self.stack.pop()
                self.sp -= 1
            else:
                print("Erro")
                exit()
        elif command == "LINK":
            if len(parts) == 1:
                self.stack.append(self.fbr)
                self.sp += 1
                self.fbr = self.sp - 1
            else:
                print("Erro")
                exit()
        elif command == "MALLOC":
            if len(self.stack) >= 1 and isinstance(self.stack[self.sp - 1], int):
                num = self.stack.pop() + 1
                array = [None] * num
                self.memory[self.address] = array
                self.address = hex(int(self.address, 16) + 1)
                self.sp -= 1
            else:
                print("Erro: Tamanho inválido para alocação")
                exit()
        elif command == "ADD":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a + b)
                self.sp -= 1
            else:
                print("Erro: Não há valores suficientes para a operação ADD")
                exit()
        elif command == "SUB":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a - b)
                self.sp -= 1
            else:
                print("Erro: Não há valores suficientes para a operação SUB")
                exit()
        elif command == "TIMES":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.stack.append(a * b)
                self.sp -= 1
            else:
                print("Erro: Não há valores suficientes para a operação MUL")
                exit()
        elif command == "DIV":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if b != 0:
                    self.stack.append(a // b)
                else:
                    print("Erro: Divisão por zero")
                    exit()
            else:
                print("Erro: Não há valores suficientes para a operação DIV")
                exit()
        elif command == "MOD":
            if len(self.stack) >= 2:
                b = self.stack.pop()
                a = self.stack.pop()
                self.sp -= 1
                if b != 0:
                    self.stack.append(a % b)
                else:
                    print("Erro: Divisão por zero")
                    exit()
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
                exit()        
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
                exit()
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
                exit()
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
                exit()
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
                exit()
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
                exit()
        elif command == "ISNIL":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a == 0:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação ISNIL")
                exit()
        elif command == "ISPOS":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a > 0:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação ISPOS")
                exit()
        elif command == "ISNEG":
            if len(self.stack) >= 1:
                a = self.stack.pop()
                if a < 0:
                    self.stack.append(1)
                else:
                    self.stack.append(0)
            else:
                print("Erro: Não há valores suficientes para a operação ISNEG")
                exit()
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
                exit()
        elif command == "DUP":
            if len(self.stack) >= 1:
                a = self.stack[-1]
                self.stack.append(a)
                self.sp += 1
            else:
                print("Erro: Não há valores suficientes para a operação DUP")
                exit()
        elif command == "SWAP":
            if len(self.stack) >= 2:
                a = self.stack.pop()
                b = self.stack.pop()
                self.stack.append(a)
                self.stack.append(b)
            else:
                print("Erro: Não há valores suficientes para a operação SWAP")
                exit()
        elif command == "WRITE":
            if self.stack and isinstance(self.stack[-1], int):
                print(self.stack[-1])  # Imprime o valor no topo da pilha
            else:
                print("Erro: Pilha vazia ou valor não é inteiro")
                exit()
        elif command == "WRITESTR":
            aux = self.stack[self.sp-1];
            if self.is_hexadecimal(aux):
                address = self.stack.pop()
                self.sp -= 1
                if address in self.memory:
                    print(self.memory[address])
                else:
                    print("Erro: Endereço de memória inválido")
                    exit()
            else:
                print("Erro: O valor no topo da pilha não é um endereço de memória")
                exit()
        elif command == "STOP":
            print("Execução terminada.")
            exit()
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
                exit()
        else:
            print(f"Erro: Instrução desconhecida '{command}'")
            exit()


filename = 'program.sam'
interpreter = SaMInterpreter()
interpreter.load_program_from_file(filename)
interpreter.execute()
