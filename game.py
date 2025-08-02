from deck import Deck
from card import Card

import copy

class Game:
    def __init__(self):
        self.history = []  # undo用
        self.score = 0     # スコア
        self.moves = 0     # 手数
        self._init_game()

    def _init_game(self):
        self.deck = Deck()
        self.tableau = [[] for _ in range(7)]  # 場札
        self.foundation = [[] for _ in range(4)]  # 組札
        self.stock = []  # 山札
        self.waste = []  # 捨て札
        self.score = 0   # ←ここでも初期化
        self.moves = 0   # ←ここでも初期化
        self.setup()

    def setup(self):
        # 場札にカードを配る
        for i in range(7):
            for j in range(i + 1):
                card = self.deck.draw()
                if j == i:
                    card.face_up = True
                self.tableau[i].append(card)
        # 残りは山札
        while not self.deck.is_empty():
            self.stock.append(self.deck.draw())

    def save_state(self):
        state = (
            copy.deepcopy(self.tableau),
            copy.deepcopy(self.foundation),
            copy.deepcopy(self.stock),
            copy.deepcopy(self.waste),
            self.score,
            self.moves
        )
        self.history.append(state)

    def undo(self):
        if not self.history:
            print("No moves to undo.")
            return
        state = self.history.pop()
        self.tableau = copy.deepcopy(state[0])
        self.foundation = copy.deepcopy(state[1])
        self.stock = copy.deepcopy(state[2])
        self.waste = copy.deepcopy(state[3])
        self.score = state[4]
        self.moves = state[5]
        print("Undid one move.")

    def add_move(self, score_delta=0):
        self.moves += 1
        self.score += score_delta

    def get_score(self):
        return self.score

    def get_moves(self):
        return self.moves

    def is_stuck(self):
        if self.stock or self.waste:
            return False
        for i, pile in enumerate(self.tableau):
            if not pile or not pile[-1].face_up:
                continue
            for j, dest in enumerate(self.tableau):
                if i == j:
                    continue
                if dest:
                    if self.can_stack(pile[-1], dest[-1]):
                        return False
                else:
                    if pile[-1].rank == 'K':
                        return False
        for i, pile in enumerate(self.tableau):
            if pile and pile[-1].face_up:
                for foundation in self.foundation:
                    if self.can_move_to_foundation(pile[-1], foundation):
                        return False
        if self.waste:
            card = self.waste[-1]
            for dest in self.tableau:
                if dest:
                    if self.can_stack(card, dest[-1]):
                        return False
                else:
                    if card.rank == 'K':
                        return False
            for foundation in self.foundation:
                if self.can_move_to_foundation(card, foundation):
                    return False
        return True

    def is_win(self):
        # 全ての組札がKで終わっていれば勝利
        return all(len(foundation) == 13 and foundation[-1].rank == 'K' for foundation in self.foundation)
        # 全ての組札がKで終わっていれば勝利
        return all(len(foundation) == 13 and foundation[-1].rank == 'K' for foundation in self.foundation)
    def move_foundation_to_tableau(self, foundation_idx, tableau_idx):
        self.save_state()
        if foundation_idx < 0 or foundation_idx >= len(self.foundation):
            print("Invalid foundation number.")
            return
        if tableau_idx < 0 or tableau_idx >= len(self.tableau):
            print("Invalid tableau number.")
            return
        foundation = self.foundation[foundation_idx]
        if not foundation:
            print("That foundation is empty.")
            return
        card = foundation[-1]
        dest_pile = self.tableau[tableau_idx]
        if dest_pile:
            dest_card = dest_pile[-1]
            if not dest_card.face_up:
                print("Top card of destination tableau is face down.")
                return
            if not self.can_stack(card, dest_card):
                print("Cannot move to destination tableau. Rule violation.")
                return
        else:
            if card.rank != 'K':
                print("Only King can be placed on an empty tableau column.")
                return
        dest_pile.append(card)
        foundation.pop()
        self.add_move(-15)
        print(f"Moved from foundation {foundation_idx+1} to tableau {tableau_idx+1}.")

    def move_waste_to_tableau(self, dst):
        self.save_state()
        if not self.waste:
            print("Waste is empty.")
            return
        card = self.waste[-1]
        dest_pile = self.tableau[dst]
        if dest_pile:
            dest_card = dest_pile[-1]
            if not dest_card.face_up:
                print("Top card of destination tableau is face down.")
                return
            if not self.can_stack(card, dest_card):
                print("Cannot move to destination tableau. Rule violation.")
                return
        else:
            if card.rank != 'K':
                print("Only King can be placed on an empty tableau column.")
                return
        dest_pile.append(card)
        self.waste.pop()
        self.add_move()
        print(f"Moved from waste to tableau {dst+1}.")

    def move_to_foundation(self, src_type, src_idx=None):
        self.save_state()
        if src_type == 't':
            pile = self.tableau[src_idx]
            if not pile or not pile[-1].face_up:
                print("Top card of tableau is not face up.")
                return
            card = pile[-1]
        elif src_type == 'w':
            if not self.waste:
                print("Waste is empty.")
                return
            card = self.waste[-1]
        else:
            print("Specify t (tableau) or w (waste).")
            return

        for i, foundation in enumerate(self.foundation):
            if self.can_move_to_foundation(card, foundation):
                foundation.append(card)
                if src_type == 't':
                    pile.pop()
                    if pile and not pile[-1].face_up:
                        pile[-1].flip()
                else:
                    self.waste.pop()
                self.add_move(10)
                print(f"Moved {card} to foundation {i+1}.")
                return
        print("Cannot move to foundation. Rule violation.")

    def move_tableau_to_tableau(self, src, dst, count=1):
        self.save_state()
        if src < 0 or src >= len(self.tableau) or dst < 0 or dst >= len(self.tableau):
            print("Invalid tableau column number.")
            return
        pile = self.tableau[src]
        if count < 1 or count > len(pile):
            print("Invalid number of cards to move.")
            return
        moving = pile[-count:]
        if not moving[0].face_up:
            print("Cannot move face down cards.")
            return
        dest_pile = self.tableau[dst]
        if dest_pile:
            dest_card = dest_pile[-1]
            if not dest_card.face_up:
                print("Top card of destination tableau is face down.")
                return
            if not self.can_stack(moving[0], dest_card):
                print("Cannot move to destination tableau. Rule violation.")
                return
        else:
            if moving[0].rank != 'K':
                print("Only King can be placed on an empty tableau column.")
                return
        self.tableau[dst].extend(moving)
        del pile[-count:]
        if pile and not pile[-1].face_up:
            pile[-1].flip()
        self.add_move()
        print(f"Moved {count} card(s) from tableau {src+1} to tableau {dst+1}.")

    def can_move_to_foundation(self, card, foundation):
        if not foundation:
            return card.rank == 'A'
        top = foundation[-1]
        return card.suit == top.suit and Card.RANKS.index(card.rank) == Card.RANKS.index(top.rank) + 1
    def can_stack(self, moving_card, dest_card):
        # 色違いで1小さい
        red = ['♥', '♦']
        black = ['♠', '♣']
        if (moving_card.suit in red and dest_card.suit in red) or (moving_card.suit in black and dest_card.suit in black):
            return False
        rank_order = Card.RANKS
        try:
            return rank_order.index(moving_card.rank) + 1 == rank_order.index(dest_card.rank)
        except ValueError:
            return False

    def print_state(self):
        print('--- Foundation ---')
        for i, pile in enumerate(self.foundation):
            print(f'{i+1}: {pile[-1] if pile else "--"}')
        print('\n--- Tableau ---')
        for i, pile in enumerate(self.tableau):
            print(f'{i+1}:', ' '.join(str(card) for card in pile))
        print('\n--- Stock ---')
        print(f'Stock: {len(self.stock)} cards, Waste: {self.waste[-1] if self.waste else "--"}')
    def draw_from_stock(self):
        self.save_state()
        if self.stock:
            card = self.stock.pop()
            card.face_up = True
            self.waste.append(card)
            self.add_move()
            print(f"Drew a card from stock: {card}")
        else:
            if self.waste:
                print("Stock is empty. Moving waste back to stock.")
                while self.waste:
                    card = self.waste.pop()
                    card.face_up = False
                    self.stock.append(card)
                self.add_move()
            else:
                print("Both stock and waste are empty. Cannot draw a card.")
