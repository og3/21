class ThinkPattern:

    @staticmethod
    def should_draw_defensive(opponent_burst_prob, round_number):
        """
        ディフェンス型: 相手がバーストするのを待つ。
        - 相手のバースト確率が30％以下なら引く
        - 3ラウンド以降はバースト確率の判定基準を厳しくする（20%以下なら引く）
        """
        threshold = 0.3 if round_number < 3 else 0.2
        return opponent_burst_prob < threshold

    @staticmethod
    def should_draw_offensive(player_burst_prob, score_difference):
        """
        オフェンス型: 21に近づくことを目指す。
        - 自分のバースト確率が50％以下なら引く
        - スコア差が3以上なら自分のバースト確率が60%以下で引く
        """
        if score_difference >= 3:
            return player_burst_prob < 0.6
        return player_burst_prob < 0.5

    @staticmethod
    def should_draw_cooperative(player_burst_prob, opponent_burst_prob):
        """
        協調型: 相手のバースト確率に合わせてカードを引く。
        - 自分のバースト確率が50%以下なら引く
        - バースト確率の差が20%以下なら引く
        """
        burst_prob_difference = abs(player_burst_prob - opponent_burst_prob)
        return player_burst_prob < 0.5 or burst_prob_difference < 0.2
