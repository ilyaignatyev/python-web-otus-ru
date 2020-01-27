from task3_lotto.lotto_game import game
game()

# print('Введите строку поиска: ')
# search_string = input()
#
# while True:
#     print('Выберите поисковую систему: 1 - yandex.ru, 2 - google.ru:')
#     site_str = input()
#     site = int(site_str) if site_str.isdigit() else None
#     if site in [SEARCH_SITE_YANDEX, SEARCH_SITE_GOOGLE]:
#         break
#
# print('Введите количество результатов:')
# url_count = input()

# class A():
#     def __init__(self, price):
#         self.price = price
#
#     def __getattribute__(self, item):
#         print('getattribute0')
#         super().__getattribute__(item)
#
# class B(A):
#     def __init__(self, price):
#         super().__init__(price)
#
#     def __getattribute__(self, item):
#         super().__getattribute__(item)
#         print('getattribute')
#         # raise AttributeError
#         return 123
#
#     def __getattr__(self, item):
#         print('getattr')
#         return 1
#
#
# c = B(123)
# # print(c.price)
# print(c.asd)

# from abc import ABC, abstractmethod
# class P(ABC):
#     @abstractmethod
#     def get(self):
#         pass
#
# class R(P):
#     def get(self):
#         pass
#     pass

# c = R()
# class Model:
#     def __init__(self):
#         print('Model init')
#
#
# class ExtendedModel(Model):
#     def __init__(self):
#         print('Extended init')
#         super().__init__()
#
#
# class BaseMixin:
#     pass
#
#
# class ModelMixin(BaseMixin):
#     def __init__(self):
#         print('ModelMixin init')
#         super().__init__()
#
#
# class MyModel(ModelMixin, ExtendedModel):
#     pass
#
# # model_1 = ExtendedModel()
# model_1 = MyModel()
# print (MyModel.mro())
#
# class a:
#     def __init__(self):
#         print('init a')
#
# class b(a):
#     def __init__(self):
#         print('init b')
#         super().__init__()
#
# class c:
#     def __init__(self):
#         print('init c')
#         super().__init__()
#
# class d(c, b):
#     pass
#     # def __init__(self):
#     #     print('init d')
#
# m = d()
# print (d.mro())
