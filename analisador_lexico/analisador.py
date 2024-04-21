from read import Reader
from writer import Writer
from interfaces import ComentarioBlocoAberto, Token, TokenDefeituoso
from state_machine import State_Machine
import re
from config import END_COMMENT_BLOCK_PATTER

class Analisador:
    def __init__(self) -> None:
        self.reader = Reader()
        self.state_machine = State_Machine()
        self.is_open = False
        self.writer = Writer()
        self.error_comf_line = 0

        self.reader.delete()

    def analise(self):
        for file_name, file in self.reader.read_file():
            print(file_name)
            cmf = ''
            for line_index, line in enumerate(file):

                try:
                    self.state_machine.new_line(line,line_index+1)
                    if not self.is_open: #se n tiver comentario de bloco aberto
                        self.state_machine.next_token()
                        temp_tokens = self.state_machine.alltokens
                        self.writer.write_all(file_name,temp_tokens)

                    else: #Comentario de Bloco Aberto
                        cmf = f'{cmf}\n{line}' #Espera-se que o comentario esteja aberto
                        new_line = re.sub(END_COMMENT_BLOCK_PATTER,'',line)

                        if new_line != line: #Comentario de Bloco Fechou!!!
                            print(line)
                            self.state_machine.new_line(new_line,line_index+1)
                            self.state_machine.next_token()
                            temp_tokens = self.state_machine.alltokens
                            self.writer.write_all(file_name,temp_tokens)
                            cmf=''
                            self.is_open = False
                            self.error_comf_line = 0

                except ComentarioBlocoAberto:
                    self.is_open = True
                    self.error_comf_line = line_index + 1
                    cmf = self.state_machine.alltokens.pop()[2]
                    temp_tokens = self.state_machine.alltokens
                        
                    self.writer.write_all(file_name,temp_tokens)
            if self.is_open:
                comf = TokenDefeituoso(self.error_comf_line, 'CoMF', cmf)
                self.writer.errors_arr.append(comf)
                self.is_open = False

            self.writer.write_errors(file_name)
            self.writer.write_clear(file_name)
                


