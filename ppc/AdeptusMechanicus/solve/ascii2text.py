import string
from art import text2art

#генерируем массив всех возможных букв / цифр / знаков
all_possible_chars = string.ascii_letters + string.digits + string.punctuation

#составляем словарь, где каждому символу соотносится ascii-арт
ascii_chars = {}
for char in all_possible_chars:
    ascii_char = text2art(char)
    ascii_chars["".join(ascii_char.replace('\n',''))] = char

def ascii2text(input):
    return ascii_chars.get(input, "")

#ascii_input = text2art("{")
#print(ascii_input)

ascii_input = r"""
   __
  / /
 | | 
< <  
 | | 
  \_\

"""
#print(text2art("{").replace('\n', ''))
#print(ascii_input.replace('\n',''))
print(ascii2text("".join(ascii_input.replace('\n', ''))))
    