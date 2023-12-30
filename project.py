from enum import Enum

class TokenType(Enum):
    NUMBER = 1
    ADDITION = 2
    SUBTRACT = 3
    MULTI = 4
    DIVIDE = 5
    END_OF_FILE = 6

class Token:
    def __init__(self, type, value=0):
        self.type = type
        self.value = value

class ELexer:
    def __init__(self, input_str):
        self.input = input_str
        self.position = 0

    def get_next_token(self):
        while self.position < len(self.input) and self.input[self.position].isspace():
            # Skip whitespace
            self.position += 1

        if self.position >= len(self.input):
            # End of file
            return Token(TokenType.END_OF_FILE)

        current_char = self.input[self.position]
        if current_char == '+':
            self.position += 1
            return Token(TokenType.ADDITION)
        elif current_char == '-':
            self.position += 1
            return Token(TokenType.SUBTRACT)
        elif current_char == '*':
            self.position += 1
            return Token(TokenType.MULTI)
        elif current_char == '/':
            self.position += 1
            return Token(TokenType.DIVIDE)
        elif current_char.isdigit():
            # Parse NUMBER
            value = 0
            while self.position < len(self.input) and self.input[self.position].isdigit():
                value = value * 10 + int(self.input[self.position])
                self.position += 1
            return Token(TokenType.NUMBER, value)
        else:
            # Invalid character
            raise ValueError(f"Error: Invalid character '{current_char}'")

class ExpressionParseException(Exception):
    pass

class ExpressionParser:
    def __init__(self, lexer):
        self.lexer = lexer
        self.current_token = lexer.get_next_token()

    def parse_expression(self):
        result = self.parse_term()  # Parse the first term in the expression

        while self.current_token.type in (TokenType.ADDITION, TokenType.SUBTRACT):
            op = self.current_token
            if op.type == TokenType.ADDITION:
                self.consume(TokenType.ADDITION)
                result += self.parse_term()
            elif op.type == TokenType.SUBTRACT:
                self.consume(TokenType.SUBTRACT)
                result -= self.parse_term()

        return result

    def parse(self):
        self.parse_expression()
        if self.current_token.type != TokenType.END_OF_FILE:
            raise ExpressionParseException("Error: Unexpected token after expression")

    def consume(self, expected_type):
        if self.current_token.type == expected_type:
            self.current_token = self.lexer.get_next_token()
        else:
            raise ExpressionParseException("Error: Unexpected token type")

    def parse_factor(self):
        if self.current_token.type == TokenType.NUMBER:
            value = self.current_token.value
            self.consume(TokenType.NUMBER)
            return value
        elif self.current_token.type == TokenType.ADDITION:
            self.consume(TokenType.ADDITION)
            return self.parse_factor()
        elif self.current_token.type == TokenType.SUBTRACT:
            self.consume(TokenType.SUBTRACT)
            return -self.parse_factor()
        else:
            raise ExpressionParseException("Error: Unexpected token type in factor")

    def parse_term(self):
        result = self.parse_factor()

        while self.current_token.type in (TokenType.MULTI, TokenType.DIVIDE):
            op = self.current_token
            if op.type == TokenType.MULTI:
                self.consume(TokenType.MULTI)
                result *= self.parse_factor()
            elif op.type == TokenType.DIVIDE:
                self.consume(TokenType.DIVIDE)
                divisor = self.parse_factor()
                if divisor == 0:
                    raise ExpressionParseException("Error: Division by zero")
                result /= divisor

        return result

def main():
    input_str = input("Enter your arithmetic expression: ")
    
    try:
        lexer = ELexer(input_str)
        parser = ExpressionParser(lexer)

        parser.parse()

        print("The Expression has been parsed successful ")
    except ExpressionParseException as e:
        print(e)

if __name__ == "__main__":
    main()