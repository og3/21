import random
import time


class Effect:
    PAUSE_DURATION = 2

    def display_logo(logo_name):
        filepath = f"logos/{logo_name}.txt"

        try:
            with open(filepath, "r", encoding="utf-8") as file:
                content = file.read()

            print(content)
        except FileNotFoundError:
            return "Error: ファイルが見つかりません。"
        except Exception as e:
            return f"Error: {e}"

    def highlight_line(text):
        line = "*" * (len(text) * 2)
        print(line)
        print(text)
        print(line)

    def display_with_pause():
        time.sleep(Effect.PAUSE_DURATION)


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

    def show_score(self, hide_first_card=False):
        if hide_first_card and len(self.hand) > 1:
            return f"{self.show_hand(hide_first_card)} (合計: ?+{self.calculate_score_excluding_first()}/{Game21.MAX_SCORE})"

        return f"{self.show_hand(hide_first_card)} (合計: {self.calculate_score()}/{Game21.MAX_SCORE})"

    def draw_card(self, deck, silent=False):
        if deck.cards:
            card = deck.draw()
            self.hand.append(card)
            if not silent:
                Effect.highlight_line(f"{self.name}は{card}を引きました。")
                Effect.display_with_pause()

            return card
        else:
            Effect.highlight_line("山札が尽きました！！")
            Effect.display_with_pause()
            return False


class Deck:
    def shuffle(self):
        random.shuffle(self.cards)

    def draw(self):
        return self.cards.pop() if self.cards else None

    def reset(self):
        self.cards = [i for i in range(1, 12)]
        self.shuffle()


class Game21:
    MAX_SCORE = 21
    INITIAL_LIFE = 5
    INITIAL_CARDS = 2
    INITIAL_ROUND_NUMBER = 0
    MIN_OPPONENT_DRAW_SCORE = 17

    def __init__(self):
        self.initialize_game()

    def initialize_game(self):
        # プレイヤーと相手のライフカウンターを初期化
        self.player = Player("あなた", Game21.INITIAL_LIFE)
        self.opponent = Player("相手", Game21.INITIAL_LIFE)
        self.round_number = Game21.INITIAL_ROUND_NUMBER
        self.deck = Deck()
        self.reset_round()

    def reset_round(self):
        self.deck.reset()
        self.player.reset_hand()
        self.opponent.reset_hand()

    def deal_initial_cards(self):
        for _ in range(Game21.INITIAL_CARDS):
            self.player.draw_card(self.deck, silent=True)
            self.opponent.draw_card(self.deck, silent=True)

    def increment_round_number(self):
        self.round_number += 1

    def player_turn(self):
        print(f"\nあなたの手札: {self.player.show_score(hide_first_card=True)}")
        print(f"相手の手札: {self.opponent.show_score(hide_first_card=True)}")
        choice = self.get_player_input()
        if choice.lower() == "y":
            if not self.player.draw_card(self.deck):
                return False
        return choice.lower() != "n"

    def get_player_input(self):
        while True:
            try:
                choice = input("カードを引きますか？ (y/n): ").strip().lower()
                if choice in ["y", "n"]:
                    return choice
                else:
                    print("無効な入力です。'y' または 'n' を入力してください。")
            except EOFError:
                print("入力エラーが発生しました。デフォルト値 'n' を使用します。")
                return "n"

    def opponent_turn(self):
        opponent_score = self.opponent.calculate_score()

        # 相手の判断ロジック: スコアがMIN_OPPONENT_DRAW_SCORE未満ならカードを引く
        if opponent_score < Game21.MIN_OPPONENT_DRAW_SCORE:
            self.opponent.draw_card(self.deck)
            return True
        else:
            Effect.highlight_line("相手はカードを引きませんでした。")
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
                Effect.highlight_line(
                    "お互いにカードを引かなかったので勝敗判定を行います..."
                )
                Effect.display_with_pause()
                return self.check_winner()

            # ターンの切り替え
            player_active = not player_active

    def check_winner(self):
        player_score = self.player.calculate_score()
        opponent_score = self.opponent.calculate_score()

        print(f"\nあなたの手札: {self.player.show_score(hide_first_card=False)})")
        print(f"相手の手札: {self.opponent.show_score(hide_first_card=False)})")

        if player_score > Game21.MAX_SCORE and opponent_score > Game21.MAX_SCORE:
            print("両者ともバーストしました！")
            return "draw"
        elif player_score > Game21.MAX_SCORE:
            print("あなたはバーストしました！")
            return "opponent"
        elif opponent_score > Game21.MAX_SCORE:
            print("相手がバーストしました！")
            return "player"
        elif player_score == opponent_score:
            print("両者とも同じスコアです！")
            return "draw"
        elif player_score > opponent_score:
            return "player"
        elif player_score < opponent_score:
            return "opponent"

    def play_round(self):
        self.increment_round_number()
        self.deal_initial_cards()

        print(f"\nあなたの手札: {self.player.show_score(hide_first_card=True)}")
        print(f"相手の手札: {self.opponent.show_score(hide_first_card=True)}")

        # 交互にカードを引く
        return self.alternating_turns()

    def play_game(self):
        while self.player.life > 0 and self.opponent.life > 0:
            print(f"\n--- 第{self.round_number + 1}ラウンド  ---")
            print(f"ライフ: あなた {self.player.life} - 相手 {self.opponent.life}")

            result = self.play_round()

            if result == "player":
                Effect.display_logo("you_win")
                print(
                    f"\nあなたの勝ちです！相手はライフを{self.round_number}失います。。"
                )
                self.opponent.life -= self.round_number
            elif result == "opponent":
                Effect.display_logo("you_lose")
                print(
                    f"\nあなたの負けです！あなたはライフを{self.round_number}失います。。"
                )
                self.player.life -= self.round_number
            else:
                Effect.display_logo("draw")
                print("\n引き分けです！ラウンドは進みますが、ライフはそのままです。。")

            # ラウンドリセット
            self.reset_round()

        Effect.display_logo("game_over")
        if self.player.life <= 0:
            print("\nゲームオーバー！相手の勝利です。")
        else:
            print("\nおめでとうございます！あなたの勝利です。")


# ゲームを開始
if __name__ == "__main__":
    game = Game21()
    Effect.display_logo("game_21")
    game.play_game()
