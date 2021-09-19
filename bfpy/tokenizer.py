from enum import Enum
from typing import List


class Token(Enum):
    NEXTPTR = ">"
    PREPTR = "<"
    INCR = "+"
    DECR = "-"
    EVAL = "."
    READ = ","
    OPBR = "["
    CLSBR = "]"
    END = "END"


def tokenizer(text: str) -> List[Token]:
    text = "".join(text.split())

    def token(char):
        try:
            return Token(char)
        except ValueError as e:
            raise ParseError(e)

    tokens = list(map(token, text))
    if tokens[-1] != Token.END:
        tokens.append(Token.END)
    return tokens


class ParseError(Exception):
    pass
