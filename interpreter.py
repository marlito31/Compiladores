class SaMInterpreter:
   def __init__(self):
       self.stack = []  # Pilha inicial vazia
       self.program = []  # Código do programa (samcode)
       self.pc = 0  # Contador de programa (inicialmente no início)


   def load_program_from_file(self, filename):
       with open(filename, 'r') as file:
           self.program = [line.strip() for line in file.readlines() if line.strip()]
          




   def execute(self):
       while self.pc < len(self.program):
           instr = self.program[self.pc]
           self.pc += 1
           self.process_instruction(instr)
      


   def process_instruction(self, instruction):
       parts = instruction.split()
       command = parts[0]


       if command == "PUSH":
           value = int(parts[1])
           self.stack.append(value)
       elif command == "POP":
           if self.stack:
               self.stack.pop()
           else:
               print("Erro: Pilha vazia")
       elif command == "ADD":
           if len(self.stack) >= 2:
               b = self.stack.pop()
               a = self.stack.pop()
               self.stack.append(a + b)
           else:
               print("Erro: Não há valores suficientes para a operação ADD")
       elif command == "SUB":
           if len(self.stack) >= 2:
               b = self.stack.pop()
               a = self.stack.pop()
               self.stack.append(a - b)
           else:
               print("Erro: Não há valores suficientes para a operação SUB")
       elif command == "TIMES":
           if len(self.stack) >= 2:
               b = self.stack.pop()
               a = self.stack.pop()
               self.stack.append(a * b)
           else:
               print("Erro: Não há valores suficientes para a operação MUL")
       elif command == "DIV":
           if len(self.stack) >= 2:
               b = self.stack.pop()
               a = self.stack.pop()
               if b != 0:
                   self.stack.append(a // b)
               else:
                   print("Erro: Divisão por zero")
           else:
               print("Erro: Não há valores suficientes para a operação DIV")
       elif command == "MOD":
           if len(self.stack) >= 2:
               b = self.stack.pop()
               a = self.stack.pop()
               if b != 0:
                   self.stack.append(a % b)
               else:
                   print("Erro: Divisão por zero")
       elif command == "PRINT":
           if self.stack:
               print(self.stack[-1])  # Imprime o valor no topo da pilha
           else:
               print("Erro: Pilha vazia")
       elif command == "STOP":
           print("Execução terminada.")
           return
       elif command == "JUMP":
           self.pc = int(parts[1]) - 1  # Atualiza o contador de programa para o valor fornecido
       elif command == "JUMPIF":
           if self.stack and self.stack[-1] == 1:
               self.pc = int(parts[1]) - 1  # Salta para o rótulo indicado, se o topo da pilha for 1
           else:
               print("Erro: JUMPIF não saltou, topo da pilha não é 1")




filename = 'program.sam'
interpreter = SaMInterpreter()
interpreter.load_program_from_file(filename)
interpreter.execute()





