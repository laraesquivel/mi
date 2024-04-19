from read import Reader
from writer import Writer
from interfaces import ComentarioBlocoAberto
from state_machine import State_Machine
import re
from config import END_COMMENT_BLOCK_PATTER


class Analisador:
    def __init__(self) -> None:
        self.reader = Reader()
        self.writer = None
        self.is_open = False
        self.state_machine = State_Machine()
        self.open_comment = ''
        

        self.file_name = ''
        self.line = ''
        self.line_number = 0
    

    def tokenization(self):
        cmf = ''
        while True:
            try:
                self.file_name, self.line,self.line_number = next(self.reader.read_file())
                print(self.file_name, self.line, self.line_number)
                try:
                    if not self.is_open:  #Sem Comentario Aberto
                        self.state_machine.new_line(self.line,self.line_number)
                        self.state_machine.next_token()
                        writer = Writer(self.state_machine.alltokens,self.file_name)
                        writer.write('a')
                    else: #Comentario Aberto
                        cmf += '\n' + self.line #Já se espera que a cadeia esteja aberta para n fazer mais uma verificacao
                        new_line = re.sub(END_COMMENT_BLOCK_PATTER,self.line)
                        if new_line != self.line:  #Comentario fechou
                            self.state_machine.new_line(new_line,self.line_number)
                            self.state_machine.next_token()
                            writer = Writer(self.state_machine.alltokens,self.file_name)
                            writer.write('a')
                            self.is_open = False
                            
                except ComentarioBlocoAberto:
                    begin_cmf = self.state_machine.get_pop_cmf()
                    writer = Writer(self.state_machine.alltokens,self.file_name)
                    writer.write('a')
                    cmf = cmf + begin_cmf
                    self.is_open = True

            except StopIteration:
                break
           
        if self.is_open:
            writer = Writer([(self.line,'CMF',cmf)],self.file_name)
            writer.write('a')
            
