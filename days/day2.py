from typing import Iterable, Tuple
from days.local_functools import chain_functions

"""
Rock Paper Scissors
"""
ROCK = "rock"
PAPER = "paper"
SCISSORS = "scissors"

PLAY_SCORE = {
    ROCK: 1,
    PAPER: 2,
    SCISSORS: 3
}

WIN = "win"
DRAW = "draw"
LOSE = "lose"

OUTCOME_SCORE = {
    WIN: 6,
    DRAW: 3,
    LOSE: 0
}

OPPONENT_ENCODINGS = {
    "A": ROCK,
    "B": PAPER,
    "C": SCISSORS
}

USER_ENCODINGS = {
    "X": ROCK,
    "Y": PAPER,
    "Z": SCISSORS
}

RECOMMENDED_PLAYS = {
    "X": LOSE,
    "Y": DRAW,
    "Z": WIN
}

BEATS = {
    ROCK: SCISSORS,
    PAPER: ROCK,
    SCISSORS: PAPER
}

LOSES = {
    ROCK: PAPER,
    PAPER: SCISSORS,
    SCISSORS: ROCK
}


def part_1(encrypted_strategy_guide: list[str]) -> str:
    return chain_functions(encrypted_strategy_guide, decrypt, score, sum, str)


def decrypt(encrypted_strategy_guide: list[str]) -> Iterable[Tuple[str, str]]:
    def decrypter(value: str) -> (str, str):
        split = value.split(" ")
        return OPPONENT_ENCODINGS[split[0]], USER_ENCODINGS[split[1]]

    return map(decrypter, map(lambda s: s.strip(), encrypted_strategy_guide))


"""
A user gets points both for wining or drawing and for the play (scissors, rock, paper).
"""


def score(decrypted_strategy_guide: Iterable[Tuple[str, str]]) -> Iterable[int]:
    def play_scorer(match: (str, str)) -> int:
        return PLAY_SCORE[match[1]]

    def match_evaluator(match: (str, str)) -> str:
        opponent_play, user_play = match
        if opponent_play == user_play:
            return DRAW
        elif BEATS[user_play] == opponent_play:
            return WIN
        else:
            return LOSE

    def evaluated_match_scorer(outcome: str) -> int:
        return OUTCOME_SCORE[outcome]

    return map(lambda match: play_scorer(match) + evaluated_match_scorer(match_evaluator(match)),
               decrypted_strategy_guide)


def part_2(encrypted_strategy_guide: list[str]) -> str:
    return chain_functions(encrypted_strategy_guide, decrypt_correctly, score_correctly, sum, str)


def decrypt_correctly(encrypted_strategy_guide: list[str]) -> Iterable[Tuple[str, str]]:
    def decrypter(encrypted: str) -> (str, str):
        opponent_encoded, recommend_play_encoded = encrypted.split(" ")
        return OPPONENT_ENCODINGS[opponent_encoded], RECOMMENDED_PLAYS[recommend_play_encoded]

    return map(decrypter, map(lambda s: s.strip(), encrypted_strategy_guide))


"""
After speaking with the elf further, we know that the input is actually telling
us what outcome (win, lose, draw) we must achieve. This scorer still scores the same,
but first learns what play the user should select and then scores the outcome as well.
"""


def score_correctly(encrypted_strategy_guide: Iterable[Tuple[str, str]]) -> Iterable[int]:
    def get_play(play_and_outcome: (str, str)) -> str:
        play, outcome = play_and_outcome
        return play if outcome == DRAW else BEATS[play] if outcome == LOSE else LOSES[play]

    def scorer(play_and_outcome: (str, str)) -> int:
        user_play = get_play(play_and_outcome)
        outcome = play_and_outcome[1]
        return OUTCOME_SCORE[outcome] + PLAY_SCORE[user_play]

    return map(scorer, encrypted_strategy_guide)
