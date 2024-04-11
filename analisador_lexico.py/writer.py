import os


class Writer:
    dir = 'files'
    def __init__(self,token_arr,input_file_name) -> None:
        self.token_arr = token_arr
        self.input_file_name = input_file_name
    
    def write(self) -> None:
        with open(f'{Writer.dir}/{self.input_file_name}-saida.txt','w',encoding='utf-8') as file:
            for item in self.token_arr:
                text_writer = f"{(item[0])}  %  Linha {item[1]} \n"
                file.write(text_writer)