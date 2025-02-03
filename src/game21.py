from effect import Effect
from deck import Deck
from player import Player
from calculate_burst_probability import CalculateBurstProbability
import joblib
import pandas as pd


class Game21:
    MAX_SCORE = 21
    INITIAL_LIFE = 5
    INITIAL_CARDS = 2
    INITIAL_ROUND_NUMBER = 0
    MIN_OPPONENT_DRAW_SCORE = 17
    NPC_MODEL_PATH = "./datas/npc_model_data/random_forest_model.pkl"

    def __init__(self):
        self.initialize_game()
        # todo:このクラスが持つのは違和感がある
        self.npc_model = joblib.load(Game21.NPC_MODEL_PATH)

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
            self.player.draw_card(self.deck)
            self.opponent.draw_card(self.deck)

    def increment_round_number(self):
        self.round_number += 1

    def player_turn(self):
        print(
            f"\nあなたの手札: {self.player.show_score(Game21.MAX_SCORE, hide_first_card=True)}"
        )
        print(
            f"相手の手札: {self.opponent.show_score(Game21.MAX_SCORE, hide_first_card=True)}"
        )
        choice = self.get_player_input()
        if choice.lower() == "y":
            card = self.player.draw_card(self.deck)
            if card:
                Effect.highlight_line(f"{self.player.name}は{card}を引きました。")
                Effect.display_with_pause()

                return True

            else:
                Effect.highlight_line("山札が尽きました！！")
                Effect.display_with_pause()

                return False
        else:
            Effect.highlight_line("カードを引きませんでした。")
            Effect.display_with_pause()
            return False

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

    def generate_prediction_data(self):
        score_difference = abs(
            (Game21.MAX_SCORE - self.player.calculate_score_excluding_first())
            - (Game21.MAX_SCORE - self.opponent.calculate_score_excluding_first())
        )
        player_burst_prob = CalculateBurstProbability.calculate_burst_probability(
            self.player.show_hand(hide_first_card=True), self.deck.cards
        )
        opponent_burst_prob = CalculateBurstProbability.calculate_burst_probability(
            self.opponent.show_hand(hide_first_card=True), self.deck.cards
        )
        prediction_data = pd.DataFrame(
            [
                {
                    "score_difference": score_difference,
                    "player_burst_prob": player_burst_prob,
                    "opponent_burst_prob": opponent_burst_prob,
                    "remaining_cards_num": len(self.deck.cards),
                    "round": self.round_number,
                    "player_life": self.player.life,
                    "opponent_life": self.player.life,
                }
            ]
        )

        return prediction_data

    def should_draw_card(self, data):
        prediction = self.npc_model.predict(data)

        return True if prediction[0] else False

    def opponent_turn(self):

        if self.should_draw_card(self.generate_prediction_data()):
            card = self.opponent.draw_card(self.deck)
            if card:
                Effect.highlight_line(f"{self.opponent.name}は{card}を引きました。")
                Effect.display_with_pause()
                return True
            else:
                Effect.highlight_line("山札が尽きました！！")
                Effect.display_with_pause()

                return False

        else:
            Effect.highlight_line(f"{self.opponent.name}はカードを引きませんでした。")
            Effect.display_with_pause()
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

        print(
            f"\nあなたの手札: {self.player.show_score(Game21.MAX_SCORE, hide_first_card=False)})"
        )
        print(
            f"相手の手札: {self.opponent.show_score(Game21.MAX_SCORE, hide_first_card=False)})"
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
        self.deal_initial_cards()

        print(
            f"\nあなたの手札: {self.player.show_score(Game21.MAX_SCORE, hide_first_card=True)}"
        )
        print(
            f"相手の手札: {self.opponent.show_score(Game21.MAX_SCORE, hide_first_card=True)}"
        )

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
