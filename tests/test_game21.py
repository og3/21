import pytest
from game21 import Game21

@pytest.fixture
def game():
    return Game21()

def test_initialization(game):
    # 初期化の確認
    assert game.player_life == Game21.INITIAL_LIFE
    assert game.opponent_life == Game21.INITIAL_LIFE
    assert len(game.deck) == 11  # 山札には1~11が1セット
    assert len(game.player_hand) == 0
    assert len(game.opponent_hand) == 0

def test_draw_card(game):
    # カードを引いた後の手札確認
    game.draw_card(game.player_hand, "TestPlayer", silent=True)
    assert len(game.player_hand) == 1

def test_calculate_score(game):
    # スコア計算の確認
    game.player_hand = [3, 4, 5]
    assert game.calculate_score(game.player_hand) == 12
    assert game.calculate_score_excluding_first(game.player_hand) == 9

def test_check_winner_draw(game):
    # 両者ともバーストした場合
    game.player_hand = [22]
    game.opponent_hand = [23]
    result = game.check_winner()
    assert result == "draw"

def test_check_winner_player_win(game):
    # プレイヤーの勝利
    game.player_hand = [20]
    game.opponent_hand = [19]
    result = game.check_winner()
    assert result == "player"

def test_check_winner_opponent_win(game):
    # 相手の勝利
    game.player_hand = [18]
    game.opponent_hand = [19]
    result = game.check_winner()
    assert result == "opponent"
