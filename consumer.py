"""
This module represents the Consumer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Consumer(Thread):
    """
    Class that represents a consumer.
    """

    def __init__(self, carts, marketplace, retry_wait_time, **kwargs):

        Thread.__init__(self, **kwargs)
        self.carts = carts
        self.marketplace = marketplace
        self.retry_wait_time = retry_wait_time
        self.kwargs = kwargs
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
        """
            Fiecarui consumator i se acorda un cart cu un id

            Iterez prin cart, verific tipul operatiunii de efectuat add/remove
            executa operatia de cate ori se cere.

            In caz ca nu poate adauga in cos, asteapta un timp predefinit.

            La final printeaza la ecran ce are in cart dupa toate operatiile
        """
        cart_id = self.marketplace.new_cart()
        for el in self.carts:
            for action in el:
                if action['type'] == 'add':
                    for _ in range(action['quantity']):
                        approved = self.marketplace.add_to_cart(cart_id, action['product'])
                        while not approved:
                            time.sleep(self.retry_wait_time)
                            approved = self.marketplace.add_to_cart(cart_id, action['product'])
                else:
                    for _ in range(action['quantity']):
                        self.marketplace.remove_from_cart(cart_id, action['product'])

        self.marketplace.place_order(cart_id, self.kwargs['name'])

