"""
Игровой процесс
"""

__author__ = 'Игнатьев И.В.'

import random
from lotto_game.master import Master
from lotto_game.players import Person, Computer
from lotto_game.input_output import InputOutput


def game():
    """
    Игровой процесс
    """
    # Создаем ведущего
    master = Master()

    # Создаем игроков
    person = Person('Человек')
    computer = Computer('Компьютер')

    # Выдаем игрокам карточки
    master.give_card(person)
    master.give_card(computer)

    # Определяем кто первый будет ходить
    players = [person, computer]
    random.shuffle(players)

    # Последовательно ведущий достает очередное число, пока числа не кончатся либо кто-нибудь не выиграет
    # либо кто-нибудь не проиграет
    for number in master.get_number_sequence():
        InputOutput.print_message(f'Номер: {number}')
        game_over = False

        for player in players:
            player_name = player.get_name()

            # Игрок делает ход
            InputOutput.print_message(f'Ходит {player_name}:')
            InputOutput.print_card(player.card)
            step = player.make_step(number)
            InputOutput.print_message(f'Ход: {"+" if step else "-"}')
            InputOutput.print_card(player.card)

            # Ведущий проверяет ход на наличие ошибки
            step_result = master.check_step(player, number, step)
            if step_result['mistake']:
                InputOutput.print_message(f'Игрок {player_name} проиграл из-за ошибки.')
                return

            if step_result['win']:
                InputOutput.print_message(f'Игрок {player_name} выиграл.')
                game_over = True

        # Завершаем игру, если кто-то проиграл или выиграл
        if game_over:
            break
