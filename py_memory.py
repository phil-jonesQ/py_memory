from MemoryCard import MemoryCard

# Initialise
full_cards = []
cards1 = {}
cards2 = {}
cards_amount = range(10)

card_names_list = ["Number One", "Number Two", "Number Three", "Number Four", "Number Five", "Number Six",
                   "Number Seven", "Number Eight", "Number Nine", "Number Ten"]

# Create each set of cards
for card in cards_amount:
    cards1[card] = card_names_list[card]
    full_cards.append(MemoryCard(card_names_list[card], card, "Black"))
    cards2[card] = card_names_list[card]
    full_cards.append(MemoryCard(card_names_list[card], card, "Red"))

print(cards1)
print(cards2)
print(full_cards[18].display_card())




