class reencode_dish:
    def __init__(self, orders):
        data = {}
        for key in orders:
            row = orders[key]
            data[row.dish.name] = True

        count = 1       # make the id start from 1 ,0 is for other
        encoder = {}
        decoder = {}
        names = sorted(data.keys())
        for k in names:
            encoder[k] = count
            decoder[count] = k
            count += 1
        self.decoder = decoder
        self.encoder = encoder
        self.count = count + 1

    def get_count(self):
        return self.count

    def get_id(self, name):
        return self.encoder[name]

    def get_name(self, id):
        return self.decoder[id]
