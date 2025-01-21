import pytest
from game21 import Game21, Effect
import itertools


@pytest.fixture
def game():
    return Game21()


def test_initialization(game):
    assert game.player.life == Game21.INITIAL_LIFE
    assert game.opponent.life == Game21.INITIAL_LIFE
    assert game.round_number == Game21.INITIAL_ROUND_NUMBER
    assert len(game.deck) == 11
    assert game.player.hand == []
    assert game.opponent.hand == []


def test_reset_round(game):
    game.reset_round()
    assert len(game.deck) == 11
    assert game.player.hand == []
    assert game.opponent.hand == []


def test_draw_card(game):
    card = game.draw_card(game.player.hand, "Player", silent=True)
    assert card in range(1, 12)
    assert len(game.player.hand) == 1
    assert len(game.deck) == 10

    empty_deck_game = Game21()
    empty_deck_game.deck = []
    card = empty_deck_game.draw_card(empty_deck_game.player.hand, "Player", silent=True)
    assert card is None


def test_deal_initial_cards(game):
    game.deal_initial_cards(game.player.hand, "Player")
    assert len(game.player.hand) == Game21.INITIAL_CARDS
    assert len(game.deck) == 11 - Game21.INITIAL_CARDS


def test_increment_round_number(game):
    game.increment_round_number()
    assert game.round_number == 1


def test_calculate_score(game):
    game.player.hand = [5, 6, 7]
    assert game.calculate_score(game.player.hand) == 18


def test_calculate_score_excluding_first(game):
    game.player.hand = [5, 6, 7]
    assert game.calculate_score_excluding_first(game.player.hand) == 13


def test_show_hand(game):
    game.player.hand = [5, 6, 7]
    assert game.show_hand(game.player.hand) == "['?', 6, 7] (合計: ?+13/21)"
    assert game.show_hand([]) == "[]"


def test_opponent_turn(game):
    game.opponent.hand = [5]
    game.opponent_turn()
    assert (
        len(game.opponent.hand) > 1
        or game.calculate_score(game.opponent.hand) >= Game21.MIN_OPPONENT_DRAW_SCORE
    )


def test_check_winner(game):
    game.player.hand = [10, 7]
    game.opponent.hand = [9, 6]
    assert game.check_winner() == "player"

    game.player.hand = [10, 2]
    assert game.check_winner() == "opponent"

    game.player.hand = [10, 7]
    game.opponent.hand = [10, 7]
    assert game.check_winner() == "draw"


def test_play_round(game, mocker):
    mocker.patch.object(Game21, "get_player_input", return_value="n")
    result = game.play_round()
    assert result in ["player", "opponent", "draw"]


def test_display_logo(mocker):
    mocker.patch("builtins.open", mocker.mock_open(read_data="Game 21 Logo"))
    assert Effect.display_logo("game_21") is None

    mocker.patch("builtins.open", side_effect=FileNotFoundError)
    assert Effect.display_logo("missing") == "Error: ファイルが見つかりません。"

    mocker.patch("builtins.open", side_effect=Exception("Test Error"))
    assert Effect.display_logo("error") == "Error: Test Error"


def test_play_game_lifecycle(game, mocker):
    mocker.patch.object(Game21, "get_player_input", side_effect=itertools.cycle(["n"]))
    game.player.life = 1
    game.opponent.life = 1
    game.play_game()
    assert game.player.life == 0 or game.opponent.life == 0
