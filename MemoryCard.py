class MemoryCard:
    ''' Class to create a card object '''
    def __init__(self, name=None, value=None, colour=None):
        self.name = name
        self.value = value
        self.colour = colour

    def display_card(self):
        print(self.name, self.value, self.colour)






