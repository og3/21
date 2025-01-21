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
    def __init__(self, initial_life):
        self.life = initial_life
        self.hand = []

    def reset_hand(self):
        self.hand = []


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
        self.player = Player(Game21.INITIAL_LIFE)
        self.opponent = Player(Game21.INITIAL_LIFE)
        self.round_number = Game21.INITIAL_ROUND_NUMBER
        self.reset_round()

    def reset_round(self):
        # 山札 (1~11のカードが1セット)
        self.deck = [i for i in range(1, 12)]
        random.shuffle(self.deck)

        self.player.reset_hand()
        self.opponent.reset_hand()

    def draw_card(self, hand, owner, silent=False):
        if self.deck:
            card = self.deck.pop()
            hand.append(card)
            if not silent:
                Effect.highlight_line(f"{owner}は{card}を引きました。")
                Effect.display_with_pause()
            return card
        else:
            print("山札が尽きました！")
            return None

    def deal_initial_cards(self, hand, owner):
        for _ in range(Game21.INITIAL_CARDS):
            self.draw_card(hand, owner, silent=True)

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
        print(f"\nあなたの手札: {self.show_hand(self.player.hand)}")
        print(f"相手の手札: {self.show_hand(self.opponent.hand)}")
        choice = self.get_player_input()
        if choice.lower() == "y":
            self.draw_card(self.player.hand, "あなた")
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
        opponent_score = self.calculate_score(self.opponent.hand)

        # 相手の判断ロジック: スコアがMIN_OPPONENT_DRAW_SCORE未満ならカードを引く
        if opponent_score < Game21.MIN_OPPONENT_DRAW_SCORE:
            self.draw_card(self.opponent.hand, "相手")
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
        player_score = self.calculate_score(self.player.hand)
        opponent_score = self.calculate_score(self.opponent.hand)

        print(
            f"\nあなたの手札: {self.player.hand} (合計: {player_score}/{Game21.MAX_SCORE})"
        )
        print(
            f"相手の手札: {self.opponent.hand} (合計: {opponent_score}/{Game21.MAX_SCORE})"
        )

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
        self.deal_initial_cards(self.player.hand, "あなた")
        self.deal_initial_cards(self.opponent.hand, "相手")

        print(f"\nあなたの手札: {self.show_hand(self.player.hand)}")
        print(f"相手の手札: {self.show_hand(self.opponent.hand)}")

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
