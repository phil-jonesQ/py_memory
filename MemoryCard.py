class Card:
    ''' Class to create a card object '''
    def __init__(self, value, suite):
        self.value = value
        self.suite = suite

    def display_card(self, index):
        print("The", self.value, "Of", self.suite, "is in cell", index)

    def test(self):
        print("HELLO!")






