from collections import Counter


class CalculateBurstProbability:
    @staticmethod
    def calculate_burst_probability(player_hand, deck):
        # 山札の残りカードの枚数をカウント
        remaining_cards = Counter(deck)

        # 自分の確定スコアを計算（伏せカード以外）
        visible_score = sum(card for card in player_hand if card != "?")

        burst_cases = 0
        total_cases = 0

        # 伏せカードが取りうるすべての値を試す
        possible_cards = list(remaining_cards.elements())  # 残りのカードリスト

        for hidden_card in possible_cards:  # 伏せカードの1つの可能性を仮定
            # 仮のスコア（確定スコア + 伏せカード）
            player_total_score = visible_score + hidden_card

            # 山札から次に引くカードのバースト確率を計算
            for next_card, count in remaining_cards.items():
                if hidden_card == next_card:
                    count -= 1  # 伏せカードを山札から除く
                if count <= 0:
                    continue

                if player_total_score + next_card > 21:
                    burst_cases += count

                total_cases += count

        # バースト確率を計算
        return round((burst_cases / total_cases), 2) if total_cases > 0 else 0.0
