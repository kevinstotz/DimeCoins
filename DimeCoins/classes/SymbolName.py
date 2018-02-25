

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
                    if int(char) == 2:
                        new_symbol = new_symbol + 'TWO_'
                    if int(char) == 3:
                        new_symbol = new_symbol + 'THREE_'
                    if int(char) == 4:
                        new_symbol = new_symbol + 'FOUR_'
                    if int(char) == 5:
                        new_symbol = new_symbol + 'FIVE_'
                    if int(char) == 6:
                        new_symbol = new_symbol + 'SIX_'
                    if int(char) == 7:
                        new_symbol = new_symbol + 'SEVEN_'
                    if int(char) == 8:
                        new_symbol = new_symbol + 'EIGHT_'
                    if int(char) == 9:
                        new_symbol = new_symbol + 'NINE_'
                    if int(char) == 0:
                        new_symbol = new_symbol + 'ZERO_'
                elif char.encode('ascii') == '@':
                    new_symbol = new_symbol + 'BAT_'
                elif char.encode('ascii').isalpha():
                    new_symbol = new_symbol + char
                else:
                    pass
            elif char == 'B@':
                print("FA")
                new_symbol = new_symbol + '_AT'
            else:
                if char.encode('ascii').isalpha() or char.isdigit():
                    new_symbol = new_symbol + char
        self.new_symbol = new_symbol
        return new_symbol
