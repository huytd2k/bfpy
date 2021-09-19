from bfpy.tokenizer import ParseError, Token, tokenizer

import pytest


def test_tokenizer():
    text = "+>[-]"
    tokens = tokenizer(text)

    assert tokens == [
        Token.INCR,
        Token.NEXTPTR,
        Token.OPBR,
        Token.DECR,
        Token.CLSBR,
        Token.END,
    ]

    text = "a+>"
    with pytest.raises(ParseError):
        tokens = tokenizer(text)
