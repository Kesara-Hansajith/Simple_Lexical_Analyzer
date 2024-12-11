class LexicalAnalyzer:

    def __init__(self):
        # Initialize the lexer with a starting state, empty token list, and buffer for the current token.
        self.state = "START"        # The initial state of the lexer
        self.tokens = []            # List to store tokens as (token_type, token_value) tuples
        self.current_token = ""     # Temporary buffer for constructing tokens

    def reset(self):
        # Reset the current state and clear the token buffer.
        self.state = "START"
        self.current_token = ""

    def add_token(self, token_type):
        # Finalize the current token and add it to the list of tokens[token_type (str): The type of token being finalized].
        self.tokens.append((token_type, self.current_token)
                           )        # Add token to the list
        self.reset()                # Reset state and buffer

    def transition(self, char):
        # Handle the transition between states based on the input character[char (str): The current character being processed].
        # If an unexpected character is encountered "ValueError:" raises.
        if self.state == "START":
            # Determine the type of token based on the first character
            if char.isalpha():      # Start of an identifier
                self.state = "IDENTIFIER"
                self.current_token += char
            elif char.isdigit():    # Start of a number
                self.state = "NUMBER"
                self.current_token += char
            elif char in "+-*/":    # Operators raises then add it to operator token directly
                self.tokens.append(("OPERATOR", char))
            elif char == "=":       # Assignment operator raises then add it to assignment token
                self.tokens.append(("ASSIGNMENT", char))
            elif char in "()":      # Parentheses raises then add it to parenthesis token
                self.tokens.append(("PARENTHESIS", char))
            elif char == ";":       # Semicolon raises then add it to semicolon token
                self.tokens.append(("SEMICOLON", char))  
            elif char.isspace():    # Do nothing for whitespace
                pass                
            else:
                raise ValueError(f"Unexpected character: '{char}'")     # This is used to handle invalid characters
        elif self.state == "IDENTIFIER":
            # Continue collecting alphanumeric characters for identifiers
            if char.isalnum():
                self.current_token += char
            else:
                self.add_token("IDENTIFIER")  # Finalize the identifier token
                self.transition(char)         # Reprocess the current character
        elif self.state == "NUMBER":
            # Continue collecting digits for numeric tokens
            if char.isdigit():
                self.current_token += char
            else:
                self.add_token("NUMBER")      # Finalize the number token
                self.transition(char)         # Reprocess the current character

    def tokenize(self, input_string):
        # Tokenize the given input string into a list of tokens[input_string (str): The input string to be tokenized].
        # Returns a list of tokens as (token_type, token_value) tuples.
        for char in input_string:
            self.transition(char)       # Process each character in the input string
        # Finalize any remaining token at the end of the input
        if self.state == "IDENTIFIER":
            self.add_token("IDENTIFIER")
        elif self.state == "NUMBER":
            self.add_token("NUMBER")
        return self.tokens



if __name__ == "__main__":
    lexer = LexicalAnalyzer()           # Initialize the lexer
    input_expression = input("Enter an expression: ")       # Get the user input 

    # Tokenize the input
    try: 
        tokens = lexer.tokenize(input_expression)       # Generate tokens from the input
        print("\nTokens:")              # Print the resulting tokens
        for token in tokens:
            print(token)
    except ValueError as e:
        print(f"Error: {e}")            # Print an error message for invalid input
