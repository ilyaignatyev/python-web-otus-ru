"""
Игровой процесс
"""

__author__ = 'Игнатьев И.В.'

import random

from lotto_game.constants import COMPUTER_MISTAKE_CHANCE, PERSON_COUNT, COMPUTER_COUNT
from lotto_game.input_output import InputOutput
from lotto_game.master import Master
from lotto_game.players import Person, Computer


class Game:
    """
    Игра
    """
    def __init__(self, person_count=PERSON_COUNT, computer_count=COMPUTER_COUNT, input_output=InputOutput,
                 computer_mistake_chance=COMPUTER_MISTAKE_CHANCE):
        """
        :param person_count: Количество игроков-человек
        :param computer_count: Количество игроков-компьютеров
        :param input_output: Класс ввода/вывода
        :param computer_mistake_chance: Вероятность совершить игроку-компьютеру ошибку
        """
        self.__person_count = person_count
        self.__computer_count = computer_count
        self.__input_output = input_output
        self.__computer_mistake_chance = computer_mistake_chance

    def play(self) -> dict:
        """
        Игровой процесс
        :return: Выигравшие/проигравшие игроки
        """
        # Создаем ведущего
        master = Master()

        # Создаем игроков
        players = []
        for person_idx in range(self.__person_count):
            name = f'Человек' + (f' {person_idx + 1}' if self.__person_count > 1 else '')
            players.append(Person(name, self.__input_output))

        for computer_idx in range(self.__computer_count):
            name = 'Компьютер' + (f' {computer_idx + 1}' if self.__computer_count > 1 else '')
            players.append(Computer(name, self.__computer_mistake_chance))

        # Определяем порядок ходов
        random.shuffle(players)

        # Выдаем игрокам карточки
        for player in players:
            master.give_card(player)

        result = {'mistake': [], 'win': []}

        # Последовательно ведущий достает очередное число, пока числа не кончатся либо кто-нибудь не проиграет
        # либо кто-нибудь не выиграет
        for number in master.get_number_sequence():
            game_over = False

            for player in players:
                # Игрок делает ход
                if self.__input_output:
                    self.__input_output.print_message(f'Номер: {number}, ходит {player.get_name()}:')
                    self.__input_output.print_card(player.card)

                step = player.make_step(number)

                if self.__input_output:
                    self.__input_output.print_message(f'Ход: {"+" if step else "-"}')
                    if step:
                        self.__input_output.print_card(player.card)

                # Ведущий проверяет ход на наличие ошибки
                step_result = master.check_step(player, number, step)
                if step_result['mistake']:
                    # В случае ошибки игра сразу завершается
                    result['mistake'].append(player)
                    for other_player in players:
                        if other_player != player:
                            result['win'].append(other_player)
                    game_over = True
                    break

                if step_result['win']:
                    # При выигрыше одного из игроков даем завершить ход остальным игрокам (обработать выпавщее число)
                    result['win'].append(player)
                    game_over = True

            # Завершаем игру, если кто-то проиграл или выиграл
            if game_over:
                break

        if self.__input_output:
            for player in result['mistake']:
                self.__input_output.print_message(f'Игрок {player.get_name()} проиграл из-за ошибки.')

            for player in result['win']:
                self.__input_output.print_message(f'Игрок {player.get_name()} выиграл.')

        return result
