"""
Ввод/вывод данных
"""

__author__ = 'Игнатьев И.В.'

from lotto_game.cards import Card
from lotto_game.constants import X_NUMBER


class InputOutput:
    """
    Ввод/вывод
    """
    @staticmethod
    def get_step(number):
        """
        Ввод хода человека
        :param number: число
        :return: есть ли число на карточке
        """
        while True:
            InputOutput.print_message(f'Число {number} есть на карточке? Введите +/-:')
            answer = input()
            if answer in ['+', '-']:
                break

        return answer == '+'

    @staticmethod
    def print_message(message):
        """
        Вывод сообщения на экран
        :param message: сообщение
        """
        print(f'\n{message}')

    @staticmethod
    def print_card(card: Card):
        """
        Выводит карточку на экран
        :param card: карточка
        """
        for row in card.numbers:
            print('  '.join([(str(number) if number != X_NUMBER else 'X').rjust(2) if number is not None
                             else ' .' for number in row]))
