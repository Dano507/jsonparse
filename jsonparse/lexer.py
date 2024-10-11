import time


## Helper Functions
# jsonstring "interface"
# Enables auto range checking when accessing jsonstring
class safeinterface:
    jsonstring = None
    head = 0
    line_number = 1
    last_newline_position = 0

    @classmethod
    def safeget(cls, idx):        
        # Check for jsonstring
        if cls.jsonstring is None:
            print("ERROR: no jsonstring defined in class")
            exit()

        # Actual function
        if not idx < len(cls.jsonstring):
            return None
        return cls.jsonstring[idx]

    # Same as get, but automatically sums "head" with "idx" (offset, in this case)
    # Should return None if not head < len(jsonstring)
    @classmethod
    def relativeget(cls, offset, amount=1):       
        letters = []
        for count in range(amount):
            char = cls.safeget(cls.head + offset + count)
            if not type(char) is str: continue
            letters.append(char)

        
        out_str = "".join(letters)
        if len(out_str) == 0: 
            return None
        return out_str

    @classmethod
    def relativestrcmp(cls, tocmp):
        length = len(tocmp)
        count = 0
        while count < length:
            if not cls.relativeget(count) == tocmp[count]:
                return False
            count += 1
        return True

    @classmethod
    def advancehead(cls, amount):
        cls.head += amount

    @classmethod
    def position_to_lineandcol(cls, position):
        line = 1
        last_newline = 0
        head = 0

        while head < len(cls.jsonstring) and head < position:
            current_char = cls.safeget(head)
            if current_char == "\n":
                line += 1
                last_newline = head
            head += 1

        column = head - last_newline
        return (line, column)



def is_number_literal(char):
    if not type(char) is str:
        return None

    charcode = ord(char)
    return charcode >= 48 and charcode <= 57



## Abstract BaseToken  Class
class TokenBase:
    def __init__(self, value):
        self.value = value
        self.position = safeinterface.head

    # get position in lines and columns
    def position_linecol(self):
        return safeinterface.position_to_lineandcol(self.position)
        

    # return length of token, or 0 if no match
    @staticmethod
    def check(jsonstring, head):
        pass

    def __repr__(self):
        return f"<{self.__class__.__name__} '{self.value}'>"


## Real Token Classes
class WhitespaceToken(TokenBase):
    def __init__(self, value):
        super().__init__(value)
    
    @staticmethod
    def check():
        valid_values = [' ', '\t', '\n']

        length = 0
        while True:
            current_char = safeinterface.relativeget(length)
            if not current_char in valid_values:
                return length
            length += 1


class SeparatorToken(TokenBase):
    def __init__(self, value):
        super().__init__(value)
  
    @staticmethod
    def check():
        head = safeinterface.head
        valid_values = ['{', '}', '[', ']']

        current_char = safeinterface.relativeget(0)
        if current_char in valid_values:
            return 1
        else:
            return 0


class InlineSeparatorToken(TokenBase):
    def __init__(self, value):
        super().__init__(value)
  
    @staticmethod
    def check():
        valid_values = [':', ',']

        current_char = safeinterface.relativeget(0)
        if current_char in valid_values:
            return 1
        else:
            return 0


# DATATYPES
# Could be a name, or a string value. They are written the same way
class StringToken(TokenBase):
    def __init__(self, value):
        if len(value) < 2:
            print(f"{__name__} ERROR: value '{value}' to small to be a string")
            exit()
        
        new_value = value[1:-1]

        super().__init__(new_value)

    @staticmethod
    def check():
        valid_string_wrapper = '"'
        length = 0

        if safeinterface.relativeget(length) != valid_string_wrapper:
            return length

        length += 1
        while True:
            current_char = safeinterface.relativeget(length)
            length += 1

            if current_char == valid_string_wrapper:
                return length
            elif current_char is None:
                line, col = safeinterface.position_to_lineandcol(safeinterface.head)
                print(
                    f"{__name__} ERROR: Unterminated string at " \
                    + f"line {line} column {col}"
                )
                exit()
            else:
                continue


class NumberToken(TokenBase):
    def __init__(self, value):
        new_value = None
        if value.count(".") > 0: new_value = float(value)
        else: new_value = int(value)

        super().__init__(new_value)

    @staticmethod
    def check():
        current_char = safeinterface.relativeget(0)
        length = 0


        while True:
            current_char = safeinterface.relativeget(length)

            if not (is_number_literal(current_char) 
                or current_char == "."
            ):
                return length

            length += 1


class BooleanToken(TokenBase):
    def __init__(self, value):
        new_value = None
        if value == "true": new_value = True
        elif value == "false": new_value = False
        else:
            print(f"{__name__} ERROR: invalid boolean token instantiated")

        super().__init__(new_value)

    @staticmethod
    def check():
        valid_values = ["true", "false"]

        length = 0
        for word in valid_values:
            if safeinterface.relativestrcmp(word):
                length = len(word)
        return length




## Export functions
token_types = {
    WhitespaceToken,
    SeparatorToken,
    InlineSeparatorToken,
    StringToken,
    NumberToken,
    BooleanToken,
}
def lex(jsonstring):
    safeinterface.jsonstring = jsonstring
    safeinterface.head = 0

    tokens = []
    # Start Lexer Loop
    while safeinterface.head < len(jsonstring):
        #time.sleep(0.1)
        #print("loop iter", safeinterface.head)  # Debug Stuff
        
        length = 0

        for tok_class in token_types:
            length = tok_class.check()
            if length > 0:
                new_token = tok_class(safeinterface.relativeget(0, length))
                tokens.append(new_token)
                safeinterface.head += length
                break
        
        match_not_found = length == 0
        if match_not_found: 
            #safeinterface.head += 1
            line, col = safeinterface.position_to_lineandcol(safeinterface.head)
            print(__name__, f"ERROR: invalid syntax at line {line} col {col}")
            exit()


    return tokens
