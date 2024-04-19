from config import (OP_LOGIC_ONE_CHAR_SET, OP_RELATIONAL_ONE_CHAR_SET, OP_ARITIMETIC_ONE_CHAR_SET,
                    DELIMETER_CHAR_SET, STOP_ERRORS, ASCII,RESERVED_WORDS)

from interfaces import ComentarioBlocoAberto

class State_Machine:
    def __init__(self,line,line_number) -> None:
        self.line = line
        self.current_char = None
        self.last_token = None
        self.line_number = line_number
        self.pos = 0

        self.alltokens = []

    def number_state(self):
        pass
    def __comment_state(self): #/
        self.pos +=1
        self.current_char = self.line[self.pos] if self.pos < len(self.line) else None

        if self.current_char:
            if self.current_char == '/': #Comentario de linha
                self.pos = float('inf')
            elif self.current_char =='*': #Bloco Coment
                self.pos+= 1
                self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
                
                while self.current_char:
                    self.pos+=1
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
                    next_char = self.line[self.pos + 1] if self.pos + 1 < len(self.line) else None
                    if self.current_char == '*' and next_char=='/': #Comentario de bloco fechou na msm linha
                        self.pos+=2
                        break

                if not self.current_char:
                    raise ComentarioBlocoAberto
        else:
            self.alltokens.append((self.line_number,'ART','/'))


    def __op_logic_state(self):
        #LOGIC
        next_char = self.line[self.pos + 1] if  self.pos + 1 < len(self.line) else ''

        if self.current_char == '!':
            if next_char == '=':
                self.alltokens.append((self.line_number,'REL',self.current_char+next_char)) #Operador Relacional
                self.pos+=2
            else:
                self.alltokens.append((self.line_number, 'LOG', self.current_char)) #Operador Lógico
                self.pos+=1

        elif self.current_char == next_char and self.pos + 1 <  len(self.line): 
            self.alltokens.append((self.line_number,'LOG', self.current_char + next_char))
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

    def __op_relational_state(self):
        possible_token = self.current_char #token que iniciou o estado
        
        self.pos+=1 
        self.current_char = self.line[self.pos] if self.pos < len(self.line) else None
        if self.current_char == '=':
            self.alltokens.append((self.line_number,'REL',possible_token + self.current_char))
            self.pos+=2
        else:
            print(self.current_char)
            self.alltokens.append((self.line_number,'REL',possible_token))
                      
    def __op_aritimetic_state(self):
        possible_token = self.current_char
        if possible_token == '-':
            self.pos+=1
            self.current_char = self.line[self.pos] if self.pos < self.line else ''
            if self.current_char in OP_ARITIMETIC_ONE_CHAR_SET: #Verificando se é ++ ou --
                match(self.current_char):
                    case "-":
                        possible_token+="-"
                        self.alltokens.append((self.line_number,'ART',possible_token))
                    case "+":
                        possible_token+='+'
                        self.alltokens.append((self.line_number,'ART',possible_token))
                    
                    case _:
                        self.alltokens.append((self.line_number,'ART',possible_token))
                        self.pos-=1
            else:
                if self.current_char.isdigit(): #Numero Negativo
                    pass
    

    def __cadeia_state(self):
        cadeia = self.current_char

        cadeia_close = False

        self.pos+=1 #proximo caractere da cadeia
        self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
        cadeia_close = True if self.current_char == '"' else False
        cadeia = cadeia + self.current_char if self.current_char else cadeia
        ascii_invalid = self.current_char not in ASCII and (self.current_char != '"' and self.current_char != '')


        while self.pos <len(self.line) and not cadeia_close:
            if not ascii_invalid:
                self.pos+=1
                self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
                cadeia_close = True if self.current_char == '"' else False
                ascii_invalid = self.current_char not in ASCII and (self.current_char != '"' and self.current_char != '')
                print((self.current_char, ascii_invalid))
                cadeia= cadeia + self.current_char if self.current_char else cadeia
            else:
                while self.pos < len(self.line) and not cadeia_close:
                    self.pos +=1
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
                    if self.current_char == '"':
                        cadeia_close = True

        if cadeia_close and not ascii_invalid:
            self.alltokens.append((self.line_number,'CAC',cadeia))
            self.pos+=1
        
        else:
            self.alltokens.append((self.line_number,'CMF',cadeia))
            self.pos+=1

    # estado para indentificação de números
    def __numbers_state(self):
        numero =self.current_char
        ponto_decimal = False
        fim_numero = False
        numero_Mal_formado= False
        # pega proximo lexema
        self.pos+=1 #proximo caractere do numero
        self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
        # executa o laço até chegar ao fim de linha fim do número ou ponto decimal
        while self.pos <len(self.line) and not fim_numero:
            if not ponto_decimal:
                #se for um digito
                if self.current_char.isdigit():
                    # concatena o numero
                    numero += self.current_char
                    #proximo caractere do numero
                    self.pos+=1 
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
                #se for um ponto decimal
                elif self.current_char == '.' and not numero_Mal_formado:
                    # inicio da parte fracionaria do número
                    print('ponto')
                    ponto_decimal=True
                    numero += self.current_char
                    #proximo caractere do numero
                    self.pos+=1 
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
                # se for um espaço ou delimitador é o fim do número
                elif self.current_char == ' ' or self.current_char in STOP_ERRORS:
                    fim_numero= True
                # se não for um digito
                elif not self.current_char.isdigit():
                    numero_Mal_formado = True

                    numero += self.current_char
                    #proximo caractere do numero
                    self.pos+=1 
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''

                    
            #caso seja a parte decimal
            else:
                #se for um digito
                if self.current_char.isdigit():
                    # concatena o numero
                    numero += self.current_char
                    #proximo caractere do numero
                    self.pos+=1 
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
                # se encontrou o fim do numero
                elif self.current_char == ' ':
                    fim_numero =True
                # caso não seja um digito ou fim do numero ex ['-', ' ','\n']
                elif not self.current_char.isdigit():
                    numero_Mal_formado

        # finalizada a leitura do lexema
        if not numero_Mal_formado:
            self.alltokens.append((self.line_number,'NRO',numero))
        else:
            self.alltokens.append((self.line_number,'NMF',numero))
        print(self.current_char)
    #estado para indentificar identificadores e palavras reservadas
    def __identifier_reserved_word_state(self):
        identificador = self.current_char
        # primeiro verifica se o caractere atual está dentro do intervalo ASCII Utilizado
        ascii_invalid = self.current_char not in ASCII
        identificador_MF = False
        fim_indentificador = False

        if ascii_invalid:
            self.alltokens.append((self.line_number,'TMF',identificador))
        else:
            # se não houver erro de formação no começo percorre todo identificador
            self.pos+=1 #proximo caractere do identificador
            self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
            # percorre até o fim de linha ou fim do identificador
            while self.pos <len(self.line) and not fim_indentificador:
                #verifica se é um dos permitidos
                if self.current_char.isdigit() or self.current_char.isalpha() or self.current_char =='_':
                    identificador+= self.current_char
                    self.pos+=1
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
                # se for um delimitador, fim de linha ou espaço
                elif self.current_char in STOP_ERRORS or self.current_char =='\n' or self.current_char ==' ':
                    #marca o fim do identificador
                    fim_indentificador=True
                # se for qualquer simbolo invalido marca como identificador mal formado
                else:
                    identificador_MF = True
                    #atualiza para proxima posição
                    identificador+= self.current_char
                    self.pos+=1
                    self.current_char = self.line[self.pos] if self.pos < len(self.line) else ''
            # encerrado o laço insere o token equivalente
            if identificador_MF:
                # se houve um simbolo invalido no identificador
                # criar o token do identificador mal formado
                self.alltokens.append((self.line_number,'IMF',identificador))
            else:
                # se é um identificador valido pode ser uma palavra reservada
                if identificador in RESERVED_WORDS:
                    self.alltokens.append((self.line_number,'PRE',identificador))
                else:
                    self.alltokens.append((self.line_number,'IDE',identificador))

    def next_token(self):

        while self.pos < len(self.line):
        
            self.current_char = self.line[self.pos]
            #self.next_char = self.line[self.pos + 1] if len(self.line) < 2 else None

            if self.current_char == '/': #COMENTARIO
                self.__comment_state()

            elif self.current_char in OP_LOGIC_ONE_CHAR_SET: #OPERADOR_LOGICO
                self.__op_logic_state()
 
            elif self.current_char in OP_RELATIONAL_ONE_CHAR_SET: #OPERADOR RELACIONAL
                self.__op_relational_state()

            elif self.current_char in OP_ARITIMETIC_ONE_CHAR_SET: #OPERADOR ARITMETICO
                pass

            elif self.current_char.isdigit():
                self.__numbers_state()
            elif self.current_char == '"': #CADEIRA 
                self.__cadeia_state()

            elif self.current_char in DELIMETER_CHAR_SET: #Delimitador
                pass
            elif self.current_char.isspace(): #Espaço
                self.pos = self.pos + 1 
            else:  #Palavra Reservada ou Identificador
                self.__identifier_reserved_word_state()
                
        
#a = '"alalala" "Ç" "ahsjhaiosjoa" <<<<<<<<<<<<<<<<<<< "auhhbdahbdbhia" "2423982u3'
a= '4aksksaksaakjkajakjjs5>a'
b = State_Machine(a,0)
b.next_token()
print(b.alltokens)
print("Ç"not in ASCII)