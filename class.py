from abc import ABC, abstractmethod
from typing import Dict


class Storage(ABC):
    @abstractmethod
    def add(self, product, number):
        pass

    @abstractmethod
    def remove(self, product, number):
       pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def get_unique_items_count(self):
        pass


class Store(Storage):
    def __init__(self, items={}, capacity=100):
        self.items = items
        self.capacity = capacity  # Вместимость

    def add(self, product, number):
        if self.__check_item(product):
            if sum(self.items.values()) < self.get_free_space():
                self.items[product] += number
            return 'Нет места'

    def remove(self, product, number):
        if self.items[product] >= number:
            self.items[product] -= number
        else:
            self.items.pop(product)

    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items.keys())

    def __check_item(self, product):
        return product in self.items

class Shop(Storage):
    def __init__(self, items={}, capacity=20):
        self.items = items
        self.capacity = capacity

    def add(self, product, number):
        if self.__check_item(product):
            if sum(self.items.values()) < self.get_free_space() and len(self.items.keys()) < 5:
                self.items[product] += number
            return 'Нет места'
        else:
            if sum(self.items.values()) < self.get_free_space() and len(self.items.keys()) < 5:
                self.items[product] = number
            return 'Нет места'

    def remove(self, product, number):
        if self.items[product] >= number:
            self.items[product] -= number
        else:
            self.items.pop(product)

    def get_free_space(self):
        return self.capacity - sum(self.items.values())

    def get_items(self):
        return self.items

    def get_unique_items_count(self):
        return len(self.items.keys())

    def __check_item(self, product):
        return product in self.items


class Request:
    def __init__(self, request_str):
        request_list = request_str.split()
        action = request_list[0]
        self.__number = int(request_list[1])
        self.__number = request_list[2]
        if action == "доставить":
            self.__from = self.cast(request_list[4])
            self.__to = self.cast(request_list[6])
        elif action == "забрать":
            self.__from = self.cast(request_list[4])
            self.__to = None
        elif action == "привезти":
            self.__from = None
            self.__to = self.cast(request_list[4])

    def cast(self, word):
        if 'склад' in word:
            return "storage" + word[5:]
        if 'магазин' in word:
            return "shop" + word[7:]

    def move(self):
        if self.__to and self.__from:
            if eval(self.__from).remove(self.__number, self.__number):
                eval(self.__to).add(self.__number, self.__number)
        elif self.__to:
            eval(self.__to).add(self.__number, self.__number)
        elif self.__from:
            eval(self.__from).remove(self.__number, self.__number)


storage_1 = Store(items={})
storage_1.add('печеньки', 5)
storage_1.add('печеньки', 5)
storage_1.add('носки', 26)
storage_2 = Store(items={})
storage_2.add('печеньки', 25)
storage_2.add("собачки", 35)
storage_2.add('носки', 35)
shop_1 = Shop(items={})
shop_1.add('печеньки', 5)
shop_1.add("собачки", 1)
shop_1.add('носки', 3)
shop_1.add('бананы', 3)
shop_2 = Shop(items={})
shop_2.add("собачки", 5)
shop_2.add("коробки", 4)
shop_2.add("бананы", 11)

print("Привет!")

while True:
    print("Текущее наличие мест")
    print(f"СКЛАД_1: {storage_1}\nСКЛАД_2: {storage_2}\nМАГАЗИН_1: {shop_1}\nМАГАЗИН_2: {shop_2}")
    print(f"Команда 1: Доставить ___ из ___ в ___;\nКоманда 2: Забрать ___ из ___;\nКоманда 3: Привезти ___ на ___;")
    print("Вставьте вместо нижних подчёркиваний выбранные слова!")
    print("'_'            - любое число;\n'__'           - одно из слов: 'носки', 'собачки', 'коробки', 'бананы'"
          "\n'___' и '____' - одно из слов: 'склад_1', 'склад_2', 'магазин_1', 'магазин_2'")

    user_text = (input("Выберите команду и вставьте нужные слова!:\n")).lower()

    if user_text == "стоп":
        break
    else:
        try:
            req = Request(user_text)
            req.move()
        except Exception as e:
            print(f"Ошибка {e}, повторите попытку")