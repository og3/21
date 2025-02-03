import random
from collections import Counter


class Deck:
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def reset(self):
        self.cards = self.initial_deck_cards()
        self.shuffle()

    def initial_deck_cards(self):
        return [i for i in range(1, 12)]

    def identify_remaining_cards(self, player_hand, opponent_hand):
        card_counter = Counter(self.initial_deck_cards())

        for card in player_hand:
            if card != "?":
                card_counter[card] -= 1

        for card in opponent_hand:
            if card != "?":
                card_counter[card] -= 1

        remaining_cards = [
            card
            for card, count in card_counter.items()
            if count > 0
            for _ in range(count)
        ]
        return remaining_cards
