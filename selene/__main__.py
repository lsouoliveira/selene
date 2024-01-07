import argparse
from selene.lexer import Lexer, TokenType


def build_parser():
    argparser = argparse.ArgumentParser(
        prog="Selene", description="Selene command line tool"
    )

    argparser.add_argument("filename", help="Input file")
    argparser.add_argument("--version", action="version", version="%(prog)s 0.1.0")
    argparser.add_argument(
        "--lexer", action="store_true", help="Run lexer on input file"
    )

    return argparser


def tokenize(filename):
    with open(filename, "r") as f:
        lexer = Lexer(f)
        token = lexer.next()
        while token.type != TokenType.EOF:
            print(token)
            token = lexer.next()


def main():
    parser = build_parser()

    args = parser.parse_args()

    if args.lexer:
        tokenize(args.filename)


if __name__ == "__main__":
    main()
