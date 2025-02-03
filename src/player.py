class Player:
    def __init__(self, name, initial_life):
        self.name = name
        self.life = initial_life
        self.hand = []

    def reset_hand(self):
        self.hand = []

    def calculate_score(self):
        return sum(self.hand)

    def calculate_score_excluding_first(self):
        return sum(self.hand[1:])

    def show_hand(self, hide_first_card=False):
        if hide_first_card and len(self.hand) > 1:
            return ["?", *self.hand[1:]]

        return self.hand

    def show_score(self, max_score, hide_first_card=False):
        if hide_first_card and len(self.hand) > 1:
            return f"{self.show_hand(hide_first_card)} (合計: ?+{self.calculate_score_excluding_first()}/{max_score})"

        return f"{self.show_hand(hide_first_card)} (合計: {self.calculate_score()}/{max_score})"

    def draw_card(self, deck):
        if deck.cards:
            card = deck.draw()
            self.hand.append(card)

            return card
        else:
            return False
