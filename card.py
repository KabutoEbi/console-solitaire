class Card:
    SUITS = ['♠', '♥', '♦', '♣']
    RANKS = ['A'] + [str(n) for n in range(2, 11)] + ['J', 'Q', 'K']

    def __init__(self, suit, rank, face_up=False):
        self.suit = suit
        self.rank = rank
        self.face_up = face_up

    def __str__(self):
        return f'{self.suit}{self.rank}' if self.face_up else 'XX'

    def flip(self):
        self.face_up = not self.face_up
