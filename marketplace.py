"""
This module represents the Marketplace.
Computer Systems Architecture Course
Assignment 1
March 2021
"""
import threading


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
        self.n_lock = threading.Lock()
        self.queue_max_size = 0

    def register_producer(self):
        """
        Returns an id for the producer that calls this.

        Initializing producers starting with id - 0
        """
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

               Verify if there is space in the queue
        """
        with self.n_lock:
            if self.queue_max_size == (self.queue_size * (self.producer_id_counter + 1)):
                return False
            else:
                self.queue_max_size += 1
                self.producers_queue.append(product)
                return True

    def new_cart(self):
        """
        Creates a new cart for the consumer
        :returns an int representing the cart_id

        Initializing consumers starting with id - 0
        and a list for every consumer
        """
        with self.n_lock:
            self.consumers_id_counter += 1
            self.consumers_queue.append([])
            return self.consumers_id_counter

    def add_to_cart(self, cart_id, product):
        """
        Adds a product to the given cart. The method returns
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to add to cart
        :returns True or False. If the caller receives False, it should wait and then try again

        Verify if there is the desired product in the producers queue
        add if available , remove from producers queue

        if not available , signal to the consumer to wait until it is available
        """
        with self.n_lock:
            if self.producers_queue.count(product) >= 1:
                self.consumers_queue[cart_id].append(product)
                self.queue_max_size -= 1
                self.producers_queue.remove(product)
                return True
            return False

    def remove_from_cart(self, cart_id, product):
        """
        Removes a product from cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type product: Product
        :param product: the product to remove from cart


        Verify if the consumer has the item he wants to remove
        if he has it , then remove it from his cart and put it back
        into the producers queue
        """
        if self.consumers_queue[cart_id].count(product) >= 1:
            self.producers_queue.append(product)
            self.consumers_queue[cart_id].remove(product)

    def place_order(self, cart_id, name):
        """
        Return a list with all the products in the cart.
        :type cart_id: Int
        :param cart_id: id cart
        :type name: string

        Print the cart of the consumer at the end of all his desirable operations
        """
        self.consumers_id_counter -= 1
        for i in range(len(self.consumers_queue[cart_id])):
            print(name + " " + 'bought' + " " + str(self.consumers_queue[cart_id][i]))
        self.consumers_queue[cart_id].clear()

    def end_day(self):
        # Signal the producers when to finish producing
        if self.consumers_id_counter <= -1:
            return False
        return True
