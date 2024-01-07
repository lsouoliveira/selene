from enum import Enum, auto
from dataclasses import dataclass
from io import IOBase


class TokenType(Enum):
    INTEGER = auto()
    EOF = auto()
    STRING_LITERAL = auto()
    IDENTIFIER = auto()
    ASSIGN = auto()
    NEWLINE = auto()
    PLUS = auto()


OPERATORS = {
    "+": TokenType.PLUS,
}


@dataclass
class Token:
    type: TokenType
    value: str


class UnexpectedCharacter(Exception):
    def __init__(self, position: int, char: str):
        self.position = position
        self.char = char

    def __str__(self):
        return "Unexpected character {} at position {}".format(self.char, self.position)


class Lexer:
    def __init__(self, stream: IOBase):
        self.stream = stream
        self.cursor = 0

    def next(self) -> Token:
        while self._iswhitespace(self.cursor):
            self._increment_cursor()

        if self._isnewline(self.cursor):
            return Token(TokenType.NEWLINE, value=self._read_character())

        if self._peek(self.cursor) in OPERATORS:
            return Token(TokenType.PLUS, value=self._read_character())

        if self._iseof(self.cursor):
            return Token(TokenType.EOF, value="")

        if self._isstring(self.cursor):
            return self._read_string()

        if self._isinteger(self.cursor):
            return self._read_integer()

        if self._isidentifier(self.cursor):
            return self._read_identifier()

        if self._isassign(self.cursor):
            return Token(TokenType.ASSIGN, value=self._read_character())

        raise UnexpectedCharacter(self.cursor, self._peek(self.cursor))

    def _iswhitespace(self, cursor) -> bool:
        return self._peek(cursor) == " "

    def _isstring(self, cursor) -> bool:
        index = cursor

        if self._peek(index) in ["'", '"']:
            index += 1

        while not self._iseof(index) and self._peek(index) not in ["'", '"']:
            index += 1

        return self._peek(index) in ["'", '"']

    def _isidentifier(self, cursor) -> bool:
        return self._peek(cursor).isalpha() or (
            self._peek(cursor) == "_" and self._peek(cursor + 1).isalpha()
        )

    def _isinteger(self, cursor) -> bool:
        return self._peek(cursor).isdigit()

    def _isassign(self, cursor) -> bool:
        return self._peek(cursor) == "="

    def _isnewline(self, cursor) -> bool:
        return self._peek(cursor) == "\n"

    def _peek(self, position: int) -> str:
        self.stream.seek(position)
        return self.stream.read(1)

    def _increment_cursor(self):
        self.cursor += 1

    def _read_character(self) -> str:
        self.stream.seek(self.cursor)
        self._increment_cursor()
        return self.stream.read(1)

    def _iseof(self, cursor) -> bool:
        return self._peek(cursor) == ""

    def _read_integer(self) -> Token:
        value = ""

        while not self._iseof(self.cursor) and self._isinteger(self.cursor):
            value += self._read_character()

        return Token(TokenType.INTEGER, value)

    def _read_string(self) -> Token:
        value = ""
        quote = self._read_character()

        while self._peek(self.cursor) != quote:
            value += self._read_character()

        self._read_character()

        return Token(TokenType.STRING_LITERAL, value)

    def _read_identifier(self) -> Token:
        value = self._read_character()

        while not self._iseof(self.cursor) and (
            self._peek(self.cursor).isalnum() or self._peek(self.cursor) == "_"
        ):
            value += self._read_character()

        return Token(TokenType.IDENTIFIER, value)
