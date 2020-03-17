# -*- coding:utf-8 -*-
class Book:
    author = 'Alice'
    price = 30

    def set_price(self, price):
        self.price = price


book = Book()
book.set_price(40)
print(book.price)

