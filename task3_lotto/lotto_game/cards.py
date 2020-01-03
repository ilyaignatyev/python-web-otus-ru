"""
Модуль для работы с карточками
"""

__author__ = 'Игнатьев И.В.'

import copy
import random

from lotto_game.constants import MIN_NUMBER, MAX_NUMBER, CARD_ROW_COUNT, CARD_COL_COUNT, X_NUMBER, NUMBERS_IN_ROW


class Card:
    """
    Карточка
    """
    def __init__(self, numbers):
        # Числа, двумерный массив
        self.__numbers = copy.deepcopy(numbers)

    @property
    def numbers(self) -> list:
        """
        Возвращает числа на карточке
        :return: Числа
        """
        return self.__numbers

    @property
    def numbers_set(self) -> set:
        """
        Возвращает множество чисел на карточке
        :return: Числа
        """
        return set(number for row in self.__numbers for number in row if number is not None)

    def contains(self, number: int) -> bool:
        """
        Сожержит ли карточка число
        :param number: Число
        :return: Содержит ли его
        """
        return number in self.numbers_set

    def mark_number(self, number: int):
        """
        Закрашивает число на карточке
        :param number: Число
        """
        for row in range(CARD_ROW_COUNT):
            for col in range(CARD_COL_COUNT):
                if self.__numbers[row][col] == number:
                    self.__numbers[row][col] = X_NUMBER

    @staticmethod
    def get_copy(card):
        """
        Возвращает копию карточки
        :param card: Карточка
        :return: Копия карточки
        """
        return Card(card.numbers)


class Cards:
    """
    Хранит карточки и генерирует новые карточки.
    """
    def __init__(self):
        self.__cards = []

    def get_card(self):
        """
        Генерация карточки
        3 строки, 9 столбцов. 5 чисел в каждой строке. Карточки не должны повторяться.
        :return: Новая карточка
        """
        while True:
            card = []
            for row in range(CARD_ROW_COUNT):
                card.append([None] * CARD_COL_COUNT)
            used_numbers = []
            for row in range(CARD_ROW_COUNT):
                col_filled = 0
                while col_filled <= NUMBERS_IN_ROW:
                    number = random.randint(MIN_NUMBER, MAX_NUMBER)
                    if number not in used_numbers:
                        used_numbers.append(number)
                        col_filled += 1
                        # Распределяем числа по столбцам десятками:
                        # 1 столбец - от 1 до 9, 2-ой - от 10 до 19, и т.д. В последний столбец помещаем все числа,
                        # которые не влезают в заданное количество столбцов.
                        column = (number // 10) if number < CARD_COL_COUNT * 10 else (CARD_COL_COUNT - 1)
                        card[row][column] = number

            exists_similar = False
            for existing_card in self.__cards:
                if self.__similar_cards(card, existing_card):
                    exists_similar = True
                    break

            if not exists_similar:
                break

        return Card(card)

    @staticmethod
    def __similar_cards(card1, card2) -> bool:
        """
        Сравнивает 2 карточки
        :param card1: Карточка 1
        :param card2: Карточка 2
        :return: Одинаковые или нет
        """
        if [card1[row][col] for row in range(CARD_ROW_COUNT) for col in range(CARD_COL_COUNT)] == \
                [card2[row][col] for row in range(CARD_ROW_COUNT) for col in range(CARD_COL_COUNT)]:
            return True
        return False
