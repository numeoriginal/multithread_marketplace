"""
This module represents the Marketplace.

Computer Systems Architecture Course
Assignment 1
March 2021
"""

import random
import collections


class Marketplace:
    """
    Class that represents the Marketplace. It's the central part of the implementation.
    The producers and consumers use its methods concurrently.
    """

    def __init__(self, queue_size_per_producer):
        """
        Constructor

        :type queue_size_per_producer: Int
        :param queue_size_per_producer: the maximum size of a queue associated with each producer
        """
        self.producers_queue = []
        self.consumers_queue = []
        self.queue_size = queue_size_per_producer
        self.producer_id_counter = -1
        self.consumers_id_counter = -1
        pass

    def register_producer(self):

        """
        Returns an id for the producer that calls this.
        """
        self.producers_queue.append(collections.deque(maxlen=self.queue_size))
        self.producer_id_counter += 1

        return self.producer_id_counter

    def publish(self, producer_id, product):
        """
               Adds the product provided by the producer to the marketplace

               :type producer_id: String
               :param producer_id: producer id

               :type product: Product
               :param product: the Product that will be published in the Marketplace

               :returns True or False. If the caller receives False, it should wait and then try again.
        """
        if len(self.producers_queue[producer_id]) == self.queue_size:
            return False
        else:

            self.producers_queue[producer_id].append(product)

            return True

    def new_cart(self):
        """
        Creates a new cart for the consumer

        :returns an int representing the cart_id
        """
        self.consumers_queue.append(collections.deque(maxlen=100))
        self.consumers_id_counter += 1
        return self.consumers_id_counter

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to add to cart

        :returns True or False. If the caller receives False, it should wait and then try again
        """
        for i in range(len(self.producers_queue)):
            # print(self.producers_queue[i].count(product))
            if self.producers_queue[i].count(product) >= 1:
                self.consumers_queue[cart_id].append(product)
                self.producers_queue[i].remove(product)
                return True

        return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.

        :type cart_id: Int
        :param cart_id: id cart

        :type product: Product
        :param product: the product to remove from cart
        """
        if self.consumers_queue[cart_id].count(product) > 1:
            self.consumers_queue[cart_id].remove(product)

    def place_order(self, cart_id):
        """
        Return a list with all the products in the cart.

        :type cart_id: Int
        :param cart_id: id cart
        """
        self.consumers_id_counter -= 1
        return self.consumers_queue[cart_id]

    def end_day(self):
        if self.consumers_id_counter < 0:
            return False
        return True
