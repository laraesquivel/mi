from config import END_COMMENT_BLOCK_PATTER
import re

a = 'asbhashihaiha*/lasa'

resultado = re.sub(END_COMMENT_BLOCK_PATTER, '', a)

print(resultado)