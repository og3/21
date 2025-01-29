class NpcThinkPattern:

    @staticmethod
    def should_draw_defensive(
        opponent_burst_prob,
        player_burst_prob,
        round_number,
        remaining_cards_num,
        player_life,
    ):
        """
        ディフェンス型: 相手がバーストするのを待つ。
        - 前提：山札のカードが4枚以上なら引く
        - 相手のバースト確率が30％以下なら引く
        - そのラウンドで敗北すると自分のライフが0になる場合、自分のバースト確率が30%以下なら引く
        """
        if remaining_cards_num >= 4:
            if opponent_burst_prob < 0.3:
                return True
            if player_life - round_number == 0 and player_burst_prob < 0.3:
                return True

        return False

    @staticmethod
    def should_draw_offensive(
        player_burst_prob,
        score_difference,
        round_number,
        remaining_cards_num,
        player_life,
        opponent_life,
    ):
        """
        オフェンス型: 21に近づくことを目指す。
        - 前提：山札が2枚以上なら引く
        - そのラウンドで勝利すると相手のライフが0になる場合、自分のバースト確率が60%以下なら引く
        - そのラウンドで敗北すると自分のライフが0になる場合、自分のバースト確率が40%以下なら引く
        - スコア差が3以上なら自分のバースト確率が60%以下で引く
        - 自分のバースト確率が50％以下なら引く
        """

        if remaining_cards_num >= 2:
            if opponent_life - round_number == 0 and player_burst_prob < 0.6:
                return True
            if player_life - round_number == 0 and player_burst_prob < 0.4:
                return True
            if score_difference >= 3 and player_burst_prob < 0.6:
                return True
            if player_burst_prob < 0.5:
                return True

        return False

    @staticmethod
    def should_draw_cooperative(
        player_burst_prob,
        opponent_burst_prob,
        round_number,
        remaining_cards_num,
        opponent_life,
    ):
        """
        協調型: 相手のバースト確率に合わせてカードを引く。
        - 前提：山札のカードが3枚以上なら引く
        - そのラウンドで勝利すると相手のライフが0になる場合、自分のバースト確率が40%以下なら引く
        - バースト確率の差が20%以下なら引く
        - 自分のバースト確率が50%以下なら引く

        """

        if remaining_cards_num >= 3:
            burst_prob_difference = abs(player_burst_prob - opponent_burst_prob)

            if player_burst_prob < 0.5:
                return True
            if burst_prob_difference < 0.2:
                return True
            if opponent_life - round_number == 0 and player_burst_prob < 0.4:
                return True

        return False
