# -*- coding: utf-8 -*-

from collections import namedtuple

Customer = namedtuple('Customer', 'name fidelity')

class LineItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price
    def total(self):
        return self.quantity * self.price

class Order:
    def __init__(self, customer, cart, promotion=None):
        self.customer = customer
        self.cart = list(cart)
        self.promotion = promotion
    def total(self):
        if not hasattr(self, '__total'):
            self.__total = sum(item.total() for item in self.cart)
        return self.__total
    def due(self):
        if self.promotion:
            return self.total() - self.promotion(self)
        else:
            return self.total()
    def __repr__(self):
        fmt = 'Order total {:.2f} due {:.2f}'
        return fmt.format(self.total(), self.due())

promos = []
def promotion(promo_func):
    promos.append(promo_func)
    return promo_func

@promotion
def fidelity(order):
    return order.total() * .05 if order.customer.fidelity >= 1000 else 0

@promotion
def bulk_item(order):
    discount = 0
    for item in order.cart:
        if item.quantity >= 20:
            discount += item.total() * .1
    return discount

@promotion
def large_order(order):
    distinct = {item.product for item in order.cart}
    if len(distinct) >= 10:
        return order.total() * .07
    return 0

def best_promo(order):
    return max(promo(order) for promo in promos)

joe = Customer('joe', 0)
ann = Customer('ann', 1000)
cart = [LineItem('apple', 10, .8), LineItem('banana', 20, 1), LineItem('watermallon', 2, 10)]
long_cart = [LineItem(str(code), 1, 1) for code in range(10)]
print(Order(joe, cart, best_promo))
print(Order(ann, cart, best_promo))
print(Order(ann, cart, bulk_item))
print(Order(ann, long_cart, best_promo))
print(Order(ann, long_cart, large_order))
