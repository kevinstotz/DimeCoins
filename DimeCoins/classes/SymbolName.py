

class SymbolName:

    def __init__(self, symbol):
        self.symbol = symbol
        self.new_symbol = ""

    def parse_symbol(self):
        new_symbol = ""
        for idx, char in enumerate(self.symbol):
            if idx == 0:
                if char.isdigit():
                    if int(char) == 1:
                        new_symbol = new_symbol + 'ONE_'
                    elif int(char) == 2:
                        new_symbol = new_symbol + 'TWO_'
                    elif int(char) == 3:
                        new_symbol = new_symbol + 'THREE_'
                    elif int(char) == 4:
                        new_symbol = new_symbol + 'FOUR_'
                    elif int(char) == 5:
                        new_symbol = new_symbol + 'FIVE_'
                    elif int(char) == 6:
                        new_symbol = new_symbol + 'SIX_'
                    elif int(char) == 7:
                        new_symbol = new_symbol + 'SEVEN_'
                    elif int(char) == 8:
                        new_symbol = new_symbol + 'EIGHT_'
                    elif int(char) == 9:
                        new_symbol = new_symbol + 'NINE_'
                    elif int(char) == 0:
                        new_symbol = new_symbol + 'ZERO_'
                    else:
                        pass
                    continue


            if idx == (len(self.symbol) - 1):
                if char == '$':
                    new_symbol = new_symbol + 'DOLLAR'
                elif char == '@':
                    new_symbol = new_symbol + '_AT'
                else:
                    new_symbol = new_symbol + char.upper()
                continue

            if char == '$':
                new_symbol = new_symbol + 'DOLLAR_'
            elif char == '@':
                new_symbol = new_symbol + 'AT_'
            elif char.isdigit():
                new_symbol = new_symbol + str(char)
            elif char.encode('ascii').isalpha():
                new_symbol = new_symbol + char.upper()
            else:
                pass

        self.new_symbol = new_symbol
        return new_symbol
