"""
Тесты
"""

import pytest

from lotto_game import Game
from lotto_game.cards import Cards, Card
from lotto_game.constants import MIN_NUMBER, MAX_NUMBER, CARD_ROW_COUNT, CARD_COL_COUNT, NUMBERS_IN_ROW, \
    COMPUTER_MISTAKE_CHANCE
from lotto_game.input_output import InputOutput
from lotto_game.master import Master
from lotto_game.players import Person, Computer


@pytest.fixture(scope='module')
def master() -> Master:
    """
    Создает ведущего
    :return: Ведущий
    """
    return Master()


@pytest.fixture(scope='module')
def person() -> Person:
    """
    Создает игрока-человека
    :return: Игрок-человек
    """
    return Person('Человек', input_output=InputOutput)


@pytest.fixture(scope='module')
def computer() -> Computer:
    """
    Создает игрока-компьютера
    :return: Игрок-компьютер
    """
    return Computer('Компьютер', mistake_chance=COMPUTER_MISTAKE_CHANCE)


def test_cards():
    """
    Проверяет карточки
    :param cards: Карточки
    """
    cards = Cards()
    card1 = cards.get_card()
    card2 = cards.get_card()

    for card in (card1, card2):
        # Карточка сгенерирована
        assert card is not None

        # Множество чисел на карточке
        assert card.numbers_set == set(number for row in card.numbers for number in row if number is not None)
        assert len(card.numbers_set) == CARD_ROW_COUNT * NUMBERS_IN_ROW

        # Количество строк
        assert len(card.numbers) == CARD_ROW_COUNT

        for row in card.numbers:
            # Количество столбцов
            assert len(row) == CARD_COL_COUNT

            for number in row:
                # Элементы попадают в интервал
                assert MIN_NUMBER <= number <= MAX_NUMBER if number is not None else True

                # Карточка содержит число
                assert card.contains(number) if number is not None else True

        # Закраска числа
        number = list(card.numbers_set)[0]
        card.mark_number(number)
        assert number not in card.numbers_set

        # Копирование карточки
        card_copy = Card.get_copy(card)
        assert id(card_copy) != id(card)
        assert id(card_copy.numbers) != id(card.numbers)
        assert card_copy.numbers_set == card.numbers_set
        for row1, row2 in zip(card.numbers, card_copy.numbers):
            for number1, number2 in zip(row1, row2):
                assert number1 == number2

    # Неравенство карточек
    assert card1.numbers_set != card2.numbers_set


def test_master_numbers(master):
    """
    Проверяет последовательность чисел, произодимую ведущим
    :param master: Ведущий
    """
    numbers = set(master.get_number_sequence())
    assert len(numbers) == MAX_NUMBER - MIN_NUMBER + 1
    for number in numbers:
        assert MIN_NUMBER <= number <= MAX_NUMBER


def test_master_player_cards(master, person, computer):
    """
    Проверяет соответствие карточек у игроков и ведущего и отличие карточк у игроков
    :param master: Ведущий
    :param person: Игрок-человек
    :param computer: Игрок-компьютер
    """
    master.give_card(person)
    master.give_card(computer)
    assert person.card.numbers_set != computer.card.numbers_set
    master_cards = master.player_cards
    assert master_cards[person.id].numbers_set == person.card.numbers_set
    assert master_cards[computer.id].numbers_set == computer.card.numbers_set


def test_check_step(master, person, computer):
    """
    Проверяет корректность проверки хода игрока ведущим
    :param master: Ведущий
    :param person: Игрок-человек
    :param computer: Игрок-компьютер
    """
    for player in (person, computer):
        master.give_card(player)
        numbers = list(player.card.numbers_set)

        # Число есть на карточке игрока, игрок ходит "+"
        check_result = master.check_step(player, numbers[0], True)
        assert not check_result['mistake']

        # Число есть на карточке игрока, игрок ходит "-"
        check_result = master.check_step(player, numbers[0], False)
        assert check_result['mistake']

        # Числа нет на карточке игрока, игрок ходит "+"
        check_result = master.check_step(player, MAX_NUMBER + 1, True)
        assert check_result['mistake']

        # Числа нет на карточке игрока, игрок ходит "-"
        check_result = master.check_step(player, MAX_NUMBER + 1, False)
        assert not check_result['mistake']


def test_check_fail_win():
    """
    Тест проигрыша.выигрыша, игра 2х компьютеров.
    """
    # Выиграет один или оба
    game = Game(person_count=0, computer_count=2, computer_mistake_chance=0, input_output=None)
    game_result = game.play()
    assert len(game_result['win']) in (1, 2)
    assert len(game_result['mistake']) == 0

    # Один проиграет из-за ошибки, второй из-за этого выиграет
    game = Game(person_count=0, computer_count=2, computer_mistake_chance=100, input_output=None)
    game_result = game.play()
    assert len(game_result['win']) == 1
    assert len(game_result['mistake']) == 1
