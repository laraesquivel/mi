'''
Universidade Estadual de Feira de Santana
Autores: Alisson Rodrigues
Lara Esquivel de Brito Santos

09/07/2024

Este é o código principal, para adicionar arquivos, os coloque dentro da pasta files no diretorio principal, favor n confundir com a pasta files
dentro do analisador_lexico. Execute o python neste módulo, os outros módulos possuem importações relativas, n funcionarão isolados
pois este é o arquivo principal
'''


from analisador_lexico.analisador import Analisador
from mi2.analisador_sintatico.analisador_sintatico import AnalisadorSintatico 

a = Analisador()

a.analise()


tokens_arr = a.all_tokens_file

#print(tokens_arr)

for token_group in tokens_arr:
    print('_______________________________________________________________________')
    print('\n')

    a_sintax = AnalisadorSintatico() #Isto é um objeto de uma classe
    a_sintax.token_list = token_group
    a_sintax.proxima_producao()

    print('_______________________________________________________________________')
    print('\n')