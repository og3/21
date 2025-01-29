import random
import pandas as pd
from npc_think_patterns import NpcThinkPattern

MAX_SCORE = 21
MAX_LIFE_POINTS = 5
# ゲーム開始時にカードを2枚ずつ引くのでゲーム中は最大8枚
MAX_DECK_CARDS = 8


def generate_data_with_styles(num_samples=1000, weights=(7, 1, 2)):
    """
    プレイスタイルの割合を指定してデータを生成する。
    weights は (ディフェンス, オフェンス, 協調) の比率。
    """
    data = []
    styles = ["defensive", "offensive", "cooperative"]

    for _ in range(num_samples):
        # ラウンド情報をランダムに生成
        round_number = random.randint(1, 7)
        player_score = random.randint(1, MAX_SCORE)
        opponent_score = random.randint(1, MAX_SCORE)
        player_burst_prob = random.uniform(0, 1)
        opponent_burst_prob = random.uniform(0, 1)
        remaining_cards_num = random.randint(1, MAX_DECK_CARDS)
        player_life = random.randint(1, MAX_LIFE_POINTS)
        opponent_life = random.randint(1, MAX_LIFE_POINTS)

        # スコア差を計算
        score_difference = abs(
            (MAX_SCORE - player_score) - (MAX_SCORE - opponent_score)
        )

        # プレイスタイルを重みに基づいて選択
        style = random.choices(styles, weights=weights)[0]

        # プレイスタイルごとの行動ルール
        if style == "defensive":
            draw_card = NpcThinkPattern.should_draw_defensive(
                opponent_burst_prob,
                player_burst_prob,
                round_number,
                remaining_cards_num,
                player_life,
            )
        elif style == "offensive":
            draw_card = NpcThinkPattern.should_draw_offensive(
                player_burst_prob,
                score_difference,
                round_number,
                remaining_cards_num,
                player_life,
                opponent_life,
            )
        elif style == "cooperative":
            draw_card = NpcThinkPattern.should_draw_cooperative(
                player_burst_prob,
                opponent_burst_prob,
                round_number,
                remaining_cards_num,
                opponent_life,
            )
        else:
            draw_card = False  # デフォルト

        # データ行を追加
        data.append(
            {
                "score_difference": score_difference,
                "player_burst_prob": round(player_burst_prob, 2),
                "opponent_burst_prob": round(opponent_burst_prob, 2),
                "remaining_cards_num": remaining_cards_num,
                "round": round_number,
                "player_life": player_life,
                "opponent_life": opponent_life,
                "draw_card": draw_card,
            }
        )

    return pd.DataFrame(data)


# データ生成の例（ディフェンス: 7, オフェンス: 1, 協調: 2 の割合）
style_data = generate_data_with_styles(1000, weights=(7, 1, 2))

# データを保存または表示
style_data.to_csv("npc_style_data.csv", index=False)
print(style_data.head())
