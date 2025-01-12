import random

class Game21:
    MAX_SCORE = 21

    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        # プレイヤーと相手のライフカウンターを初期化
        self.player_life = 5
        self.opponent_life = 5
        self.round_number = 0
        self.reset_round()

    def reset_round(self):
        # 山札 (1~11のカードが1セット)
        self.deck = [i for i in range(1, 12)]
        random.shuffle(self.deck)
        
        # プレイヤーと相手の手札
        self.player_hand = []
        self.opponent_hand = []

    def draw_card(self, hand, owner, silent=False):
        if self.deck:
            card = self.deck.pop()
            if not silent:
                print(f"{owner}は{card}を引きました。")
            return card
        else:
            print("山札が尽きました！")
            return None

    def deal_initial_cards(self, hand, owner):
        for _ in range(2):
            hand.append(self.draw_card(hand, owner, silent=True))

    def increment_round_number(self):
        self.round_number += 1

    def calculate_score(self, hand):
        total = sum(hand)
        return total

    def calculate_score_excluding_first(self, hand):
        total = sum(hand[1:])
        return total

    def show_hand(self, hand):
        if len(hand) > 1:
            return f"['?', {', '.join(map(str, hand[1:]))}] (合計: ?+{self.calculate_score_excluding_first(hand)}/{Game21.MAX_SCORE})"
        return "[]"

    def player_turn(self):
        print(f"\nあなたの手札: {self.show_hand(self.player_hand)}")
        print(f"相手の手札: {self.show_hand(self.opponent_hand)}")
        choice = self.get_player_input()
        if choice.lower() == 'y':
            card = self.draw_card(self.player_hand, "あなた")
            if card:
                self.player_hand.append(card)
        return choice.lower() != 'n'

    def get_player_input(self):
        # プレイヤーがカードを引くかどうかを選べるようにする
        while True:
            try:
                choice = input("カードを引きますか？ (y/n): ").strip().lower()
                if choice in ['y', 'n']:
                    return choice
                else:
                    print("無効な入力です。'y' または 'n' を入力してください。")
            except EOFError:
                print("入力エラーが発生しました。デフォルト値 'n' を使用します。")
                return 'n'

    def opponent_turn(self):
        opponent_score = self.calculate_score(self.opponent_hand)

        # 相手の判断ロジック: スコアが17未満ならカードを引く
        if opponent_score < 17:
            card = self.draw_card(self.opponent_hand, "相手")
            if card:
                self.opponent_hand.append(card)
            return True
        else:
            print("相手はカードを引きませんでした。")
            return False

    def alternating_turns(self):
        player_active = True
        player_done = False
        opponent_done = False

        while True:
            if player_active:
                print("\nあなたのターンです。")
                if not self.player_turn():
                    player_done = True
            else:
                print("\n相手のターンです。")
                if not self.opponent_turn():
                    opponent_done = True

            # 両者がカードを引かない場合に勝敗判定
            if player_done and opponent_done:
                return self.check_winner()

            # 切り替え
            player_active = not player_active

    def check_winner(self):
        player_score = self.calculate_score(self.player_hand)
        opponent_score = self.calculate_score(self.opponent_hand)

        print(f"\nあなたの手札: {self.player_hand} (合計: ?+{player_score}/{Game21.MAX_SCORE})")
        print(f"相手の手札: {self.opponent_hand} (合計: ?+{opponent_score}/{Game21.MAX_SCORE})")

        if player_score > 21 and opponent_score > 21:
            print("両者ともバーストしました！引き分けです。")
            return "draw"
        elif player_score > 21:
            print("あなたはバーストしました！")
            return "opponent"
        elif opponent_score > 21:
            print("相手がバーストしました！")
            return "player"
        elif player_score == opponent_score:
            print("両者とも同じスコアです！引き分けです。")
            return "draw"
        elif player_score > opponent_score:
            return "player"
        elif player_score < opponent_score:
            return "opponent"

    def play_round(self):
        # 初期状態
        self.increment_round_number()
        self.deal_initial_cards(self.player_hand, "あなた")
        self.deal_initial_cards(self.opponent_hand, "相手")

        print(f"\nあなたの手札: {self.show_hand(self.player_hand)}")
        print(f"相手の手札: {self.show_hand(self.opponent_hand)}")

        # 交互にカードを引く
        return self.alternating_turns()

    def play_game(self):
        while self.player_life > 0 and self.opponent_life > 0:
            print(f"\n--- 第{self.round_number + 1}ラウンド  ---")
            print(f"ライフ: あなた {self.player_life} - 相手 {self.opponent_life}")

            result = self.play_round()

            if result == "player":
                print(f"\nあなたの勝ちです！相手はライフを{self.round_number}失います。。")
                self.opponent_life -= self.round_number
            elif result == "opponent":
                print(f"\nあなたの負けです！あなたはライフを{self.round_number}失います。。")
                self.player_life -= self.round_number
            else:
                print("\n引き分けです！ラウンドは進みますが、ライフはそのままです。。")

            # ラウンドリセット
            self.reset_round()

        if self.player_life <= 0:
            print("\nゲームオーバー！相手の勝利です。")
        else:
            print("\nおめでとうございます！あなたの勝利です。")

# ゲームを開始
if __name__ == "__main__":
    game = Game21()
    game.play_game()
