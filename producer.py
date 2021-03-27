"""
This module represents the Producer.

Computer Systems Architecture Course
Assignment 1
March 2021
"""
import time
from threading import Thread


class Producer(Thread):
    """
    Class that represents a producer.
    """

    def __init__(self, products, marketplace, republish_wait_time, **kwargs):
        """
        Constructor.

        @type products: List()
        @param products: a list of products that the producer will produce

        @type marketplace: Marketplace
        @param marketplace: a reference to the marketplace

        @type republish_wait_time: Time
        @param republish_wait_time: the number of seconds that a producer must
        wait until the marketplace becomes available

        @type kwargs:
        @param kwargs: other arguments that are passed to the Thread's __init__()
        """

        super(Producer, self).__init__()
        self.products = products
        self.marketplace = marketplace
        self.republish_wait_time = republish_wait_time
        self.kwargs = kwargs

    def run(self):
        self.id = self.marketplace.register_producer()
        """
            Producatorul se inregistreaza in market 
            dupa care incearca sa isi plaseze produsele pe raftul sau 
        """
        day = True
        while day:
            for it in self.products:
                for _ in range(it[1]):
                    approved = self.marketplace.publish(self.id, it[0])
                    if approved:
                        time.sleep(it[2])
                    else:
                        while not approved:
                            time.sleep(self.republish_wait_time)
                            approved = self.marketplace.publish(self.id, it[0])

            day = self.marketplace.end_day()
            print(day)
            if not day:
                break
            print("ALOO")
