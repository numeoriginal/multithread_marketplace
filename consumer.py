"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread
import json


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):

        super(Consumer, self).__init__()
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs
        #print(carts)
        #print(kwargs)
        """
        Constructor.

        :type carts: List
        :param carts: a list of add and remove operations

        :type marketplace: Marketplace
        :param marketplace: a reference to the marketplace

        :type retry_wait_time: Time
        :param retry_wait_time: the number of seconds that a producer must wait
        until the Marketplace becomes available

        :type kwargs:
        :param kwargs: other arguments that are passed to the Thread's __init__()
        """

    def run(self):
        self.cart_id = self.marketplace.new_cart()
        #print(self.cart_id)
        for el in self.carts:
            for action in el:
                if action['type'] == 'add':
                    #print("Add command")
                    for _ in range(action['quantity']):
                        approved = self.marketplace.add_to_cart(self.cart_id, action['product'])
                        while not approved:
                            time.sleep(self.retry_wait_time)
                            approved = self.marketplace.add_to_cart(self.cart_id, action['product'])
                else:
                    for _ in range(action['quantity']):
                        pass
                        self.marketplace.remove_from_cart(self.cart_id, action['product'])
                    #print("Remove command")

        cart = self.marketplace.place_order(self.cart_id)
        for i in range(len(cart)):
            print(self.kwargs['name'] + " " + 'bought' + " " + str(cart[i]))
