"""
Списки
"""

__author__ = 'Игнатьев И.В.'

# Выведите все элементы, которые меньше 5
numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9]
print([number for number in numbers if number < 5])

# Объедините 2 списка так, чтобы в итоге получился 1 список включающий элементы обоих
first_list = [1, 2, 3, 4, 5]
second_list = [6, 7, 8, 9, 0]
result_list = first_list + second_list
print(result_list)

# Удалите дубликаты из списка
elems = [1, 2, 3, 4, 5, 6, 7, 8, 9, 1, 2, 3, 4, 5, -1, -2, -3]
# Вариант 1: порядок не нужно сохранять
res_list1 = list(set(elems))
print(res_list1)

# Вариант 2: порядок нужно сохранять
res_list2 = []
for elem in elems:
    if elem not in res_list2:
        res_list2.append(elem)
print(res_list2)

# Посчитайте количество символов в списке и выведите цифры. A: 5, B: 3, C: 1
elems = ['A', 'B', 'C', 'D', 'A', 'M', 'K']
count_dict = dict.fromkeys(elems, 0)
for elem in elems:
    count_dict[elem] += 1
print(', '.join(['{}: {}'.format(key, count_dict[key]) for key in count_dict]))

# Сделайте проверку, явдяется ли слово Палиндромом
def palindrom(word: str) -> bool:
    if not word:
        return False
    return word == word[::-1]

words = ['', 'asddsa', 'asdsa', 'asd', 'asdf']
for word in words:
    print('"{}" - {}палиндром'.format(word, 'не ' if not palindrom(word) else ''))

# Выведите список элементов, которые есть в первом списке, но нет во втором
list1 = [1, 2, 3, 4, 5, 6, 7]
list2 = [4, 5, 6, 7, 8, 9]
print(set(list1) - set(list2))

# Проверьте, повторяются ли символы в строке
string = 'asdfg' #'asdfgasdf' # 'asdfg'
print(len(string) == len(set(string)))

# Найдите и выведите наиболее и наимее часто встречающеся слова в строке
import re
string = 'Один два три. Четыре пять,шесть семь:восемь девять десять. Четыре, три, три, ноль.'
words = re.findall(r'\w+', string)
count_dict = dict.fromkeys(words, 0)
for word in words:
    if word not in count_dict:
        count_dict[word] = 0
    count_dict[word] += 1

print('Max: {}'.format([word for word in count_dict if count_dict[word] == max(count_dict.values())]))
print('Min: {}'.format([word for word in count_dict if count_dict[word] == min(count_dict.values())]))

# На вход получаете 2 списка, выведите новый список с элементами первого, которых нет во втором
list1 = [1, 2, 3, 4, 5, 6, 7]
list2 = [1, 3, 5, 6, 9, 10]
print([set(list1) - set(list2)])

# Исключения
# Посчитайте сумму всех чисел в списке. В списке могут быть строки
numbers = [1, 2, 3, '4', 'asdf', '789', 15.5]
numbers_sum = 0
for number in numbers:
    try:
        numbers_sum += float(number)
    except ValueError:
        pass
print(numbers_sum)

# Получите из списка не существующий индекс и вместо ошибки напечатайте: Объекта не существует
elems = [1, 2, 3, 4, 5]
idx = 100
try:
    print(elems[idx])
except IndexError:
    print('Объект не существует')

# Из списка выведите список цифр и список строк, которые в нем содержатся isinstance()
elems = [1, 2, 3, 100, 99, '123', 'computer', 'python', 5]
print([elem for elem in elems if isinstance(elem, int) and 0 <= elem <= 9])
print([elem for elem in elems if isinstance(elem, str)])
