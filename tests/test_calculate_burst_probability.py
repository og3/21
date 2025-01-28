import pytest
from collections import Counter
from calculate_burst_probability import CalculateBurstProbability


def test_calculate_burst_probability_basic_case():
    player_hand = ["?", 1, 2, 10]  # Visible score: 13
    deck = [7, 8, 9, 11]  # Hidden card possibilities
    expected = 1.0  # All combinations lead to burst
    result = CalculateBurstProbability.calculate_burst_probability(player_hand, deck)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_calculate_burst_probability_no_burst():
    player_hand = ["?", 1, 2]
    deck = [3, 4, 5, 6]
    expected = 0.0  # No possible card causes burst
    result = CalculateBurstProbability.calculate_burst_probability(player_hand, deck)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_calculate_burst_probability_full_deck():
    player_hand = ["?", 5, 6]  # Visible score: 11
    deck = [1, 2, 3, 4, 7, 8, 9, 10, 11]
    expected = 0.67  # Based on manual calculation
    result = CalculateBurstProbability.calculate_burst_probability(player_hand, deck)
    assert round(result, 2) == expected, f"Expected {expected}, but got {result}"


def test_calculate_burst_probability_empty_deck():
    player_hand = ["?", 1, 2]
    deck = []  # No cards in the deck
    expected = 0.0  # No cards to draw means no burst chance
    result = CalculateBurstProbability.calculate_burst_probability(player_hand, deck)
    assert result == expected, f"Expected {expected}, but got {result}"
