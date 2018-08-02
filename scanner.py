import re
import sys

class Scanner:
    '''The interface comprises the methods lookahead and consume.
       Other methods should not be called from outside of this class.'''

    def __init__(self, input_file):
        '''Reads the whole input_file to input_string, which remains constant.
           current_char_index counts how many characters of input_string have
           been consumed.
           current_token holds the most recently found token and the
           corresponding part of input_string.'''
        # source code of the program to be compiled
        self.input_string = input_file.read()
        # index where the unprocessed part of input_string starts
        self.current_char_index = 0
        # a pair (most recently read token, matched substring of input_string)
        self.current_token = self.get_token()

    def skip_white_space(self):
        '''Consumes all characters in input_string up to the next
           non-white-space character.'''
        white_spaces = [" ", "\n","\t"]
        while self.current_char_index < len(self.input_string) and (self.input_string[self.current_char_index] in white_spaces):
            self.current_char_index +=1

    def no_token(self):
        '''Stop execution if the input cannot be matched to a token.'''
        print('lexical error: no token found at the start of ' +
              self.input_string[self.current_char_index:])
        sys.exit()

    def get_token(self):
        '''Returns the next token and the part of input_string it matched.
           The returned token is None if there is no next token.
           The characters up to the end of the token are consumed.
           TODO:
           Raise an exception by calling no_token() if the input contains
           extra non-white-space characters that do not match any token.'''
        self.skip_white_space()
        # find the longest prefix of input_string that matches a token
        token, longest = None, ''  
        flag = 0
        for (t, r) in Token.token_regexp:
            match = re.match(r, self.input_string[self.current_char_index:])
            if match and match.end() > len(longest): 
                token, longest = t, match.group()
              #  print("matched token "+token)
                flag = 1
        # consume the token by moving the index to the end of the matched part
        self.current_char_index += len(longest)
        if flag == 0 and token == None and self.current_char_index<(len(self.input_string)-1):           
            self.no_token()        
        return (token, longest)

    def lookahead(self):
        '''Returns the next token without consuming it.
           Returns None if there is no next token.'''
        return self.current_token[0]

    def unexpected_token(self, found_token, expected_tokens):
        '''Stop execution because an unexpected token was found.
           found_token contains just the token, not its value.
           expected_tokens is a sequence of tokens.'''
        print('syntax error: token in ' + repr(sorted(expected_tokens)) +
              ' expected but ' + repr(found_token) + ' found')
        sys.exit()

    def consume(self, *expected_tokens):
        '''Returns the next token and consumes it, if it is in
           expected_tokens. Calls unexpected_token(...) otherwise.
           If the token is a number or an identifier, not just the
           token but a pair of the token and its value is returned.'''
        token = self.current_token[0]
       # print("current token "+token)
       # print("expected tokens "+''.join(expected_tokens))
        if token in expected_tokens:
            if token in Token.ID or token is Token.NUM:
               # print("identifier "+token)                
                new_token = (self.current_token[0], self.current_token[1])
            else:
              #  print("not identifier "+token)
               # print("returned token "+token)
                new_token = token
        else:
            self.unexpected_token(token, expected_tokens)
        scanner.current_token = scanner.get_token()  
        return new_token                               
        
        

class Token:
    # The following enumerates all tokens.
    DO    = 'DO'
    ELSE  = 'ELSE'
    END   = 'END'
    IF    = 'IF'
    THEN  = 'THEN'
    WHILE = 'WHILE'
    READ  = 'READ'
    WRITE = 'WRITE'    
    SEM   = 'SEM'
    BEC   = 'BEC'
    LESS  = 'LESS'
    EQ    = 'EQ'
    GRTR  = 'GRTR'
    LEQ   = 'LEQ'
    GEQ   = 'GEQ'    
    NEQ   = 'NEQ'
    ADD   = 'ADD'
    SUB   = 'SUB'
    MUL   = 'MUL'
    DIV   = 'DIV'
    LPAR  = 'LPAR'
    RPAR  = 'RPAR'
    NUM   = 'NUM'
    ID    = 'ID'


    # The following list gives the regular expression to match a token.
    # The order in the list matters for mimicking Flex behaviour.
    # Longer matches are preferred over shorter ones.
    # For same-length matches, the first in the list is preferred.
    token_regexp = [       
        (DO,    'do'),
        (ELSE,  'else'),
        (END,   'end'),
        (IF,    'if'),
        (THEN,  'then'),
        (WHILE, 'while'),
        (READ,  'read'),
        (WRITE, 'write'),         
        (SEM,   ';'),
        (BEC,   ':='),
        (LESS,  '<'),
        (EQ,    '='),
        (GRTR,  '>'),
        (LEQ,   '<='),
        (GEQ,   '>='),
        (NEQ,   '!='),
        (ADD,   '\\+'), # + is special in regular expressions
        (SUB,   '-'),        
        (MUL,   '\\*'),
        (DIV,   '\\/'),                
        (LPAR,  '\\('), # ( is special in regular expressions
        (RPAR,  '\\)'), # ) is special in regular expressions
        (NUM,   '[0-9]*'),        
        (ID,   '[a-z]+'),
    ]

# Initialise scanner.

scanner = Scanner(sys.stdin)

# Show all tokens in the input.

token = scanner.lookahead()
while token != None:
    if token in [Token.NUM, Token.ID]:
        token, value = scanner.consume(token)
        print(token, value)
    else:
        token = scanner.consume(token)
        print(token)
    token = scanner.lookahead()

