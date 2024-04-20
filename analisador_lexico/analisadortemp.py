from read import Reader
from writer import Writer
from interfaces import ComentarioBlocoAberto
from state_machine import State_Machine
import re
from config import END_COMMENT_BLOCK_PATTER


class AnalisadorTemp:
    def __init__(self) -> None:
        self.reader = Reader()
        self.writer = None
        self.is_open = False
        self.state_machine = State_Machine()
        self.open_comment = ''
        

        self.file_name = ''
        self.line = ''
        self.line_number = 0
        self.arr = []
    
    def test2(self):
        print(next(self.reader.read_file()))

    def tokenization(self):
        cmf = ''
        c= 0
        while True:
            try:
                c+=1
                self.file_name, self.line,self.line_number = next(self.reader.read_file())
                print(self.file_name, self.line, self.line_number,c)
                try:
                    if not self.is_open:  #Sem Comentario Aberto
                        self.state_machine.new_line(self.line,self.line_number)
                        self.state_machine.next_token()
                        self.arr.append((self.state_machine.alltokens,self.line_number))
                       # writer = Writer(self.state_machine.alltokens,self.file_name)
                        #writer.write()
                    else: #Comentario Aberto
                        cmf += '\n' + self.line #Já se espera que a cadeia esteja aberta para n fazer mais uma verificacao
                        new_line = re.sub(END_COMMENT_BLOCK_PATTER,self.line)
                        if new_line != self.line:  #Comentario fechou
                            self.state_machine.new_line(new_line,self.line_number)
                            self.state_machine.next_token()
                            #writer = Writer(self.state_machine.alltokens,self.file_name)
                            #writer.write()
                            self.arr.append((self.state_machine.alltokens,self.line_number))
                            self.is_open = False
                            
                except ComentarioBlocoAberto:
                    begin_cmf = self.state_machine.get_pop_cmf()
                    #writer = Writer(self.state_machine.alltokens,self.file_name)
                    #writer.write()
                    self.arr.append((self.state_machine.alltokens,self.line_number))
                    cmf = cmf + begin_cmf
                    self.is_open = True

            except StopIteration:
                break
           
        if self.is_open:
            #writer = Writer([(self.line,'CMF',cmf)],self.file_name)
            #writer.write('a')
            self.arr.append((self.line, 'CMF',cmf))
            
