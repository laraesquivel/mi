from config import (OP_LOGIC_ONE_CHAR_SET, OP_RELATIONAL_ONE_CHAR_SET, OP_ARITIMETIC_ONE_CHAR_SET,
                    DELIMETER_CHAR_SET, STOP_ERRORS)

class State_Machine:
    def __init__(self,line,line_number) -> None:
        self.line = line
        self.current_char = None
        self.last_token = None
        self.next_char = None
        self.line_number = line_number
        self.pos = 0

        self.alltokens = []

    def number_state(self):
        pass
    def comment_state(self):
        pass
    def op_logic_state(self):
        #LOGIC
        self.next_char = self.line[self.pos + 1] if  self.pos + 1 < len(self.line) else self.line[self.pos]

        if self.current_char == '!':
            self.alltokens.append((self.line_number, 'LOG', self.current_char))
            self.pos+=1

        elif self.current_char == self.next_char and self.pos + 1 <  len(self.line): 
            self.alltokens.append((self.line_number,'LOG', self.current_char + self.next_char))
            self.pos+=2


        else:
            error = True
            error_token = ''
            while error and self.pos < len(self.line):
                #self.pos = self.pos + 1 if self.pos + 1 < len(self.line) else 
                self.current_char += self.line[self.pos] if self.line[self.pos] not in STOP_ERRORS else ''
                print(self.current_char)
                error = True if self.current_char == '' else False
                self.pos = self.pos +1
            self.alltokens.append((self.line_number, 'TMF', self.current_char))



                


    def op_relational_state(self):
        pass
    def op_aritimetic_state(self):
        pass
    def cadeia_state(self):
        pass

    def next_token(self):

        while self.pos < len(self.line):
        

            self.current_char = self.line[self.pos]
            #self.next_char = self.line[self.pos + 1] if len(self.line) < 2 else None

            if self.current_char.isdigit():#NUMERO 
                pass
            
            elif self.current_char == '/': #COMENTARIO
                pass

            elif self.current_char in OP_LOGIC_ONE_CHAR_SET: #OPERADOR_LOGICO
                self.op_logic_state()
            elif self.current_char in OP_RELATIONAL_ONE_CHAR_SET: #OPERADOR RELACIONAL
                pass
            elif self.current_char in OP_ARITIMETIC_ONE_CHAR_SET: #OPERADOR ARITMETICO
                pass
            elif self.current_char == '"': #CADEIRA 
                pass
            elif self.current_char in DELIMETER_CHAR_SET: #Delimitador
                pass
            elif self.current_char.isspace(): #Espaço
                self.pos = self.pos + 1 
            else:  #Palavra Reservada ou Identificador
                pass
            



a = '! || && |&'
b = State_Machine(a,0)
b.next_token()
print(b.alltokens)
                

