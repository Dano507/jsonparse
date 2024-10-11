from . import lexer
from . import analyzer




# parse() should return a dictionary-ified json
def parse(json_string):
    print("lexer starting...")
    token_list = lexer.lex(json_string)
    print("lexer finished!")

    print("analyzer starting...")
    syntax_tree = analyzer.analyze(token_list)
    print("analyzer finished!")

    return syntax_tree

