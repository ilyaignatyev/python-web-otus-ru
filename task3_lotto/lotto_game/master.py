"""
Ведущий
"""

__author__ = 'Игнатьев И.В.'

import random

from lotto_game.cards import Cards, Card
from lotto_game.constants import MIN_NUMBER, MAX_NUMBER
from lotto_game.players import Player


class Master:
    """
    Ведущий. Генерирует последовательность выпавших чисел. Раздает карточки игрокам. Проверяет ходы.
    """
    def __init__(self):
        # Номера, которые еще не выпали
        self.__numbers = None

        # Выпавшие номера
        self.__played_numbers = []

        # Карточки
        self.__cards = Cards()
        self.__player_cards = {}

    @property
    def player_cards(self) -> dict:
        """
        Возвращает карточки игроков
        :return: Карточки
        """
        return self.__player_cards

    def get_number_sequence(self):
        """
        Генератор последовательности чисел
        """
        self.__numbers = list(range(MIN_NUMBER, MAX_NUMBER + 1))
        while self.__numbers:
            idx = random.randint(0, len(self.__numbers) - 1)
            number = self.__numbers[idx]
            self.__numbers.pop(idx)
            self.__played_numbers.append(number)
            yield number

    def give_card(self, player: Player):
        """
        Выдает карточку игроку
        :param player: Игрок
        """
        card = self.__cards.get_card()
        player.card = card
        self.__player_cards[player.id] = Card.get_copy(card)

    def check_step(self, player: Player, number: int, step: bool) -> dict:
        """
        Проверяет ход игрока (выиграл/совершил ошибку/нейтральный ход).
        :param player: Игрок
        :param number: Выпавшее число
        :param step: Ход
        :return: Результат хода:
                    mistake (bool) - совершил ошибку
                    win (bool) - выиграл
        """
        card = self.__player_cards[player.id]
        card_contains_number = card.contains(number)
        return {
            'mistake': step and not card_contains_number or not step and card_contains_number,
            'win': not (card.numbers_set - set(self.__played_numbers))
        }
