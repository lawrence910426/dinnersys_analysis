from analysis.reencode.regex_dish import *
from analysis.reencode.name_dish import *


class reencode_dish:
    def __init__(self, orders=None):
        if orders is None:
            self.model = regex_dish()
            tmp = dict((i, self.model.get_name(i))
                       for i in range(self.model.get_count()))
            self.decoder = tmp
        else:
            self.model = name_dish(orders)
            self.decoder = self.model.decode

    def get_count(self):
        return self.model.get_count()

    def get_id(self, name):
        return self.model.get_id(name)

    def get_name(self, id):
        return self.model.get_name(id)
