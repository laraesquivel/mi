import os
import glob

class Reader:
    dir = 'files'
    def __init__(self) -> None:
        self.arquivos = [file for file in glob.glob('analisador_lexico/files' + '/*') if not file.endswith('-saida.txt')]
        #self.arquivos = glob.glob(Reader.dir + '/*[^-saida].txt')
#        self.arquivos = glob.glob(Reader.dir + '/*.txt')
        self.counter = 0

    def list_files(self):
        print(self.arquivos)
    
    def read_file(self):
        for ark in self.arquivos:
            with open(ark, 'r', encoding='utf-8') as file:
                self.counter+=1
                yield (os.path.splitext(os.path.basename(ark))[0],file.readlines(),self.counter)
    
r = Reader()
r.list_files()