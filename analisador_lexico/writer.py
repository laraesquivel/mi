import glob
import os
import interfaces

class Writer:
    dir = 'files'

    def __init__(self) -> None:
        self.mode = 'a+'
        self.errors = False
        self.errors_arr = []

    
    def write_clear(self):
        self.errors = False
        self.errors_arr.clear()


        
    def write_all(self, file_name, token_arr):
        output_file_path = os.path.join(Writer.dir, f"{file_name}-saida.txt")

        with open(output_file_path, 'a+', encoding='utf-8') as file:
            for token in token_arr:
                if type(token) == interfaces.Token:
                    text_writer = f'{token.line}    {token.code}    {token.token}\n'
                    file.write(text_writer)
                else:
                    self.errors_arr.append(token)
                    self.errors = True
            
                
    
    def write_errors(self, file_name):
        output_file_path = os.path.join(Writer.dir, f"{file_name}-saida.txt")
        os.makedirs(Writer.dir, exist_ok=True)

        with open(output_file_path, self.mode, encoding='utf-8') as file:
            for token in self.errors_arr:
                text_writer = f'{token.line}    {token.code}    {token.token}\n'
                file.write(text_writer)

'''
    def write(self, token, kind) -> None:
        # Construir o caminho completo para o arquivo de saída
        output_file_path = os.path.join(Writer.dir, f"{self.input_file_name}-saida.txt")

        os.makedirs(Writer.dir, exist_ok=True)

        # Abrir o arquivo para escrita
        with open(output_file_path, 'w', encoding='utf-8') as file:
            # Escrever os tokens no arquivo
            for item in self.token_arr:
                text_writer = f"{item[0]} {item[1]} {item[2]}\n"
                file.write(text_writer)
'''