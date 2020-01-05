"""
Игроки (компьютер, человек)
"""

__author__ = 'Игнатьев И.В.'

from abc import ABC, abstractmethod
import random

from lotto_game.cards import Card
from lotto_game.constants import COMPUTER_MISTAKE_CHANCE


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


class NoInputOutput(Exception):
    """
    Исключение при отсутствии класса ввода-вывода
    """
    pass


class Person(Player):
    """
    Человек-игрок
    """
    def __init__(self, name, input_output):
        """
        :param name: Имя
        :param input_output: Класс ввода данных
        """
        super().__init__(name)
        self.__input_output = input_output

    def make_step(self, number) -> bool:
        """
        Ход человека
        :param number: Число
        :return: Закрашивает или нет
        """
        if self.__input_output is None:
            raise NoInputOutput('Не указан класс ввода-вывода данных.')
        step = self.__input_output.get_step(number)
        if step:
            self.card.mark_number(number)
        return step


class Computer(Player):
    """
    Компьютер-игрок
    """
    def __init__(self, name, mistake_chance):
        """
        :param name: Имя
        :param mistake_chance: Вероятность ошибки в процентах
        """
        super().__init__(name)
        self.__mistake_chance = mistake_chance

    def make_step(self, number):
        """
        Ход
        :param number: Выпавшее число
        :return: Закрашивает или нет
        """
        contains = self.card.contains(number)
        step = not contains if self.__mistake_chance and random.randint(1, 100 // self.__mistake_chance) == 1 \
            else contains
        if step:
            self.card.mark_number(number)
        return step
