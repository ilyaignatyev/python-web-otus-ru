"""
Игроки (компьютер, человек)
"""

__author__ = 'Игнатьев И.В.'

from abc import ABC, abstractmethod
import random

from lotto_game.cards import Card
from lotto_game.constants import COMPUTER_MISTAKE_CHANCE
from lotto_game.input_output import InputOutput


class Player(ABC):
    """
    Игрок
    """
    __id = 0

    def __init__(self, name: str):
        self.__numbers = None
        self.__card = None
        self.__id = self.__next_id()
        self.__name = name

    def get_name(self) -> str:
        """
        Возвращает имя игрока
        :return: Имя
        """
        return self.__name

    @property
    def card(self) -> Card:
        """
        Возвращает карточку игрока
        :return: Карточка
        """
        return self.__card

    @card.setter
    def card(self, card: Card):
        """
        Устанавливает карточку
        :param card:
        :return:
        """
        self.__card = card

    @property
    def id(self) -> int:
        """
        Возвращает идентификатор игрока
        :return: Идентификатор
        """
        return self.__id

    @staticmethod
    def __next_id() -> int:
        """
        Возвращает следующий идентификатор и увеличивает счетчик на 1
        :return: Идентификатор
        """
        Player.__id += 1
        return Player.__id

    @abstractmethod
    def make_step(self, number) -> bool:
        """
        Ход
        :param number: Число
        :return: Закрашивает или нет
        """


class Person(Player):
    """
    Человек-игрок
    """
    def make_step(self, number) -> bool:
        """
        Ход человека
        :param number: Число
        :return: Закрашивает или нет
        """
        step = InputOutput.get_step(number)
        if step:
            self.card.mark_number(number)
        return step


class Computer(Player):
    """
    Компьютер-игрок
    """
    def make_step(self, number):
        """
        Ход
        :param number: Выпавшее число
        :return: Закрашивает или нет
        """
        contains = self.card.contains(number)
        step = not contains if random.randint(1, 100 // COMPUTER_MISTAKE_CHANCE) == 1 else contains
        if step:
            self.card.mark_number(number)
        return step
