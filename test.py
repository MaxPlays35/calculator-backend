from helpers import Lexer
from translator import translate

lexer = Lexer()
parsed, error, pos = lexer.parse("3.5*(-1)+(7-3)^2")
print(parsed)
trans = translate(parsed)
print(trans)
