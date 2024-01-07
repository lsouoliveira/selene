from io import StringIO
import pytest

from selene.lexer import Lexer, TokenType, UnexpectedCharacter


def test_read_newline():
    text_stream = StringIO("\n")
    lexer = Lexer(stream=text_stream)
    token = lexer.next()

    assert token.type == TokenType.NEWLINE
    assert token.value == "\n"


def test_read_integer():
    text_stream = StringIO("123")
    lexer = Lexer(stream=text_stream)
    token = lexer.next()

    assert token.type == TokenType.INTEGER
    assert token.value == "123"


def test_read_string_with_single_quotes():
    text_stream = StringIO("'abc'")
    lexer = Lexer(stream=text_stream)
    token = lexer.next()

    assert token.type == TokenType.STRING_LITERAL
    assert token.value == "abc"


def test_read_string_with_double_quotes():
    text_stream = StringIO('"abc"')
    lexer = Lexer(stream=text_stream)
    token = lexer.next()

    assert token.type == TokenType.STRING_LITERAL
    assert token.value == "abc"


def test_read_string_with_invalid_format():
    text_stream = StringIO("'abc")
    lexer = Lexer(stream=text_stream)

    pytest.raises(UnexpectedCharacter, lexer.next)


def test_eof():
    text_stream = StringIO("")
    lexer = Lexer(stream=text_stream)
    token = lexer.next()

    assert token.type == TokenType.EOF
    assert token.value == ""


def test_read_identifier():
    identifiers = ["a", "abc", "a1", "a1b2c3", "a1_b2_c3"]
    for identifier in identifiers:
        text_stream = StringIO(identifier)
        lexer = Lexer(stream=text_stream)
        token = lexer.next()

        assert token.type == TokenType.IDENTIFIER
        assert token.value == identifier


def test_invalid_identifier():
    identifiers = ["1a", "1a2b3c", "1a_2b_3c"]

    for identifier in identifiers:
        text_stream = StringIO(identifier)
        lexer = Lexer(stream=text_stream)
        token = lexer.next()

        assert token.type == TokenType.INTEGER


def test_read_assign():
    text_stream = StringIO("=")
    lexer = Lexer(stream=text_stream)
    token = lexer.next()

    assert token.type == TokenType.ASSIGN
    assert token.value == "="


def test_unexpected_character():
    text_stream = StringIO("!")
    lexer = Lexer(stream=text_stream)

    pytest.raises(UnexpectedCharacter, lexer.next)
