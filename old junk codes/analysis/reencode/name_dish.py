class name_dish:

    def __init__(self ,orders):
        adapt = dict((orders[key].dish.name ,True) for key in orders.keys())

        i = 0
        for key in adapt:
            adapt[key] = i
            i += 1

        reverse = dict((adapt[k] ,k) for k in adapt)

        self.encode = adapt
        self.decode = reverse
    
    def get_count(self):
        return len(self.encode.keys())

    def get_id(self ,name):
        return self.encode[name]

    def get_name(self ,id):
        return self.decode[id]

        
    