from . import lexer

## Helper Functions
def strip_whitespacetokens(token_list):
    new_token_list = []
    for token in token_list:
        if type(token) is lexer.WhitespaceToken:
            continue
        new_token_list.append(token)
    return new_token_list


def error_invalid_token(token):
    line, col = token.position_linecol()
    print(f"{__name__} ERROR: unexpected token at line {line} column {col}")



## Recursive Parsing functions
# Data
class ParserData:
    token_list = None # List of whitespace-stripped tokens
    head = 0  # Current location in token list

    @classmethod
    def safeget(cls, idx):
        if not idx < len(cls.token_list):
            return None
        return cls.token_list[idx]



# Functions
def parse_array():
    valid_entry_items = [
        lexer.StringToken, 
        lexer.BooleanToken, 
        lexer.NumberToken
    ]
    
    root = None
    current_tok = ParserData.safeget(ParserData.head)
    if current_tok.value == "[":
        ParserData.head += 1
        root = []
    else:
        error_invalid_token(current_tok)


    #TODO: maybe add mini state machine here?
    while True:
        # Consume value (unless sublist)
        current_tok = ParserData.safeget(ParserData.head)
        if type(current_tok) in valid_entry_items:
            root.append(current_tok.value)
            ParserData.head += 1
        elif current_tok.value == "[":
            #TODO: implement recursion?
            sub_list = parse_array()
            root.append(sub_list)
        elif current_tok.value == "{":
            sub_object = parse_object()
            root.append(sub_object)
        else:
            error_invalid_token(current_tok)
            break

        # Consume comma or End of List
        # Comma is expected after value unless it is the last value
        current_tok = ParserData.safeget(ParserData.head)
        if current_tok.value == ",":
            ParserData.head += 1
        elif current_tok.value == "]":
            ParserData.head += 1
            return root
        else:
            error_invalid_token(current_tok)
            break



def parse_object():
    valid_keys = [
        lexer.StringToken
    ]
    valid_values = [
        lexer.StringToken,
        lexer.NumberToken,
        lexer.BooleanToken
    ]

    root = None
    current_tok = ParserData.safeget(ParserData.head)
    if current_tok.value == "{":
        ParserData.head += 1
        root = {}
    else:
        error_invalid_token(current_tok)


    while True:
        tmp_key = None

        # Consume key
        current_tok = ParserData.safeget(ParserData.head)
        if type(current_tok) in valid_keys:
            tmp_key = current_tok.value
            ParserData.head += 1
        else:
            error_invalid_token(current_tok)
        
        # Consume Separator
        current_tok = ParserData.safeget(ParserData.head)
        if current_tok.value == ":":
            ParserData.head += 1
        else:
            error_invalid_token(current_tok)

        # Consume and append value
        current_tok = ParserData.safeget(ParserData.head)
        if type(current_tok) in valid_values:
            root[tmp_key] = current_tok.value
            ParserData.head += 1
        elif current_tok.value == "[":
            sub_list = parse_array()
            root[tmp_key] = sub_list
        elif current_tok.value == "{":
            sub_obj = parse_object()
            root[tmp_key] = sub_obj
        else:
            error_invalid_token(current_tok)            

        # Consume comma or End of List
        # Comma is expected after value unless it is the last value
        current_tok = ParserData.safeget(ParserData.head)
        if current_tok.value == ",":
            ParserData.head += 1
        elif current_tok.value == "}":
            ParserData.head += 1
            return root
        else:
            error_invalid_token(current_tok)
            break





## Main Parse function
# The analyzer should take the token list to build a 
#   tree-like structure.
# In the case of JSON, this is just the JSON datastructure
#   represented as python dictionaries and lists
def analyze(token_list):
    ParserData.token_list = strip_whitespacetokens(token_list)


    first_token = ParserData.token_list[0]
    if not first_token.value in ["[", "{"]:
        print(f"{__name__} ERROR: First non-whitespace "
            + "character must be '[' or '{'")
        exit()

    parsed_json = None

    if first_token.value == "[": 
        parsed_json = parse_array()
    elif first_token.value == "{": 
        parsed_json = parse_object()
    

    return parsed_json

