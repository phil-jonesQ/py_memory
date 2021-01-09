class Card:
    ''' Class to create a card object '''
    def __init__(self, value, colour):
        self.value = value
        self.colour = colour

    def display_card(self):
        print("The ", self.value, "Of ", self.colour)






