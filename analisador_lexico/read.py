import os
import glob

class Reader:
    dir = 'files'
    def __init__(self) -> None:
        self.arquivos = [file for file in glob.glob('files' + '/*') if not file.endswith('-saida.txt')]
        self.delete_file = [file for file in glob.glob('files' + '/*') if file.endswith('-saida.txt')]

    def delete(self) -> None:
        for file in self.delete_file:
            os.remove(file)
    
    def read_file(self):  #Retorna um arquivo lido por linhas
        for ark in self.arquivos:
            with open(ark, 'r', encoding='utf-8') as file:
                #print(os.path.splitext(os.path.basename(ark))[0])
                yield (os.path.splitext(os.path.basename(ark))[0],file.readlines())
